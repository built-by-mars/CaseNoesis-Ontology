"""Python AST serializer/builder checks for the deterministic critic (Round 2)."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Literal

from critic.canonical import RuleExecution
from critic.finding_diff import make_stable_finding_id
from critic.models import CriticFinding, CriticTarget

RULE_VERSION = "1.1.0"

_PY_RULES = (
    "CRIT-S-PY-PRIVATE-OBJECTS",
    "CRIT-S-PY-JSON-DUMPS-ONLY",
    "CRIT-S-PY-FAIL-OPEN-VALIDATION",
    "CRIT-S-PY-SWALLOWED-EXCEPTION",
    "CRIT-S-PY-UNSCOPED-UUID5",
    "CRIT-S-PY-GLOBAL-UUID-IDS",
    "CRIT-S-PY-NONEXISTENT-API",
    "CRIT-S-PY-REL-ID-COLLAPSE",
    "CRIT-S-PY-SILENT-LOOKUP",
    "CRIT-S-PY-UNSAFE-OVERWRITE",
    "CRIT-S-PY-SOURCE-HASH-DRIFT",
    "CRIT-S-PY-SYNTHETIC-HASH",
    "CRIT-S-PY-QUADRATIC-SCAN",
)

_NESTED_ID_KEYWORDS = ("entry", "dict", "item", "child", "nested")
_CASE_SCOPED_HELPER_NAMES = frozenset({"uid", "make_id", "iri_for"})
_GRAPH_RECEIVER_NAMES = frozenset({"graph", "g", "case_graph", "cg"})
_CASEGRAPH_ALLOWLIST = frozenset({
    "create",
    "create_relationship",
    "write",
    "write_streaming",
    "get",
    "contains",
    "upsert_node",
    "link",
    "partition",
    "partition_by_roots",
    "serialize",
    "from_jsonld",
    "clear",
    "add_context",
    "set_context",
    "objects",
    "__iter__",
    "__len__",
    "__contains__",
})
_HEX64_RE = re.compile(r"^[0-9a-fA-F]{64}$")
_SYNTHETIC_HASH_NAME_RE = re.compile(
    r"(synthetic_hash|fake_hash|placeholder_hash)",
    re.IGNORECASE,
)

def _exec(
    rule_id: str,
    artifact_hash: str,
    finding_ids: list[str],
    *,
    status: str = "evaluated",
    examined: int = 1,
    error: str | None = None,
) -> RuleExecution:
    return RuleExecution(
        rule_id=rule_id,
        rule_version=RULE_VERSION,
        status=status,  # type: ignore[arg-type]
        input_artifact_hash=artifact_hash,
        targets_examined=examined,
        finding_ids=finding_ids,
        error_code=error,
        required_for_scope=True,
        verifies_rule_ids=[rule_id],
    )


def analyze_python_serializer(
    path: Path,
    source: str,
    *,
    serializer_mode: Literal["typed_sdk", "raw_fixture", "auto"] = "auto",
    artifact_hash: str | None = None,
) -> tuple[list[CriticFinding], list[RuleExecution]]:
    findings: list[CriticFinding] = []
    artifact = artifact_hash or path.name
    try:
        tree = ast.parse(source, filename=str(path.name))
    except SyntaxError as exc:
        finding = _s(
            rule_id="CRIT-S-PY-SYNTAX",
            severity="critical",
            category="serializer_api",
            target=CriticTarget(path=path.name, line=exc.lineno),
            evidence=[exc.msg],
            rationale="Serializer/builder Python source does not parse.",
            recommended_change="Fix syntax errors before critic review.",
            verification_method="ast.parse the serializer source.",
        )
        return [finding], [
            _exec(
                "CRIT-S-PY-SYNTAX",
                artifact,
                [finding.finding_id],
                status="failed",
                examined=0,
                error=type(exc).__name__,
            )
        ]

    findings.extend(_private_objects_mutation(path, tree))
    findings.extend(_json_dumps_as_serialization(path, tree, serializer_mode))
    findings.extend(_fail_open_validation(path, tree))
    findings.extend(_broad_swallowed_exceptions(path, tree))
    findings.extend(_uuid_helpers(path, tree))
    findings.extend(_nonexistent_sdk_api(path, tree))
    findings.extend(_relationship_id_collapse(path, tree))
    findings.extend(_silent_lookup_failure(path, tree))
    findings.extend(_unsafe_overwrite_or_workspace_bypass(path, tree, source))
    findings.extend(_source_hash_drift(path, tree))
    findings.extend(_synthetic_vs_evidence_hash(path, tree))
    findings.extend(_quadratic_full_scans(path, tree))

    executions = [
        _exec(
            rule_id,
            artifact,
            [f.finding_id for f in findings if f.rule_id == rule_id],
        )
        for rule_id in _PY_RULES
    ]
    return findings, executions


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


def _is_case_scoped_id_helper(node: ast.FunctionDef) -> bool:
    """Simple uid(label)/make_id(label) helpers are case-scoped, not nested-entry IDs."""

    base_name = node.name.lower().lstrip("_")
    if base_name not in _CASE_SCOPED_HELPER_NAMES:
        return False
    if any(keyword in node.name.lower() for keyword in _NESTED_ID_KEYWORDS):
        return False
    arg_names = [a.arg for a in node.args.args if a.arg not in {"self", "cls"}]
    return len(arg_names) == 1


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
        if uses_uuid5 and not uses_parent and not _is_case_scoped_id_helper(node):
            nested_identity = any(keyword in name for keyword in _NESTED_ID_KEYWORDS)
            if nested_identity or _uuid5_material_omits_parent(node):
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


def _uuid5_material_omits_parent(node: ast.FunctionDef) -> bool:
    """True when uuid5 namespace/name args do not reference parent/scope identifiers."""

    parent_tokens = {"parent", "parent_id", "parent_iri", "scope"}
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        func = child.func
        if not (isinstance(func, ast.Attribute) and func.attr == "uuid5"):
            continue
        for arg in child.args:
            if isinstance(arg, ast.Name) and arg.id in parent_tokens:
                return False
            if isinstance(arg, ast.Attribute) and arg.attr in parent_tokens:
                return False
        return True
    return False


def _nonexistent_sdk_api(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not isinstance(func, ast.Attribute):
            continue
        if not _is_graph_receiver(func.value):
            continue
        method = func.attr
        if method in _CASEGRAPH_ALLOWLIST:
            continue
        findings.append(
            _s(
                rule_id="CRIT-S-PY-NONEXISTENT-API",
                severity="high",
                category="serializer_api",
                target=CriticTarget(
                    path=path.name,
                    line=getattr(node, "lineno", None),
                    qualified_name=method,
                ),
                evidence=[f"call={method}"],
                rationale=(
                    f"Call to unknown CASEGraph method {method!r}; not in the "
                    "public allowlist."
                ),
                recommended_change="Use a documented CASEGraph API method.",
                verification_method="AST Attribute call on graph/g/case_graph allowlist.",
            )
        )
    return findings


def _is_graph_receiver(node: ast.AST) -> bool:
    return isinstance(node, ast.Name) and node.id in _GRAPH_RECEIVER_NAMES


def _relationship_id_collapse(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.For):
            continue
        for child in ast.walk(node):
            if child is node or not isinstance(child, ast.Call):
                continue
            func = child.func
            if not (
                isinstance(func, ast.Attribute)
                and func.attr == "create_relationship"
                and _is_graph_receiver(func.value)
            ):
                continue
            kw_names = {
                kw.arg for kw in child.keywords if isinstance(kw.arg, str)
            }
            if "assertion_id" in kw_names or "relationship_id" in kw_names:
                continue
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-REL-ID-COLLAPSE",
                    severity="high",
                    category="serializer_api",
                    target=CriticTarget(
                        path=path.name,
                        line=getattr(child, "lineno", None),
                        qualified_name="create_relationship",
                    ),
                    evidence=["create_relationship_in_for_without_assertion_id"],
                    rationale=(
                        "create_relationship in a loop without assertion_id/"
                        "relationship_id can collapse repeated assertions."
                    ),
                    recommended_change=(
                        "Pass assertion_id or relationship_id for repeated edges."
                    ),
                    verification_method="AST For containing create_relationship without id kw.",
                )
            )
    return findings


def _silent_lookup_failure(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    seen_lines: set[int] = set()

    def scan_block(stmts: list[ast.stmt], assigned_from_get: set[str]) -> None:
        local_gets = set(assigned_from_get)
        for stmt in stmts:
            if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
                target = stmt.targets[0]
                if isinstance(target, ast.Name) and isinstance(stmt.value, ast.Call):
                    func = stmt.value.func
                    if isinstance(func, ast.Attribute) and func.attr == "get":
                        local_gets.add(target.id)
            if isinstance(stmt, ast.If):
                names = _names_in_test(stmt.test)
                hit = names & local_gets
                if hit and not _body_has_raise(stmt.body) and not _body_has_raise(
                    stmt.orelse
                ):
                    if _body_has_silent_exit(stmt.body) or _body_has_silent_exit(
                        stmt.orelse
                    ):
                        line = stmt.lineno
                        if line not in seen_lines:
                            seen_lines.add(line)
                            findings.append(
                                _s(
                                    rule_id="CRIT-S-PY-SILENT-LOOKUP",
                                    severity="high",
                                    category="serializer_safety",
                                    target=CriticTarget(path=path.name, line=line),
                                    evidence=[f"lookup_names={sorted(hit)}"],
                                    rationale=(
                                        "Assignment from .get(...) followed by If that "
                                        "returns/passes/continues without Raise — silent "
                                        "lookup failure."
                                    ),
                                    recommended_change=(
                                        "Raise or surface a finding when required lookup fails."
                                    ),
                                    verification_method=(
                                        "AST Assign .get + If Return/Pass/Continue without Raise."
                                    ),
                                )
                            )
                scan_block(stmt.body, local_gets)
                scan_block(stmt.orelse, local_gets)
            elif isinstance(stmt, (ast.For, ast.While, ast.With, ast.AsyncWith)):
                scan_block(stmt.body, local_gets)
            elif isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                scan_block(stmt.body, set())
            elif isinstance(stmt, ast.ClassDef):
                scan_block(stmt.body, set())

    assert isinstance(tree, ast.Module)
    scan_block(tree.body, set())
    return findings


def _names_in_test(test: ast.AST) -> set[str]:
    return {n.id for n in ast.walk(test) if isinstance(n, ast.Name)}


def _body_has_raise(body: list[ast.stmt]) -> bool:
    for stmt in body:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Raise):
                return True
    return False


def _body_has_silent_exit(body: list[ast.stmt]) -> bool:
    for stmt in body:
        if isinstance(stmt, (ast.Return, ast.Pass, ast.Continue)):
            return True
        if isinstance(stmt, ast.If) and (
            _body_has_silent_exit(stmt.body) or _body_has_silent_exit(stmt.orelse)
        ):
            return True
    return False

def _unsafe_overwrite_or_workspace_bypass(
    path: Path,
    tree: ast.AST,
    source: str,
) -> list[CriticFinding]:
    if "workspace_policy" in source:
        return []
    findings: list[CriticFinding] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            # open(..., "w") / open(..., mode="w")
            if isinstance(func, ast.Name) and func.id == "open":
                if _open_is_write(node):
                    findings.append(
                        _s(
                            rule_id="CRIT-S-PY-UNSAFE-OVERWRITE",
                            severity="high",
                            category="serializer_safety",
                            target=CriticTarget(
                                path=path.name,
                                line=getattr(node, "lineno", None),
                                qualified_name="open",
                            ),
                            evidence=["open_write_without_workspace_policy"],
                            rationale=(
                                "open(..., 'w') without workspace_policy in the same file."
                            ),
                            recommended_change=(
                                "Route writes through workspace_policy / approved write roots."
                            ),
                            verification_method="AST open write mode; module lacks workspace_policy.",
                        )
                    )
            if isinstance(func, ast.Attribute) and func.attr in {
                "write_text",
                "write_bytes",
            }:
                findings.append(
                    _s(
                        rule_id="CRIT-S-PY-UNSAFE-OVERWRITE",
                        severity="high",
                        category="serializer_safety",
                        target=CriticTarget(
                            path=path.name,
                            line=getattr(node, "lineno", None),
                            qualified_name=func.attr,
                        ),
                        evidence=[f"{func.attr}_without_workspace_policy"],
                        rationale=(
                            f"Path.{func.attr} without workspace_policy in the same file."
                        ),
                        recommended_change=(
                            "Route writes through workspace_policy / approved write roots."
                        ),
                        verification_method="AST Path.write_*; module lacks workspace_policy.",
                    )
                )
    return findings


def _open_is_write(node: ast.Call) -> bool:
    if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
        mode = node.args[1].value
        if isinstance(mode, str) and ("w" in mode or "a" in mode or "x" in mode):
            return True
    for kw in node.keywords:
        if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
            mode = kw.value.value
            if isinstance(mode, str) and ("w" in mode or "a" in mode or "x" in mode):
                return True
    return False


def _source_hash_drift(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    for func in ast.walk(tree):
        if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        has_hashlib = any(
            (isinstance(n, ast.Name) and n.id == "hashlib")
            or (isinstance(n, ast.Attribute) and n.attr in {"sha256", "sha1", "md5"})
            for n in ast.walk(func)
        )
        for node in ast.walk(func):
            if not isinstance(node, ast.Assign):
                continue
            hex_lit = _hex64_from_value(node.value)
            if not hex_lit:
                continue
            near_hash = False
            for target in node.targets:
                if _name_mentions_hash(target):
                    near_hash = True
            # Also: keyword-like via AnnAssign already covered; check RHS Name targets
            # assigned into hash_value constructions nearby in same function via Call kwargs
            if not near_hash:
                continue
            if has_hashlib:
                continue
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-SOURCE-HASH-DRIFT",
                    severity="high",
                    category="serializer_safety",
                    target=CriticTarget(
                        path=path.name,
                        line=getattr(node, "lineno", None),
                        qualified_name="hash_value",
                    ),
                    evidence=[f"hex_literal={hex_lit[:12]}..."],
                    rationale=(
                        "64-hex literal assigned near hash_value/hashValue without "
                        "hashlib in the same function — possible source-hash drift."
                    ),
                    recommended_change=(
                        "Compute hashValue with hashlib from the source bytes in-scope."
                    ),
                    verification_method="AST hex64 assign near hash_* without hashlib.",
                )
            )
    return findings


def _hex64_from_value(value: ast.AST) -> str | None:
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        if _HEX64_RE.match(value.value):
            return value.value
    return None


def _name_mentions_hash(target: ast.AST) -> bool:
    if isinstance(target, ast.Name):
        lower = target.id.lower()
        return "hash_value" in lower or "hashvalue" in lower or lower in {
            "hash_value",
            "hashvalue",
            "digest",
        }
    if isinstance(target, ast.Attribute):
        lower = target.attr.lower()
        return "hash_value" in lower or "hashvalue" in lower
    if isinstance(target, ast.Tuple):
        return any(_name_mentions_hash(elt) for elt in target.elts)
    return False


def _synthetic_vs_evidence_hash(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    synthetic_funcs: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if _SYNTHETIC_HASH_NAME_RE.search(node.name):
                synthetic_funcs.add(node.name)
    if not synthetic_funcs:
        return findings
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        # Call to synthetic helper
        called = None
        if isinstance(node.func, ast.Name) and node.func.id in synthetic_funcs:
            called = node.func.id
        elif isinstance(node.func, ast.Attribute) and node.func.attr in synthetic_funcs:
            called = node.func.attr
        if not called:
            continue
        # Parent context: used in hash construction if ancestor Assign/Call mentions hash
        # Simpler: any Call whose args include a Call to synthetic, or Assign of Call
        # We already are at the Call — flag when this Call appears in hash-ish assignment
        findings.append(
            _s(
                rule_id="CRIT-S-PY-SYNTHETIC-HASH",
                severity="high",
                category="serializer_safety",
                target=CriticTarget(
                    path=path.name,
                    line=getattr(node, "lineno", None),
                    qualified_name=called,
                ),
                evidence=[f"synthetic_helper={called}"],
                rationale=(
                    "synthetic_hash/fake_hash/placeholder_hash return feeds hash "
                    "construction — do not present as evidence digest."
                ),
                recommended_change=(
                    "Use real source/evidence hashes; reserve synthetic digests for Tier T0 only."
                ),
                verification_method="AST function name synthetic_*_hash and Call sites.",
            )
        )
    return findings


def _quadratic_full_scans(path: Path, tree: ast.AST) -> list[CriticFinding]:
    findings: list[CriticFinding] = []
    seen: set[int] = set()
    for outer in ast.walk(tree):
        if not isinstance(outer, ast.For):
            continue
        if not _iterates_graph_objects(outer.iter):
            continue
        for inner in ast.walk(outer):
            if inner is outer or not isinstance(inner, ast.For):
                continue
            if not _iterates_graph_objects(inner.iter):
                continue
            line = getattr(outer, "lineno", 0) or 0
            if line in seen:
                break
            seen.add(line)
            findings.append(
                _s(
                    rule_id="CRIT-S-PY-QUADRATIC-SCAN",
                    severity="medium",
                    category="serializer_performance",
                    target=CriticTarget(
                        path=path.name,
                        line=line or None,
                        qualified_name="_objects",
                    ),
                    evidence=["nested_for_over_graph_objects"],
                    rationale=(
                        "Nested For loops both iterate graph `_objects` / list(graph) — "
                        "likely O(n²) scan."
                    ),
                    recommended_change="Index by IRI or use a single pass / map lookup.",
                    verification_method="AST nested For over _objects or list/iter(graph).",
                )
            )
            break
    return findings


def _iterates_graph_objects(iter_node: ast.AST) -> bool:
    if isinstance(iter_node, ast.Attribute) and iter_node.attr == "_objects":
        return True
    if isinstance(iter_node, ast.Call):
        func = iter_node.func
        if isinstance(func, ast.Name) and func.id in {"list", "iter", "tuple"}:
            if iter_node.args:
                return _iterates_graph_objects(iter_node.args[0])
        if isinstance(func, ast.Attribute) and func.attr in {"values", "keys", "items"}:
            if isinstance(func.value, ast.Attribute) and func.value.attr == "_objects":
                return True
        # list(graph) / iter(graph)
        if isinstance(func, ast.Name) and func.id in {"list", "iter"} and iter_node.args:
            arg0 = iter_node.args[0]
            if isinstance(arg0, ast.Name) and arg0.id in _GRAPH_RECEIVER_NAMES:
                return True
    if isinstance(iter_node, ast.Name) and iter_node.id in _GRAPH_RECEIVER_NAMES:
        return True
    return False


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
        verifier_rule_id=rule_id,
        rule_version=RULE_VERSION,
        identity_key=finding_id,
    )
