"""Python AST serializer/builder checks for the deterministic critic."""

from __future__ import annotations

import ast
from pathlib import Path

from critic.models import CriticFinding, CriticTarget


def analyze_python_serializer(path: Path, source: str) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    try:
        tree = ast.parse(source, filename=str(path.name))
    except SyntaxError as exc:
        findings.append(
            _s(
                rule_id="CRIT-S-PY-SYNTAX",
                severity="critical",
                category="serializer_api",
                target=CriticTarget(path=path.name, line=exc.lineno),
                evidence=[exc.msg],
                rationale="Serializer/builder Python source does not parse.",
                recommended_change="Fix syntax errors before critic review.",
                verification_method="ast.parse the serializer source.",
            )
        )
        return findings

    findings.extend(_private_objects_mutation(path, tree))
    findings.extend(_json_dumps_as_serialization(path, tree))
    findings.extend(_fail_open_validation(path, tree))
    findings.extend(_broad_swallowed_exceptions(path, tree))
    findings.extend(_uuid4_global_ids(path, tree))
    return findings


def _private_objects_mutation(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr == "_objects":
            # assignment or call target
            parent_line = getattr(node, "lineno", None)
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-PRIVATE-OBJECTS",
                    severity="high",
                    category="serializer_api",
                    target=CriticTarget(path=path.name, line=parent_line),
                    evidence=["attribute=_objects"],
                    rationale=(
                        "Builder references CASEGraph private _objects; use public "
                        "composition APIs (create/upsert/link/get)."
                    ),
                    recommended_change="Replace _objects access with public CASEGraph methods.",
                    verification_method="AST search for Attribute.attr == '_objects'.",
                )
            )
    return findings


def _json_dumps_as_serialization(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    uses_json_dumps = False
    uses_graph_write = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr == "dumps":
                if isinstance(func.value, ast.Name) and func.value.id == "json":
                    uses_json_dumps = True
            if isinstance(func, ast.Attribute) and func.attr in {
                "write",
                "serialize",
                "write_streaming",
            }:
                uses_graph_write = True
    if uses_json_dumps and not uses_graph_write:
        findings.append(
            _s(
                rule_id="CRIT-S-PY-JSON-DUMPS-ONLY",
                severity="high",
                category="serializer_api",
                target=CriticTarget(path=path.name),
                evidence=["json.dumps without graph.write/serialize"],
                rationale=(
                    "Builder uses json.dumps without CASEGraph write/serialize; "
                    "typed SDK serialization and context handling may be bypassed."
                ),
                recommended_change="Emit via CASEGraph.write() / serialize().",
                verification_method="AST: json.dumps present and write/serialize absent.",
            )
        )
    return findings


def _fail_open_validation(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    source_segments = [
        (node, ast.get_source_segment)
        for node in ast.walk(tree)
        if isinstance(node, (ast.If, ast.Return))
    ]
    # Look for: if not validator_available(): return True/success patterns nearby
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        calls_validator = False
        negated = False
        if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
            negated = True
            test = test.operand
        if isinstance(test, ast.Call):
            func = test.func
            if isinstance(func, ast.Attribute) and func.attr == "validator_available":
                calls_validator = True
            if isinstance(func, ast.Name) and func.id == "validator_available":
                calls_validator = True
        if not (calls_validator and negated):
            continue
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                val = stmt.value
                if isinstance(val, ast.Constant) and val.value in (True, "ok", "success"):
                    findings.append(
                        _s(
                            rule_id="CRIT-S-PY-FAIL-OPEN-VALIDATION",
                            severity="critical",
                            category="serializer_validation",
                            target=CriticTarget(path=path.name, line=node.lineno),
                            evidence=["not validator_available() → success return"],
                            rationale=(
                                "Validation path returns success when case_validate "
                                "is unavailable (fail-open)."
                            ),
                            recommended_change=(
                                "Fail closed: skip with pytest.skip / return error / raise."
                            ),
                            verification_method="AST If not validator_available return True.",
                        )
                    )
            if isinstance(stmt, ast.Pass):
                findings.append(
                    _s(
                        rule_id="CRIT-S-PY-FAIL-OPEN-VALIDATION",
                        severity="critical",
                        category="serializer_validation",
                        target=CriticTarget(path=path.name, line=node.lineno),
                        evidence=["not validator_available() → pass"],
                        rationale="Validation skipped silently when unavailable.",
                        recommended_change="Fail closed when the validator is unavailable.",
                        verification_method="AST If not validator_available: pass.",
                    )
                )
    _ = source_segments  # reserved for future segment-based checks
    return findings


def _broad_swallowed_exceptions(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        if node.type is None:
            broad = True
        elif isinstance(node.type, ast.Name) and node.type.id == "Exception":
            broad = True
        else:
            broad = False
        if not broad:
            continue
        body = node.body
        if len(body) == 1 and isinstance(body[0], ast.Pass):
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-SWALLOWED-EXCEPTION",
                    severity="high",
                    category="serializer_safety",
                    target=CriticTarget(path=path.name, line=node.lineno),
                    evidence=["except Exception: pass"],
                    rationale="Broad exception handler swallows errors silently.",
                    recommended_change="Catch specific errors and surface failures.",
                    verification_method="AST ExceptHandler with Pass body.",
                )
            )
    return findings


def _uuid4_global_ids(path: Path, tree: ast.AST) -> list[CriticFinding]:
    """Flag uuid4-based ID helpers that ignore parent context (heuristic)."""

    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        name = node.name.lower()
        if "id" not in name and "iri" not in name:
            continue
        uses_uuid4 = False
        uses_parent = False
        for child in ast.walk(node):
            if isinstance(child, ast.Attribute) and child.attr == "uuid4":
                uses_uuid4 = True
            if isinstance(child, ast.Name) and child.id in {
                "parent",
                "parent_id",
                "parent_iri",
                "scope",
            }:
                uses_parent = True
            if isinstance(child, ast.arg) and child.arg in {
                "parent",
                "parent_id",
                "parent_iri",
                "scope",
            }:
                uses_parent = True
        if uses_uuid4 and not uses_parent and name.startswith(("make_", "new_", "build_")):
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-GLOBAL-UUID-IDS",
                    severity="medium",
                    category="serializer_api",
                    target=CriticTarget(path=path.name, line=node.lineno),
                    evidence=[f"function={node.name}"],
                    rationale=(
                        "ID helper uses uuid4 without parent/scope parameters; "
                        "nested objects may collide across parents."
                    ),
                    recommended_change="Include parent IRI/scope in deterministic nested IDs.",
                    verification_method="AST FunctionDef with uuid4 and no parent arg.",
                )
            )
    return findings


def _s(
    *,
    rule_id: str,
    severity: str,
    category: str,
    target: CriticTarget,
    evidence: list[str],
    rationale: str,
    recommended_change: str,
    verification_method: str,
) -> CriticFinding:
    finding = CriticFinding(
        finding_id="CRIT-PENDING",
        severity=severity,  # type: ignore[arg-type]
        category=category,
        confidence=0.95,
        status="new",
        target=target,
        evidence_kind="deterministic",
        evidence=evidence,
        rationale=rationale,
        recommended_change=recommended_change,
        verification_method=verification_method,
        rule_id=rule_id,
    )
    finding.ensure_identity_key()
    return finding
