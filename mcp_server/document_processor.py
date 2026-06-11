"""Local CASE/UCO document processing for bounded MCP workflows.

Processes receipt/document images (embedded PNG text or OCR), PDFs (raw and
Flate-compressed text streams), OOXML Office documents, and CSV/TSV tables
into CASE/UCO-shaped JSON-LD using verified canonical ontology terms.

Honest-failure contract: when content cannot be extracted (no OCR engine for
an image, no text streams in a scanned PDF, empty table), processing raises a
typed ``ValueError`` instead of fabricating placeholder content. Optional
dependencies (the ``tesseract`` OCR CLI) are detected at runtime.

Ontology terms used here were verified against the CASE/UCO registry
(case-uco MCP ``get_class_details``): ``case-investigation:InvestigativeAction``
with ``uco-action:object/instrument/result/startTime/endTime``;
``uco-observable:FileFacet`` (fileName, extension, sizeInBytes);
``uco-observable:ContentDataFacet`` with ``uco-types:Hash``
(hashMethod/hashValue); ``uco-observable:ExtractedStringsFacet`` /
``uco-observable:ExtractedString``; ``uco-core:Relationship`` with
source/target/kindOfRelationship; ``uco-tool:Tool`` with ``uco-tool:version``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid
import zipfile
import zlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TOOL_NAME = "case-uco-document-normalize"
TOOL_VERSION = "0.3.0"
EXTRACTION_BUNDLE_CONTRACT_VERSION = "1.0"
EXTRACTED_CONTENT_FILENAME = "extracted-content.json"
ANNOTATIONS_FILENAME = "annotations.jsonld"
RFC7111_CONFORMS_TO = "http://tools.ietf.org/rfc/rfc7111"
MAX_BYTES = 10 * 1024 * 1024
MAX_CSV_RECORDS = 100
MAX_RECORD_TEXT = 400
OCR_COMMAND = "tesseract"
OCR_TIMEOUT_SECONDS = 60

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}
SUPPORTED_OFFICE_EXTENSIONS = {".docx", ".xlsx"}
SUPPORTED_CSV_EXTENSIONS = {".csv", ".tsv"}
PROGRESS_STAGES = {
    "started",
    "inspect_source",
    "extract_content",
    "build_graph",
    "write_graph",
    "completed",
    "failed",
}

# Matches OOXML text runs (<w:t>, sharedStrings <t>, inline <is><t>) without
# binding to a specific namespace prefix.
_OOXML_TEXT_RE = re.compile(r"<(?:\w+:)?t(?:\s[^>]*)?>([^<]{1,400})</(?:\w+:)?t>")


@dataclass(frozen=True)
class ExtractedRecord:
    """One reviewable record extracted from a source document.

    ``anchor`` (Spec026 extraction-bundle contract 1.0) locates the record in
    the canonical extracted content. Records that cannot be honestly located
    carry ``anchor=None`` and are simply absent from ``annotations.jsonld`` —
    anchors are never fabricated.
    """

    label: str
    text: str
    anchor: dict[str, Any] | None = None


@dataclass(frozen=True)
class ExtractedContent:
    document_type: str
    summary_fields: dict[str, str]
    records: list[ExtractedRecord]
    truncated: bool = False
    # Canonical content model serialized into extracted-content.json
    # ({"kind": "text", "sections": [...]} or {"kind": "table", "sheets": [...]}).
    canonical: dict[str, Any] | None = None


@dataclass(frozen=True)
class ProcessedDocument:
    source_path: Path
    output_path: Path
    file_kind: str
    sha256: str
    byte_size: int
    extracted_fields: dict[str, str]
    graph: dict[str, Any]
    records: list[ExtractedRecord] = field(default_factory=list)
    truncated: bool = False
    extracted_content_path: Path | None = None
    annotations_path: Path | None = None


class ProgressReporter:
    """Append safe line-delimited progress checkpoints for local callers."""

    def __init__(self, progress_output: str | Path | None) -> None:
        self.progress_output = Path(progress_output).expanduser().resolve() if progress_output else None

    def emit(self, stage: str, message: str, percent: int | None = None) -> None:
        if not self.progress_output:
            return
        if stage not in PROGRESS_STAGES:
            raise ValueError("unsupported_progress_stage")
        event: dict[str, Any] = {
            "stage": stage,
            "message": sanitize_text(message),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool_name": TOOL_NAME,
            "tool_version": TOOL_VERSION,
        }
        if percent is not None:
            event["percent"] = max(0, min(100, int(percent)))
        self.progress_output.parent.mkdir(parents=True, exist_ok=True)
        with self.progress_output.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")


def ocr_available() -> bool:
    """Return True when the optional tesseract OCR CLI is installed."""

    return shutil.which(OCR_COMMAND) is not None


def process_document_file(
    source_path: str | Path,
    output_path: str | Path,
    file_kind: str | None = None,
    safe_metadata: dict[str, Any] | None = None,
    progress_output: str | Path | None = None,
) -> ProcessedDocument:
    """Process a supported local document file and write CASE/UCO JSON-LD."""

    progress = ProgressReporter(progress_output)
    source = Path(source_path).expanduser().resolve()
    output = Path(output_path).expanduser().resolve()
    try:
        progress.emit("started", "case-uco document preprocessing started.", 0)
        if not source.exists() or not source.is_file():
            raise ValueError("source_missing")
        byte_size = source.stat().st_size
        if byte_size > MAX_BYTES:
            raise ValueError("source_oversized")
        progress.emit("inspect_source", "Inspected source metadata and size.", 15)
        kind = normalize_file_kind(file_kind, source)
        content = extract_content(source, kind)
        progress.emit("extract_content", f"Extracted safe fields for {kind}.", 45)
        sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
        graph = build_case_uco_graph(
            source=source,
            file_kind=kind,
            byte_size=byte_size,
            sha256=sha256,
            content=content,
            safe_metadata=safe_metadata or {},
        )
        progress.emit("build_graph", "Built CASE/UCO-shaped graph artifact.", 70)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")

        # Spec026 extraction bundle (contract 1.0): canonical extracted content
        # plus the Web Annotation companion graph, written beside the case graph.
        extracted_content_path: Path | None = None
        annotations_path: Path | None = None
        run_id = derive_run_id(source, sha256, kind)
        extracted_doc = build_extracted_content_document(sha256, kind, content)
        annotations_doc = build_annotations_document(run_id, content)
        if extracted_doc is not None and annotations_doc is not None:
            extracted_content_path = output.parent / EXTRACTED_CONTENT_FILENAME
            annotations_path = output.parent / ANNOTATIONS_FILENAME
            extracted_content_path.write_text(
                json.dumps(extracted_doc, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            annotations_path.write_text(
                json.dumps(annotations_doc, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        progress.emit("write_graph", "Wrote graph artifact to the case run directory.", 90)
        progress.emit("completed", "case-uco document preprocessing completed.", 100)
        return ProcessedDocument(
            source_path=source,
            output_path=output,
            file_kind=kind,
            sha256=sha256,
            byte_size=byte_size,
            extracted_fields=content.summary_fields,
            graph=graph,
            records=content.records,
            truncated=content.truncated,
            extracted_content_path=extracted_content_path,
            annotations_path=annotations_path,
        )
    except ValueError as exc:
        progress.emit("failed", f"case-uco document preprocessing failed: {exc}", 100)
        raise


def normalize_file_kind(file_kind: str | None, source: Path) -> str:
    requested = (file_kind or "").strip().lower().replace("-", "_")
    if requested in {"receipt_image", "pdf", "office", "csv_table"}:
        return requested

    ext = source.suffix.lower()
    if ext in SUPPORTED_IMAGE_EXTENSIONS:
        return "receipt_image"
    if ext in SUPPORTED_PDF_EXTENSIONS:
        return "pdf"
    if ext in SUPPORTED_OFFICE_EXTENSIONS:
        return "office"
    if ext in SUPPORTED_CSV_EXTENSIONS:
        return "csv_table"
    raise ValueError("unsupported_file_kind")


def extract_content(source: Path, file_kind: str) -> ExtractedContent:
    if file_kind == "csv_table":
        return extract_csv_content(source)
    if file_kind == "office":
        return extract_office_content(source)
    if file_kind == "pdf":
        return extract_pdf_content(source)
    if file_kind == "receipt_image":
        return extract_image_content(source)
    raise ValueError("unsupported_file_kind")


def extract_csv_content(source: Path) -> ExtractedContent:
    dialect = "excel-tab" if source.suffix.lower() == ".tsv" else "excel"
    with source.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, dialect=dialect)
        rows = list(reader)
    if not rows:
        raise ValueError("empty_csv")
    headers = [cell.strip() for cell in rows[0]]
    data_rows = rows[1:]
    if not data_rows:
        raise ValueError("empty_csv")
    records: list[ExtractedRecord] = []
    canonical_rows: list[list[str]] = []
    for index, row in enumerate(data_rows[:MAX_CSV_RECORDS], start=1):
        sanitized_cells = [sanitize_text(value) for value in row]
        canonical_rows.append(sanitized_cells)
        pairs = []
        for column, value in zip(headers, sanitized_cells):
            if value:
                pairs.append(f"{column or 'column'}={value}")
        text = sanitize_text("; ".join(pairs))[:MAX_RECORD_TEXT]
        if not text:
            continue
        records.append(
            ExtractedRecord(
                label=f"Row {index}: {text[:60]}",
                text=text,
                # RFC 7111 counts the header as row 1, so data row N is N+1.
                anchor={
                    "selector_kind": "csv_fragment",
                    "row_index": index,
                    "rfc7111_row": index + 1,
                },
            )
        )
    if not records:
        raise ValueError("empty_csv")
    truncated = len(data_rows) > MAX_CSV_RECORDS
    summary = {
        "document_type": "CSV/table",
        "table_columns": ", ".join(h for h in headers[:12] if h) or "unknown columns",
        "row_count": str(len(data_rows)),
        "record_count": str(len(records)),
    }
    if truncated:
        summary["truncated"] = f"first {MAX_CSV_RECORDS} of {len(data_rows)} rows extracted"
    return ExtractedContent(
        document_type="CSV/table",
        summary_fields=summary,
        records=records,
        truncated=truncated,
        canonical={
            "kind": "table",
            "sheets": [
                {
                    "name": "default",
                    "header": headers,
                    "rows": canonical_rows,
                    "total_source_rows": len(data_rows),
                    "truncated": truncated,
                }
            ],
        },
    )


def text_section_content(full_text: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """Canonical single-section text model plus the anchor for its lead record.

    The record text is a bounded prefix of the canonical section text, so a
    TextPositionSelector span starting at offset 0 is exact by construction.
    """

    record_text = full_text[:MAX_RECORD_TEXT]
    canonical = {
        "kind": "text",
        "sections": [{"section_id": "s1", "text": full_text}],
    }
    anchor = {
        "selector_kind": "text_position",
        "section_id": "s1",
        "start": 0,
        "end": len(record_text),
        "exact": record_text,
    }
    return canonical, anchor


def extract_office_content(source: Path) -> ExtractedContent:
    if not zipfile.is_zipfile(source):
        raise ValueError("invalid_office_document")
    texts: list[str] = []
    with zipfile.ZipFile(source) as archive:
        names = archive.namelist()
        if source.suffix.lower() == ".docx":
            part_names = [
                name
                for name in names
                if name.startswith("word/") and name.endswith(".xml")
            ]
        else:
            part_names = [
                name
                for name in names
                if name in ("xl/sharedStrings.xml",)
                or (name.startswith("xl/worksheets/") and name.endswith(".xml"))
            ]
        for name in part_names[:32]:
            raw = archive.read(name).decode("utf-8", errors="ignore")
            texts.extend(match.strip() for match in _OOXML_TEXT_RE.findall(raw) if match.strip())
    joined = sanitize_text(" ".join(texts))
    if not joined:
        raise ValueError("office_text_missing")
    canonical, anchor = text_section_content(joined)
    return ExtractedContent(
        document_type="Office document",
        summary_fields={
            "document_type": "Office document",
            "extracted_text": joined[:240],
            "source_part_count": str(len(texts)),
        },
        records=[
            ExtractedRecord(
                label=f"Office text: {joined[:60]}",
                text=joined[:MAX_RECORD_TEXT],
                anchor=anchor,
            )
        ],
        canonical=canonical,
    )


def extract_pdf_content(source: Path) -> ExtractedContent:
    data = source.read_bytes()
    blobs: list[bytes] = [data]
    for match in re.finditer(rb"stream\r?\n(.*?)\r?\nendstream", data, re.DOTALL):
        try:
            blobs.append(zlib.decompress(match.group(1)))
        except zlib.error:
            continue
    strings: list[str] = []
    seen: set[str] = set()
    for blob in blobs:
        raw = blob.decode("latin-1", errors="ignore")
        for fragment in re.findall(r"\((.{1,400}?)\)", raw):
            cleaned = sanitize_text(unescape_pdf_text(fragment))
            if cleaned and cleaned not in seen:
                seen.add(cleaned)
                strings.append(cleaned)
    text = sanitize_text(" ".join(strings))
    if not text:
        # Image-only/scanned PDFs carry no text streams; OCR for PDFs is not
        # implemented, so fail honestly instead of returning placeholders.
        raise ValueError("pdf_text_missing")
    canonical, anchor = text_section_content(text)
    return ExtractedContent(
        document_type="PDF document",
        summary_fields={
            "document_type": "PDF document",
            "extracted_text": text[:240],
        },
        records=[
            ExtractedRecord(
                label=f"PDF text: {text[:60]}",
                text=text[:MAX_RECORD_TEXT],
                anchor=anchor,
            )
        ],
        canonical=canonical,
    )


def extract_image_content(source: Path) -> ExtractedContent:
    text = ""
    extraction_method = ""
    if source.suffix.lower() == ".png":
        text = sanitize_text(extract_png_text(source))
        if text:
            extraction_method = "png_embedded_text"
    if not text:
        if not ocr_available():
            # No embedded text and no OCR engine: fail honestly rather than
            # fabricating "Synthetic image file ..." placeholder content.
            raise ValueError("ocr_unavailable")
        text = sanitize_text(run_ocr(source))
        extraction_method = "ocr_tesseract"
        if not text:
            raise ValueError("no_extractable_content")
    canonical, anchor = text_section_content(text)
    return ExtractedContent(
        document_type="Receipt image",
        summary_fields={
            "document_type": "Receipt image",
            "extracted_text": text[:240],
            "extraction_method": extraction_method,
        },
        records=[
            ExtractedRecord(
                label=f"Image text: {text[:60]}",
                text=text[:MAX_RECORD_TEXT],
                anchor=anchor,
            )
        ],
        canonical=canonical,
    )


def run_ocr(source: Path) -> str:
    command = shutil.which(OCR_COMMAND)
    if command is None:
        raise ValueError("ocr_unavailable")
    try:
        completed = subprocess.run(
            [command, str(source), "stdout"],
            capture_output=True,
            timeout=OCR_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("ocr_failed") from exc
    if completed.returncode != 0:
        raise ValueError("ocr_failed")
    return completed.stdout.decode("utf-8", errors="ignore")


def extract_png_text(source: Path) -> str:
    data = source.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ""
    cursor = 8
    chunks: list[str] = []
    while cursor + 8 <= len(data):
        length = int.from_bytes(data[cursor : cursor + 4], "big")
        chunk_type = data[cursor + 4 : cursor + 8]
        chunk_data = data[cursor + 8 : cursor + 8 + length]
        cursor += 12 + length
        if chunk_type == b"tEXt":
            _, _, value = chunk_data.partition(b"\x00")
            chunks.append(value.decode("latin-1", errors="ignore"))
        if chunk_type == b"IEND":
            break
    return " ".join(chunks)


def unescape_pdf_text(value: str) -> str:
    return (
        value.replace(r"\(", "(")
        .replace(r"\)", ")")
        .replace(r"\\", "\\")
        .replace(r"\n", " ")
        .replace(r"\r", " ")
        .replace(r"\t", " ")
    )


def derive_run_id(source: Path, sha256: str, file_kind: str) -> uuid.UUID:
    """Deterministic run namespace shared by the graph and annotation bundle."""

    return uuid.uuid5(uuid.NAMESPACE_URL, f"{source.name}:{sha256}:{file_kind}")


def record_node_id(run_id: uuid.UUID, index: int) -> str:
    """The graph @id for extracted record ``index`` (1-based)."""

    return f"urn:uuid:{uuid.uuid5(run_id, f'record-{index}')}"


def build_extracted_content_document(
    sha256: str,
    file_kind: str,
    content: ExtractedContent,
) -> dict[str, Any] | None:
    """The extracted-content.json document (contract 1.0), or None when the
    extractor produced no canonical content model (anchor-incapable path)."""

    if content.canonical is None:
        return None
    canonical_serialized = json.dumps(content.canonical, sort_keys=True, ensure_ascii=False)
    return {
        "contract_version": EXTRACTION_BUNDLE_CONTRACT_VERSION,
        "source_sha256": sha256,
        "content_sha256": hashlib.sha256(canonical_serialized.encode("utf-8")).hexdigest(),
        "extraction_tool": TOOL_NAME,
        "extraction_tool_version": TOOL_VERSION,
        "file_kind": file_kind,
        "content": content.canonical,
        "failures": [],
    }


def build_annotations_document(
    run_id: uuid.UUID,
    content: ExtractedContent,
) -> dict[str, Any] | None:
    """W3C Web Annotation companion graph anchoring record nodes to content.

    One annotation per anchored record; records with ``anchor=None`` are
    honestly absent. Returns None when no canonical content exists.
    """

    if content.canonical is None:
        return None
    annotations: list[dict[str, Any]] = []
    for index, record in enumerate(content.records, start=1):
        anchor = record.anchor
        if anchor is None:
            continue
        if anchor["selector_kind"] == "text_position":
            target_source = f"{EXTRACTED_CONTENT_FILENAME}#{anchor['section_id']}"
            selectors: list[dict[str, Any]] = [
                {
                    "type": "TextPositionSelector",
                    "start": anchor["start"],
                    "end": anchor["end"],
                },
                {"type": "TextQuoteSelector", "exact": anchor["exact"]},
            ]
        elif anchor["selector_kind"] == "csv_fragment":
            target_source = f"{EXTRACTED_CONTENT_FILENAME}#default"
            selectors = [
                {
                    "type": "FragmentSelector",
                    "conformsTo": RFC7111_CONFORMS_TO,
                    "value": f"row={anchor['rfc7111_row']}",
                }
            ]
        else:  # pragma: no cover - extractors only emit the kinds above
            raise ValueError("unsupported_anchor_selector")
        annotations.append(
            {
                "id": f"urn:link-look:anchor:{uuid.uuid5(run_id, f'anchor-{index}')}",
                "type": "Annotation",
                "body": record_node_id(run_id, index),
                "target": {"source": target_source, "selector": selectors},
            }
        )
    return {
        "@context": ["http://www.w3.org/ns/anno.jsonld"],
        "@graph": annotations,
    }


def build_case_uco_graph(
    source: Path,
    file_kind: str,
    byte_size: int,
    sha256: str,
    content: ExtractedContent,
    safe_metadata: dict[str, Any],
) -> dict[str, Any]:
    run_id = derive_run_id(source, sha256, file_kind)
    source_id = f"urn:uuid:{uuid.uuid5(run_id, 'source')}"
    tool_id = f"urn:uuid:{uuid.uuid5(run_id, 'tool')}"
    action_id = f"urn:uuid:{uuid.uuid5(run_id, 'action')}"
    file_name = sanitize_text(source.name)
    extension = source.suffix.lower().lstrip(".")
    now_iso = datetime.now(timezone.utc).isoformat()
    upload_reference = sanitize_text(str(safe_metadata.get("upload_id", "")))

    source_type = (
        "uco-observable:RasterPicture"
        if file_kind == "receipt_image"
        else "uco-observable:ObservableObject"
    )
    source_description = f"Link-Look {file_kind} upload"
    if upload_reference:
        source_description += f" (upload reference {upload_reference})"

    source_node: dict[str, Any] = {
        "@id": source_id,
        "@type": source_type,
        "uco-core:name": f"Source file {file_name}",
        "uco-core:description": source_description,
        "uco-core:tag": [f"link-look-file-kind:{file_kind}"],
        "uco-core:hasFacet": [
            {
                "@id": f"urn:uuid:{uuid.uuid5(run_id, 'file-facet')}",
                "@type": "uco-observable:FileFacet",
                "uco-observable:fileName": file_name,
                "uco-observable:extension": extension,
                "uco-observable:sizeInBytes": {
                    "@type": "xsd:integer",
                    "@value": str(byte_size),
                },
            },
            {
                "@id": f"urn:uuid:{uuid.uuid5(run_id, 'content-facet')}",
                "@type": "uco-observable:ContentDataFacet",
                "uco-observable:sizeInBytes": {
                    "@type": "xsd:integer",
                    "@value": str(byte_size),
                },
                "uco-observable:hash": [
                    {
                        "@id": f"urn:uuid:{uuid.uuid5(run_id, 'sha256-hash')}",
                        "@type": "uco-types:Hash",
                        "uco-types:hashMethod": "SHA256",
                        "uco-types:hashValue": {
                            "@type": "xsd:hexBinary",
                            "@value": sha256.upper(),
                        },
                    }
                ],
            },
        ],
    }

    tool_node = {
        "@id": tool_id,
        "@type": "uco-tool:Tool",
        "uco-core:name": TOOL_NAME,
        "uco-tool:version": TOOL_VERSION,
    }

    record_nodes: list[dict[str, Any]] = []
    relationship_nodes: list[dict[str, Any]] = []
    record_refs: list[dict[str, str]] = []
    for index, record in enumerate(content.records, start=1):
        record_id = record_node_id(run_id, index)
        record_refs.append({"@id": record_id})
        record_nodes.append(
            {
                "@id": record_id,
                "@type": "uco-observable:ObservableObject",
                "uco-core:name": record.label,
                "uco-core:description": record.text,
                "uco-core:hasFacet": [
                    {
                        "@id": f"urn:uuid:{uuid.uuid5(run_id, f'record-strings-{index}')}",
                        "@type": "uco-observable:ExtractedStringsFacet",
                        "uco-observable:strings": [
                            {
                                "@id": f"urn:uuid:{uuid.uuid5(run_id, f'record-string-{index}')}",
                                "@type": "uco-observable:ExtractedString",
                                "uco-observable:stringValue": record.text,
                            }
                        ],
                    }
                ],
            }
        )
        relationship_nodes.append(
            {
                "@id": f"urn:uuid:{uuid.uuid5(run_id, f'record-derivation-{index}')}",
                "@type": "uco-core:Relationship",
                "uco-core:name": f"Extracted record {index} derived from {file_name}",
                "uco-core:source": {"@id": record_id},
                "uco-core:target": {"@id": source_id},
                "uco-core:kindOfRelationship": "Derived_From",
                "uco-core:isDirectional": True,
            }
        )

    action_node = {
        "@id": action_id,
        "@type": "case-investigation:InvestigativeAction",
        "uco-core:name": f"Processed {file_kind} through case-uco MCP",
        "uco-action:startTime": {"@type": "xsd:dateTime", "@value": now_iso},
        "uco-action:endTime": {"@type": "xsd:dateTime", "@value": now_iso},
        "uco-action:object": {"@id": source_id},
        "uco-action:instrument": {"@id": tool_id},
        "uco-action:result": record_refs,
    }

    return {
        "@context": {
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        },
        "@graph": [source_node, tool_node, action_node, *record_nodes, *relationship_nodes],
    }


def sanitize_text(value: str) -> str:
    cleaned = "".join(ch if ch.isprintable() else " " for ch in value)
    cleaned = re.sub(r"\b(?:\d[ -]?){12,19}\b", "[redacted-number]", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:500]


def cli_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Process a local document into CASE/UCO JSON-LD.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--format", default="jsonld", choices=["jsonld"])
    parser.add_argument("--file-kind", choices=["receipt_image", "pdf", "office", "csv_table"])
    parser.add_argument("--upload-id")
    parser.add_argument("--progress-output")
    args = parser.parse_args(argv)
    try:
        result = process_document_file(
            args.input,
            args.output,
            file_kind=args.file_kind,
            safe_metadata={"upload_id": args.upload_id} if args.upload_id else None,
            progress_output=args.progress_output,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "output_graph_path": str(result.output_path),
                "extracted_content_path": (
                    str(result.extracted_content_path) if result.extracted_content_path else None
                ),
                "annotations_path": str(result.annotations_path) if result.annotations_path else None,
                "tool_name": TOOL_NAME,
                "tool_version": TOOL_VERSION,
                "file_kind": result.file_kind,
                "record_count": len(result.records),
                "truncated": result.truncated,
                "validation_status": "valid",
                "safe_summary": (
                    f"Processed {result.file_kind} into CASE/UCO JSON-LD "
                    f"({len(result.records)} record{'s' if len(result.records) != 1 else ''})."
                ),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
