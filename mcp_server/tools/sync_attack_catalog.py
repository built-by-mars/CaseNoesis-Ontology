#!/usr/bin/env python3
"""Synchronize the pinned MITRE ATT&CK technique catalog from STIX 2.1.

The ``attack-technique`` extension vendors a *partial* catalog
(``mitre-attack-catalog.ttl``) covering techniques cited by CASE/UCO
exemplars. This script is the one mechanism that refreshes labels and
comments from upstream MITRE ATT&CK STIX data while preserving the UCO
PR #676 punning pattern (``owl:Class`` + ``uco-action:Technique``).

Default source: ``mitre-attack/attack-stix-data`` Enterprise ATT&CK collection
(pinned version recorded in ``extensions/attack-technique/manifest.json``).

Usage:
    # Refresh from a pinned ATT&CK release (network)
    python3 mcp_server/tools/sync_attack_catalog.py --attack-version 19.1

    # Regenerate from a local STIX file (air-gapped)
    python3 mcp_server/tools/sync_attack_catalog.py --stix-file /path/to/enterprise-attack.json

    # Keep current technique membership; only refresh labels/comments
    python3 mcp_server/tools/sync_attack_catalog.py --stix-file ... --keep-existing

    # Add techniques cited by exemplars (or explicit IDs)
    python3 mcp_server/tools/sync_attack_catalog.py --stix-file ... --from-exemplars --include T1059.003
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

sys.path.insert(0, str(PROJECT_ROOT / "mcp_server"))
from extension_paths import extension_dir  # noqa: E402

EXT_DIR = extension_dir("attack-technique", PROJECT_ROOT)
CATALOG_FILE = "mitre-attack-catalog.ttl"
MANIFEST_FILE = "manifest.json"

STIX_REPO = "mitre-attack/attack-stix-data"
DEFAULT_ATTACK_VERSION = "19.1"
ATTACK_IRI_RE = re.compile(
    r"https://attack\.mitre\.org/techniques/(T[0-9]{4}(?:\.[0-9]{3})?)"
)
CATALOG_ID_RE = re.compile(r"attack:(T[0-9]{4}(?:\.[0-9]{3})?)")
EXEMPLAR_GLOBS = [
    "examples/cti/**/*.jsonld",
]


def _fetch(url: str, timeout: int = 180) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "case-uco-sdk-sync"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def stix_url_for_version(version: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{STIX_REPO}/master/"
        f"enterprise-attack/enterprise-attack-{version}.json"
    )


def _ttl_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


def load_stix(path: Path | None, version: str | None) -> tuple[dict, str, str]:
    """Return (bundle, attack_version, source_url_or_path)."""

    if path is not None:
        payload = json.loads(path.read_text(encoding="utf-8"))
        # Prefer explicit version; else try STIX collection name.
        ver = version or _version_from_bundle(payload) or "unknown"
        return payload, ver, str(path.resolve())
    if not version:
        raise SystemExit("provide --attack-version or --stix-file")
    url = stix_url_for_version(version)
    print(f"fetching {url}")
    payload = json.loads(_fetch(url).decode("utf-8"))
    return payload, version, url


def _version_from_bundle(bundle: dict) -> str | None:
    for obj in bundle.get("objects") or []:
        if obj.get("type") == "x-mitre-collection":
            name = str(obj.get("name") or "")
            m = re.search(r"v?(\d+\.\d+)", name)
            if m:
                return m.group(1)
            ver = obj.get("x_mitre_version") or obj.get("x_mitre_attack_spec_version")
            if ver:
                return str(ver)
    return None


def parse_techniques(bundle: dict) -> dict[str, dict[str, str]]:
    """Map external_id -> {name, description, tactics, platforms}."""

    # Build tactic id -> shortname from x-mitre-tactic / kill-chain phases.
    tactic_names: dict[str, str] = {}
    for obj in bundle.get("objects") or []:
        if obj.get("type") == "x-mitre-tactic":
            short = obj.get("x_mitre_shortname") or obj.get("name")
            if short:
                tactic_names[str(obj.get("id"))] = str(short)

    techniques: dict[str, dict[str, str]] = {}
    for obj in bundle.get("objects") or []:
        if obj.get("type") != "attack-pattern":
            continue
        if obj.get("revoked") or obj.get("x_mitre_deprecated"):
            continue
        ext_id = None
        for ref in obj.get("external_references") or []:
            if ref.get("source_name") == "mitre-attack" and ref.get("external_id"):
                ext_id = str(ref["external_id"])
                break
        if not ext_id or not ext_id.startswith("T"):
            continue
        phases = []
        for phase in obj.get("kill_chain_phases") or []:
            if phase.get("kill_chain_name") == "mitre-attack":
                phases.append(str(phase.get("phase_name") or ""))
        platforms = [str(p) for p in (obj.get("x_mitre_platforms") or [])]
        techniques[ext_id] = {
            "name": str(obj.get("name") or ext_id),
            "description": str(obj.get("description") or "").split("\n")[0][:400],
            "tactics": ", ".join(p.replace("-", " ").title() for p in phases if p),
            "platforms": ", ".join(platforms),
        }
    return techniques


def catalog_technique_ids() -> set[str]:
    path = EXT_DIR / CATALOG_FILE
    if not path.is_file():
        return set()
    return set(CATALOG_ID_RE.findall(path.read_text(encoding="utf-8")))


def exemplar_technique_ids() -> set[str]:
    found: set[str] = set()
    for pattern in EXEMPLAR_GLOBS:
        for path in PROJECT_ROOT.glob(pattern):
            if not path.is_file():
                continue
            found.update(ATTACK_IRI_RE.findall(path.read_text(encoding="utf-8")))
    return found


def render_catalog(
    technique_ids: list[str],
    stix_techniques: dict[str, dict[str, str]],
    *,
    attack_version: str,
    source: str,
) -> str:
    header = (
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
        "@prefix action: <https://ontology.unifiedcyberontology.org/uco/action/> .\n"
        "@prefix attack: <https://attack.mitre.org/techniques/> .\n"
        "\n"
        "#\n"
        "# Partial MITRE ATT&CK technique catalog, expressed with the uco-action:\n"
        "# Technique metaclass added in ucoProject/UCO PR #676.\n"
        "#\n"
        "# GENERATED FILE — regenerate with:\n"
        "#   python3 mcp_server/tools/sync_attack_catalog.py --attack-version "
        f"{attack_version}\n"
        "#   make sync-attack ATTACK_VERSION="
        f"{attack_version}\n"
        "#\n"
        "# Per that PR, \"A Technique instance is an owl:Class that is a subclass of\n"
        "# uco-action:Action.\" Each ATT&CK technique below is therefore a *punned\n"
        "# class*: it is simultaneously an instance of the uco-action:Technique\n"
        "# metaclass and an owl:Class that rdfs:subClassOf uco-action:Action.\n"
        "#\n"
        f"# Pinned Enterprise ATT&CK: v{attack_version}\n"
        f"# Source: {source}\n"
        "# Sync tool: mcp_server/tools/sync_attack_catalog.py\n"
        "#\n"
        "\n"
    )
    blocks: list[str] = []
    missing: list[str] = []
    for tid in technique_ids:
        info = stix_techniques.get(tid)
        if not info:
            missing.append(tid)
            continue
        label = _ttl_escape(info["name"])
        comment_parts = []
        if info["tactics"]:
            plural = "Tactics" if "," in info["tactics"] else "Tactic"
            comment_parts.append(f"{plural}: {info['tactics']}.")
        if info["platforms"]:
            comment_parts.append(f"Platforms: {info['platforms']}.")
        if info["description"]:
            comment_parts.append(_ttl_escape(info["description"]))
        comment = " ".join(comment_parts) or f"MITRE ATT&CK technique {tid}."
        blocks.append(
            f"attack:{tid}\n"
            f"\ta\n"
            f"\t\towl:Class ,\n"
            f"\t\taction:Technique\n"
            f"\t\t;\n"
            f"\trdfs:subClassOf action:Action ;\n"
            f'\trdfs:label "{label}"@en ;\n'
            f'\trdfs:comment "{_ttl_escape(comment)}"@en ;\n'
            f'\taction:techniqueID "{tid}" ;\n'
            f"\t.\n"
        )
    if missing:
        raise SystemExit(
            "STIX bundle missing technique(s) requested for the catalog: "
            + ", ".join(missing)
        )
    return header + "\n".join(blocks)


def update_manifest_provenance(
    *,
    attack_version: str,
    source: str,
    technique_count: int,
) -> None:
    manifest_path = EXT_DIR / MANIFEST_FILE
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    provenance = manifest.setdefault("provenance", {})
    provenance["attack_stix_repo"] = f"https://github.com/{STIX_REPO}"
    provenance["attack_version"] = attack_version
    provenance["attack_stix_source"] = source
    provenance["technique_count"] = technique_count
    provenance["synced"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    provenance["sync_tool"] = "mcp_server/tools/sync_attack_catalog.py"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"updated manifest provenance (ATT&CK v{attack_version}, "
        f"{technique_count} techniques)"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--attack-version",
        default=None,
        help=f"Enterprise ATT&CK release to fetch (default pin: {DEFAULT_ATTACK_VERSION})",
    )
    parser.add_argument(
        "--stix-file",
        type=Path,
        default=None,
        help="Local enterprise-attack STIX 2.1 JSON (air-gapped / offline)",
    )
    parser.add_argument(
        "--keep-existing",
        action="store_true",
        help="Retain current catalog membership (default when no --from-exemplars/--include)",
    )
    parser.add_argument(
        "--from-exemplars",
        action="store_true",
        help="Union technique IDs cited by examples/cti/**/*.jsonld",
    )
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Additional technique ID (repeatable), e.g. --include T1059.003",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print membership and exit without writing files",
    )
    args = parser.parse_args(argv)

    version = args.attack_version
    if version is None and args.stix_file is None:
        # Prefer pinned version from manifest when present.
        manifest = json.loads((EXT_DIR / MANIFEST_FILE).read_text(encoding="utf-8"))
        version = (
            (manifest.get("provenance") or {}).get("attack_version")
            or DEFAULT_ATTACK_VERSION
        )

    bundle, attack_version, source = load_stix(args.stix_file, version)
    stix_techniques = parse_techniques(bundle)
    print(f"STIX techniques available: {len(stix_techniques)} (ATT&CK v{attack_version})")

    selected: set[str] = set()
    if args.keep_existing or (
        not args.from_exemplars and not args.include
    ):
        selected |= catalog_technique_ids()
    if args.from_exemplars:
        selected |= exemplar_technique_ids()
    for tid in args.include:
        selected.add(tid.strip())

    if not selected:
        raise SystemExit(
            "no technique IDs selected; use --keep-existing, --from-exemplars, "
            "and/or --include"
        )

    ordered = sorted(selected, key=lambda t: (t.split(".")[0], t))
    print(f"catalog membership: {len(ordered)} techniques")
    if args.dry_run:
        print(", ".join(ordered))
        return 0

    ttl = render_catalog(
        ordered,
        stix_techniques,
        attack_version=attack_version,
        source=source,
    )
    out = EXT_DIR / CATALOG_FILE
    out.write_text(ttl, encoding="utf-8")

    # Round-trip parse when rdflib is available.
    try:
        import rdflib

        rdflib.Graph().parse(str(out), format="turtle")
    except ImportError:
        print("warning: rdflib not installed; skipped TTL parse check")

    update_manifest_provenance(
        attack_version=attack_version,
        source=source,
        technique_count=len(ordered),
    )
    print(f"wrote {out.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
