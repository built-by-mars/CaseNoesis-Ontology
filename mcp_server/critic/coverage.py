"""Source/coverage contract comparison for the deterministic critic."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from critic.graph_integrity import iter_nodes
from critic.models import CriticFinding, CriticTarget


def compare_coverage_contract(
    document: dict[str, Any],
    contract_path: Path,
) -> list[CriticFinding]:
    """Compare a machine-readable coverage contract against graph labels/IDs."""

    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [
            CriticFinding(
                finding_id="CRIT-PENDING",
                severity="high",
                category="coverage",
                confidence=1.0,
                status="new",
                target=CriticTarget(path=contract_path.name),
                evidence_kind="source",
                evidence=[type(exc).__name__],
                rationale="Coverage contract could not be parsed.",
                recommended_change="Provide valid JSON coverage contract.",
                verification_method="json.loads coverage_contract_path",
                rule_id="CRIT-C-CONTRACT-PARSE",
            )
        ]

    findings: list[CriticFinding] = []
    nodes = iter_nodes(document)
    blob = json.dumps(document, ensure_ascii=False)

    required_labels = contract.get("required_artifact_labels") or {}
    if isinstance(required_labels, dict):
        for group, labels in required_labels.items():
            if not isinstance(labels, list):
                continue
            for label in labels:
                text = str(label)
                if text not in blob:
                    findings.append(
                        CriticFinding(
                            finding_id="CRIT-PENDING",
                            severity="medium",
                            category="coverage",
                            confidence=0.85,
                            status="new",
                            target=CriticTarget(predicate=str(group)),
                            evidence_kind="source",
                            evidence=[f"missing_label={text}"],
                            rationale=(
                                "Coverage contract requires an artifact label that "
                                "does not appear in the graph serialization."
                            ),
                            recommended_change=f"Ensure {text} is represented in the graph.",
                            verification_method="Substring/label search in serialized graph.",
                            rule_id="CRIT-C-MISSING-LABEL",
                        )
                    )

    case_id = contract.get("case_identifier")
    if isinstance(case_id, str) and case_id and case_id not in blob:
        findings.append(
            CriticFinding(
                finding_id="CRIT-PENDING",
                severity="high",
                category="source_fidelity",
                confidence=0.9,
                status="new",
                target=CriticTarget(),
                evidence_kind="source",
                evidence=[f"case_identifier={case_id}"],
                rationale="Declared case identifier from coverage contract is absent from the graph.",
                recommended_change="Include the case identifier on Investigation/name fields.",
                verification_method="Search graph text for case_identifier.",
                rule_id="CRIT-C-CASE-ID-MISSING",
            )
        )

    min_nodes = contract.get("min_nodes")
    if isinstance(min_nodes, int) and len(nodes) < min_nodes:
        findings.append(
            CriticFinding(
                finding_id="CRIT-PENDING",
                severity="high",
                category="coverage",
                confidence=1.0,
                status="new",
                target=CriticTarget(),
                evidence_kind="source",
                evidence=[f"node_count={len(nodes)}", f"min_nodes={min_nodes}"],
                rationale="Graph node count is below the coverage contract minimum.",
                recommended_change="Regenerate the full scenario graph.",
                verification_method="Count @graph nodes versus min_nodes.",
                rule_id="CRIT-C-MIN-NODES",
            )
        )

    for finding in findings:
        finding.ensure_identity_key()
    return findings


def check_embedded_source_hash(
    document: dict[str, Any],
    source_hashes: dict[str, str],
) -> list[CriticFinding]:
    """Flag graph-embedded source hashes that disagree with actual file hashes."""

    if not source_hashes:
        return []
    blob = json.dumps(document, ensure_ascii=False)
    findings: list[CriticFinding] = []
    for name, digest in source_hashes.items():
        # If the graph mentions this filename and embeds a different sha256-looking value nearby,
        # we only flag when an explicit wrong hash string is present.
        # Conservative: if graph contains a sha256 hex that is not this digest but claims the file.
        marker = f"{name}"
        if marker not in blob:
            continue
        # Look for any 64-hex that isn't the true digest while filename present
        import re

        for match in re.findall(r"\b[a-fA-F0-9]{64}\b", blob):
            if match.lower() != digest.lower() and name in blob:
                # Only emit once per source file
                findings.append(
                    CriticFinding(
                        finding_id="CRIT-PENDING",
                        severity="high",
                        category="source_fidelity",
                        confidence=0.7,
                        status="new",
                        target=CriticTarget(path=name),
                        evidence_kind="source",
                        evidence=[
                            f"file_sha256={digest}",
                            f"graph_sha256_candidate={match}",
                        ],
                        rationale=(
                            "Graph contains a SHA-256 value that does not match the "
                            "hashed source file while referencing that source name."
                        ),
                        recommended_change="Update embedded source hashes to match file contents.",
                        verification_method="Compare embedded hex digest to sha256_file(source).",
                        rule_id="CRIT-C-SOURCE-HASH-MISMATCH",
                    )
                )
                break
    for finding in findings:
        finding.ensure_identity_key()
    return findings
