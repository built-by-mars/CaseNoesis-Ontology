"""Python AST serializer/builder checks for the deterministic critic (Round 2)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Literal

from critic.finding_diff import make_stable_finding_id
from critic.models import CriticFinding, CriticTarget


def analyze_python_serializer(
    path: Path,
    source: str,
    *,
    serializer_mode: Literal["typed_sdk", "raw_fixture", "auto"] = "auto",
) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    try:
        tree = ast.parse(source, filename=str(path.name))
    except SyntaxError as exc:
        return [
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
        ]

    findings.extend(_private_objects_mutation(path, tree))
    findings.extend(_json_dumps_as_serialization(path, tree, serializer_mode))
    findings.extend(_fail_open_validation(path, tree))
    findings.extend(_broad_swallowed_exceptions(path, tree))
    findings.extend(_uuid_helpers(path, tree))
    return findings


def _private_objects_mutation(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        # Assignment to *. _objects[...] or *. _objects = ...
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if _is_objects_attr(target):
                    findings.append(
                        _s(
                            rule_id="CRIT-S-PY-PRIVATE-OBJECTS",
                            severity="high",
                            category="serializer_api",
                            target=CriticTarget(
                                path=path.name,
                                line=getattr(node, "lineno", None),
                                qualified_name="_objects",
                            ),
                            evidence=["assignment_to_private__objects"],
                            rationale="Builder mutates CASEGraph private _objects.",
                            recommended_change="Use public CASEGraph composition APIs.",
                            verification_method="AST Assign to Attribute _objects.",
                        )
                    )
        if isinstance(node, ast.Subscript) and _is_objects_attr(node.value):
            # subscript write detected via AugAssign/Assign parents — also flag store ctx
            if isinstance(node.ctx, ast.Store):
                findings.append(
                    _s(
                        rule_id="CRIT-S-PY-PRIVATE-OBJECTS",
                        severity="high",
                        category="serializer_api",
                        target=CriticTarget(
                            path=path.name,
                            line=getattr(node, "lineno", None),
                            qualified_name="_objects",
                        ),
                        evidence=["store_to_private__objects_subscript"],
                        rationale="Builder mutates CASEGraph private _objects via subscript.",
                        recommended_change="Use public CASEGraph composition APIs.",
                        verification_method="AST Store to _objects[...].",
                    )
                )
    return findings


def _is_objects_attr(node: ast.AST) -> bool:
    return isinstance(node, ast.Attribute) and node.attr == "_objects"


def _json_dumps_as_serialization(
    path: Path,
    tree: ast.AST,
    serializer_mode: str,
) -> list[CriticFinding]:
    if serializer_mode == "raw_fixture":
        return []
    uses_json_dumps = False
    uses_graph_write = False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "dumps":
            if isinstance(func.value, ast.Name) and func.value.id == "json":
                uses_json_dumps = True
        if isinstance(func, ast.Attribute) and func.attr in {
            "write",
            "serialize",
            "write_streaming",
        }:
            # Prefer attribute on names suggestive of graph, not file handles
            if isinstance(func.value, ast.Name) and func.value.id in {
                "graph",
                "g",
                "case_graph",
                "cg",
            }:
                uses_graph_write = True
            elif isinstance(func.value, ast.Attribute):
                uses_graph_write = True  # graph.write path via attribute chain
    if uses_json_dumps and not uses_graph_write and serializer_mode in {"auto", "typed_sdk"}:
        return [
            _s(
                rule_id="CRIT-S-PY-JSON-DUMPS-ONLY",
                severity="high",
                category="serializer_api",
                target=CriticTarget(path=path.name, qualified_name="json.dumps"),
                evidence=["json.dumps without CASEGraph.write/serialize"],
                rationale=(
                    "Builder uses json.dumps without CASEGraph write/serialize; "
                    "typed SDK serialization may be bypassed."
                ),
                recommended_change="Emit via CASEGraph.write()/serialize() or set serializer_mode=raw_fixture.",
                verification_method="AST: json.dumps present; graph.write/serialize absent.",
            )
        ]
    return []


def _fail_open_validation(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        negated = False
        if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
            negated = True
            test = test.operand
        if not isinstance(test, ast.Call):
            continue
        func = test.func
        is_validator = (
            isinstance(func, ast.Attribute) and func.attr == "validator_available"
        ) or (isinstance(func, ast.Name) and func.id == "validator_available")
        if not (is_validator and negated):
            continue
        if _body_indicates_success(node.body):
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-FAIL-OPEN-VALIDATION",
                    severity="critical",
                    category="serializer_validation",
                    target=CriticTarget(path=path.name, line=node.lineno),
                    evidence=["not validator_available() → success-like path"],
                    rationale="Validation path succeeds when case_validate is unavailable.",
                    recommended_change="Fail closed when the validator is unavailable.",
                    verification_method="AST If not validator_available success path.",
                )
            )
    return findings


def _body_indicates_success(body: list[ast.stmt]) -> bool:
    for stmt in body:
        if isinstance(stmt, ast.Pass):
            return True
        if isinstance(stmt, ast.Return):
            val = stmt.value
            if val is None:
                return True
            if isinstance(val, ast.Constant) and val.value in (True, "ok", "success", 0):
                return True
            if isinstance(val, (ast.Tuple, ast.List, ast.Dict)):
                return True
            if isinstance(val, ast.Name):
                return True
        if isinstance(stmt, ast.If) and _body_indicates_success(stmt.body):
            return True
    return False


def _broad_swallowed_exceptions(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        broad = node.type is None or (
            isinstance(node.type, ast.Name) and node.type.id == "Exception"
        )
        if not broad:
            continue
        if _is_swallow(node.body):
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-SWALLOWED-EXCEPTION",
                    severity="high",
                    category="serializer_safety",
                    target=CriticTarget(path=path.name, line=node.lineno),
                    evidence=["broad_handler_swallows"],
                    rationale="Broad exception handler swallows errors.",
                    recommended_change="Catch specific errors and surface failures.",
                    verification_method="AST ExceptHandler swallow body.",
                )
            )
    return findings


def _is_swallow(body: list[ast.stmt]) -> bool:
    if not body:
        return True
    if len(body) == 1 and isinstance(body[0], (ast.Pass, ast.Continue)):
        return True
    if len(body) == 1 and isinstance(body[0], ast.Return):
        return True
    # log-and-ignore: Expr(Call(...)) then Pass/Continue/Return
    if len(body) == 2 and isinstance(body[0], ast.Expr) and isinstance(
        body[1], (ast.Pass, ast.Continue, ast.Return)
    ):
        return True
    return False


def _uuid_helpers(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        name = node.name.lower()
        if not any(tok in name for tok in ("id", "iri", "uid", "uuid")):
            continue
        uses_uuid4 = False
        uses_uuid5 = False
        uses_parent = False
        arg_names = {a.arg for a in node.args.args}
        if arg_names & {"parent", "parent_id", "parent_iri", "scope"}:
            uses_parent = True
        for child in ast.walk(node):
            if isinstance(child, ast.Attribute) and child.attr == "uuid4":
                uses_uuid4 = True
            if isinstance(child, ast.Attribute) and child.attr == "uuid5":
                uses_uuid5 = True
            if isinstance(child, ast.Name) and child.id in {
                "parent",
                "parent_id",
                "parent_iri",
                "scope",
            }:
                uses_parent = True
        if uses_uuid5 and not uses_parent:
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-UNSCOPED-UUID5",
                    severity="high",
                    category="serializer_api",
                    target=CriticTarget(
                        path=path.name,
                        line=node.lineno,
                        qualified_name=node.name,
                    ),
                    evidence=[f"function={node.name}"],
                    rationale=(
                        "Deterministic uuid5/label ID helper omits parent/scope; "
                        "nested entries can collide across parents."
                    ),
                    recommended_change="Include parent IRI/scope in nested ID material.",
                    verification_method="AST FunctionDef uuid5 without parent arg.",
                )
            )
        elif uses_uuid4 and not uses_parent and name.startswith(("make_", "new_", "build_")):
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-GLOBAL-UUID-IDS",
                    severity="medium",
                    category="serializer_api",
                    target=CriticTarget(
                        path=path.name,
                        line=node.lineno,
                        qualified_name=node.name,
                    ),
                    evidence=[f"function={node.name}"],
                    rationale="ID helper uses uuid4 (non-reproducible) without parent scope.",
                    recommended_change="Prefer deterministic parent-scoped IDs for nested objects.",
                    verification_method="AST FunctionDef uuid4 without parent arg.",
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
    finding_id = make_stable_finding_id(rule_id, *target.semantic_parts())
    return CriticFinding(
        finding_id=finding_id,
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
        identity_key=finding_id,
    )
