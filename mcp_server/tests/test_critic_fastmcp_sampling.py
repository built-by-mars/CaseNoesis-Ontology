"""In-process FastMCP sampling integration (string messages, pin 3.4.4)."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

fastmcp = pytest.importorskip("fastmcp")
from fastmcp import Client, Context, FastMCP  # noqa: E402


def test_fastmcp_context_sample_accepts_string_messages():
    """Exercise Context.sample with a plain string messages payload (FastMCP 3.4.4)."""

    mcp = FastMCP("critic-sampling-p0")

    @mcp.tool
    async def critic_probe(ctx: Context, user_payload: str) -> dict:
        result = await ctx.sample(
            messages=user_payload,
            system_prompt="You are a test critic.",
            max_tokens=128,
            temperature=0.0,
        )
        text = getattr(result, "text", None)
        if text is None and hasattr(result, "content"):
            content = result.content
            text = getattr(content, "text", None) or str(content)
        return {"sampled_text": text or str(result)}

    captured: dict = {}

    async def sampling_handler(messages, params, context):  # noqa: ANN001
        captured["message_count"] = len(messages)
        content = messages[0].content
        text = getattr(content, "text", None) or str(content)
        captured["user_text"] = text
        return json.dumps({"ok": True, "echo_len": len(text)})

    payload = json.dumps(
        {"instruction": "return json", "prompt_package": {"session_id": "s1"}},
        sort_keys=True,
    )

    async def _run():
        async with Client(mcp, sampling_handler=sampling_handler) as client:
            return await client.call_tool(
                "critic_probe", {"user_payload": payload}
            )

    result = asyncio.run(_run())
    assert result.is_error is False
    data = result.data if isinstance(result.data, dict) else json.loads(
        result.content[0].text
    )
    parsed = json.loads(data["sampled_text"])
    assert parsed["ok"] is True
    assert captured["message_count"] == 1
    assert captured["user_text"] == payload


def test_maybe_sample_critic_string_messages_and_policy_gate(tmp_path, monkeypatch):
    """maybe_sample_critic passes string messages and honors session policy."""

    import graph_validator
    from critic.sampling import FakeSampleContext, maybe_sample_critic
    from critic.sessions import start_critic_review

    fixtures = (
        Path(__file__).resolve().parent
        / "fixtures"
        / "critic"
        / "gold-charged-with.jsonld"
    )
    read = tmp_path / "read"
    write = tmp_path / "write"
    read.mkdir()
    write.mkdir()
    graph = read / "gold.jsonld"
    graph.write_text(fixtures.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setenv("CASE_UCO_MCP_READ_ROOTS", str(read))
    monkeypatch.setenv("CASE_UCO_MCP_WRITE_ROOTS", str(write))
    monkeypatch.setenv("CASE_UCO_CRITIC_SESSION_ROOT", str(write / "critic-sessions"))
    monkeypatch.setenv("CASE_UCO_MCP_ALLOW_OVERWRITE", "1")
    monkeypatch.delenv("CASE_UCO_MCP_CRITIC_MODE", raising=False)
    monkeypatch.setattr(graph_validator, "validator_available", lambda: True)
    monkeypatch.setattr(
        graph_validator,
        "validate_graph_file",
        lambda *a, **k: graph_validator.GraphValidationReport(
            conforms=True,
            warning_count=0,
            violation_count=0,
            exit_code=0,
            validator_name="case_validate",
            safe_summary="conforms",
            verification_status="complete",
        ),
    )

    started = start_critic_review(
        graph_path=str(graph), critic_scope="graph", model_policy="client_sampling"
    )
    package = started["prompt_package"]
    payload = {
        "schema_version": "1.2.0",
        "session_id": package["session_id"],
        "pass_number": package["pass_number"],
        "graph_sha256": package["artifact_hashes"]["graph_sha256"],
        "serializer_sha256": package["artifact_hashes"].get("serializer_sha256"),
        "prompt_package_hash": package["prompt_package_hash"],
        "review_request_sha256": package.get("review_request_sha256"),
        "review_config_sha256": package.get("review_config_sha256"),
        "findings": [],
        "finding_assessments": [],
        "scorecard": {},
    }
    ctx = FakeSampleContext(payload)
    ok = asyncio.run(
        maybe_sample_critic(ctx, package, model_policy="client_sampling")
    )
    assert ok.status == "ok"
    assert isinstance(ctx.kwargs_history[0]["messages"], str)

    skipped = asyncio.run(maybe_sample_critic(ctx, package, model_policy="manual"))
    assert skipped.status == "skipped_policy"
    assert ctx.calls == 1  # second call did not sample
