"""Tests for the canonical-term document processor (Tier T0 synthetic data)."""

import json
import struct
import sys
import zlib
import zipfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import document_processor
from document_processor import (
    MAX_CSV_RECORDS,
    ocr_available,
    process_document_file,
)


def write_png_with_text(path: Path, text: str) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    raw = b"\x00\xff\xff\xff"
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        + chunk(b"tEXt", b"Receipt\x00" + text.encode("latin-1"))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def write_plain_png(path: Path) -> None:
    """PNG with no tEXt chunk — no embedded text to extract."""

    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    raw = b"\x00\xff\xff\xff"
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def write_pdf(path: Path) -> None:
    path.write_text(
        "%PDF-1.4\n1 0 obj <<>> stream\nBT (Synthetic PDF invoice total 23.45) Tj ET\nendstream\nendobj\n%%EOF\n",
        encoding="latin-1",
    )


def write_flate_pdf(path: Path) -> None:
    """PDF whose only text lives inside a Flate-compressed content stream."""

    content = zlib.compress(b"BT (Synthetic compressed-stream invoice total 99.10) Tj ET")
    path.write_bytes(
        b"%PDF-1.4\n1 0 obj << /Filter /FlateDecode >>\nstream\n"
        + content
        + b"\nendstream\nendobj\n%%EOF\n"
    )


def write_scanned_pdf(path: Path) -> None:
    """PDF with no extractable text strings (image-only / scanned shape)."""

    path.write_bytes(b"%PDF-1.4\n1 0 obj << /Subtype /Image >>\nstream\n\x00\x01\x02\nendstream\nendobj\n%%EOF\n")


def write_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr(
            "word/document.xml",
            "<w:document><w:body><w:p><w:r><w:t>Synthetic Office document item Alpha</w:t></w:r></w:p></w:body></w:document>",
        )


def write_xlsx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr(
            "xl/sharedStrings.xml",
            '<sst><si><t>Synthetic spreadsheet cell Bravo</t></si></sst>',
        )
        archive.writestr("xl/worksheets/sheet1.xml", "<worksheet><sheetData/></worksheet>")


def graph_nodes(output: Path) -> list[dict]:
    return json.loads(output.read_text(encoding="utf-8"))["@graph"]


def nodes_of_type(nodes: list[dict], type_name: str) -> list[dict]:
    return [node for node in nodes if node.get("@type") == type_name]


# ---------------------------------------------------------------------------
# Canonical graph shape (#102)
# ---------------------------------------------------------------------------


def test_graph_uses_canonical_action_provenance_terms(tmp_path: Path) -> None:
    source = tmp_path / "receipt.png"
    write_png_with_text(source, "Synthetic receipt total 12.34")
    output = tmp_path / "receipt.jsonld"
    process_document_file(source, output, safe_metadata={"upload_id": "synthetic-upload-1"})

    raw = output.read_text(encoding="utf-8")
    # Invented predicates from v0.1.0 must be gone.
    assert "case-investigation:object" not in raw
    assert "case-investigation:instrument" not in raw
    assert "case-investigation:result" not in raw
    assert "link-look:" not in raw

    nodes = graph_nodes(output)
    actions = nodes_of_type(nodes, "case-investigation:InvestigativeAction")
    assert len(actions) == 1
    action = actions[0]
    assert action["uco-action:object"]["@id"]
    assert action["uco-action:instrument"]["@id"]
    assert action["uco-action:result"], "action must reference extracted records"
    assert action["uco-action:startTime"]["@type"] == "xsd:dateTime"


def test_source_node_carries_file_and_hash_facets(tmp_path: Path) -> None:
    source = tmp_path / "receipt.png"
    write_png_with_text(source, "Synthetic receipt total 12.34")
    output = tmp_path / "receipt.jsonld"
    result = process_document_file(source, output)

    nodes = graph_nodes(output)
    sources = nodes_of_type(nodes, "uco-observable:RasterPicture")
    assert len(sources) == 1
    facets = sources[0]["uco-core:hasFacet"]
    file_facets = [f for f in facets if f["@type"] == "uco-observable:FileFacet"]
    content_facets = [f for f in facets if f["@type"] == "uco-observable:ContentDataFacet"]
    assert file_facets[0]["uco-observable:fileName"] == "receipt.png"
    assert file_facets[0]["uco-observable:extension"] == "png"
    hash_node = content_facets[0]["uco-observable:hash"][0]
    assert hash_node["@type"] == "uco-types:Hash"
    # Plain xsd:string per UCO 1.4.0+ guidance (typed vocab literal warns).
    assert hash_node["uco-types:hashMethod"] == "SHA256"
    assert hash_node["uco-types:hashValue"]["@value"] == result.sha256.upper()


def test_tool_node_uses_canonical_version_property(tmp_path: Path) -> None:
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\n", encoding="utf-8")
    output = tmp_path / "table.jsonld"
    process_document_file(source, output)

    tools = nodes_of_type(graph_nodes(output), "uco-tool:Tool")
    assert len(tools) == 1
    assert tools[0]["uco-tool:version"] == document_processor.TOOL_VERSION


def test_records_carry_extracted_strings_facets_and_relationships(tmp_path: Path) -> None:
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\nbravo,56.78\n", encoding="utf-8")
    output = tmp_path / "table.jsonld"
    result = process_document_file(source, output)

    assert len(result.records) == 2
    nodes = graph_nodes(output)
    observables = nodes_of_type(nodes, "uco-observable:ObservableObject")
    record_nodes = [n for n in observables if n.get("uco-core:hasFacet")
                    and any(f["@type"] == "uco-observable:ExtractedStringsFacet" for f in n["uco-core:hasFacet"])]
    assert len(record_nodes) == 2
    strings_facet = record_nodes[0]["uco-core:hasFacet"][0]
    assert strings_facet["uco-observable:strings"][0]["@type"] == "uco-observable:ExtractedString"
    assert "item=alpha" in strings_facet["uco-observable:strings"][0]["uco-observable:stringValue"]

    relationships = nodes_of_type(nodes, "uco-core:Relationship")
    assert len(relationships) == 2
    assert relationships[0]["uco-core:kindOfRelationship"] == "Derived_From"
    record_ids = {n["@id"] for n in record_nodes}
    assert relationships[0]["uco-core:source"]["@id"] in record_ids


# ---------------------------------------------------------------------------
# Extraction breadth and honest failure (#103)
# ---------------------------------------------------------------------------


def test_csv_yields_bounded_per_record_candidates(tmp_path: Path) -> None:
    rows = "\n".join(f"row-{i},{i}.00" for i in range(1, MAX_CSV_RECORDS + 51))
    source = tmp_path / "big.csv"
    source.write_text("item,total\n" + rows + "\n", encoding="utf-8")
    output = tmp_path / "big.jsonld"
    result = process_document_file(source, output)

    assert len(result.records) == MAX_CSV_RECORDS
    assert result.truncated is True
    assert result.extracted_fields["truncated"].startswith(f"first {MAX_CSV_RECORDS}")


def test_empty_csv_fails_honestly(tmp_path: Path) -> None:
    source = tmp_path / "empty.csv"
    source.write_text("item,total\n", encoding="utf-8")
    with pytest.raises(ValueError, match="empty_csv"):
        process_document_file(source, tmp_path / "out.jsonld")


def test_flate_compressed_pdf_text_is_extracted(tmp_path: Path) -> None:
    source = tmp_path / "compressed.pdf"
    write_flate_pdf(source)
    output = tmp_path / "compressed.jsonld"
    result = process_document_file(source, output)
    assert "compressed-stream invoice" in result.extracted_fields["extracted_text"]


def test_scanned_pdf_without_text_fails_honestly(tmp_path: Path) -> None:
    source = tmp_path / "scanned.pdf"
    write_scanned_pdf(source)
    with pytest.raises(ValueError, match="pdf_text_missing"):
        process_document_file(source, tmp_path / "out.jsonld")


def test_xlsx_shared_strings_are_extracted(tmp_path: Path) -> None:
    source = tmp_path / "sheet.xlsx"
    write_xlsx(source)
    output = tmp_path / "sheet.jsonld"
    result = process_document_file(source, output)
    assert "Synthetic spreadsheet cell Bravo" in result.extracted_fields["extracted_text"]


def test_office_without_text_fails_honestly(tmp_path: Path) -> None:
    source = tmp_path / "blank.docx"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr("word/document.xml", "<w:document><w:body/></w:document>")
    with pytest.raises(ValueError, match="office_text_missing"):
        process_document_file(source, tmp_path / "out.jsonld")


def test_image_without_embedded_text_fails_honestly_without_ocr(tmp_path: Path, monkeypatch) -> None:
    """No OCR engine: never emit placeholder 'Synthetic image file' content."""

    monkeypatch.setattr(document_processor.shutil, "which", lambda _name: None)
    source = tmp_path / "photo.jpg"
    source.write_bytes(b"\xff\xd8\xff\xe0synthetic-jpeg-bytes")
    with pytest.raises(ValueError, match="ocr_unavailable"):
        process_document_file(source, tmp_path / "out.jsonld")


def test_no_placeholder_content_in_output(tmp_path: Path) -> None:
    source = tmp_path / "receipt.png"
    write_png_with_text(source, "Synthetic receipt total 12.34")
    output = tmp_path / "receipt.jsonld"
    process_document_file(source, output)
    raw = output.read_text(encoding="utf-8")
    assert "Synthetic image file" not in raw


@pytest.mark.skipif(not ocr_available(), reason="tesseract OCR CLI not installed")
def test_image_ocr_extracts_text_when_available(tmp_path: Path) -> None:
    """Live OCR path: a plain PNG goes through tesseract (may yield empty)."""

    source = tmp_path / "plain.png"
    write_plain_png(source)
    try:
        result = process_document_file(source, tmp_path / "out.jsonld")
    except ValueError as exc:
        # A 1x1 image legitimately has no recognizable text.
        assert str(exc) == "no_extractable_content"
    else:
        assert result.extracted_fields["extraction_method"] == "ocr_tesseract"


def test_unsupported_kind_fails_honestly(tmp_path: Path) -> None:
    source = tmp_path / "binary.exe"
    source.write_bytes(b"MZ")
    with pytest.raises(ValueError, match="unsupported_file_kind"):
        process_document_file(source, tmp_path / "out.jsonld")


def test_oversized_source_fails_honestly(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(document_processor, "MAX_BYTES", 16)
    source = tmp_path / "table.csv"
    source.write_text("item,total\nalpha,12.34\n", encoding="utf-8")
    with pytest.raises(ValueError, match="source_oversized"):
        process_document_file(source, tmp_path / "out.jsonld")


# ---------------------------------------------------------------------------
# Progress contract (unchanged)
# ---------------------------------------------------------------------------


def test_process_document_file_emits_safe_progress_checkpoints(tmp_path: Path) -> None:
    source = tmp_path / "receipt.png"
    output = tmp_path / "receipt.jsonld"
    progress = tmp_path / "progress.jsonl"
    write_png_with_text(source, "Synthetic receipt total 12.34")

    process_document_file(source, output, progress_output=progress)

    events = [
        json.loads(line)
        for line in progress.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    stages = [event["stage"] for event in events]
    assert stages == [
        "started",
        "inspect_source",
        "extract_content",
        "build_graph",
        "write_graph",
        "completed",
    ]
    assert events[-1]["percent"] == 100
    serialized = json.dumps(events)
    assert str(source) not in serialized
    assert "12.34" not in serialized
    assert "Synthetic receipt total" not in serialized


def test_process_document_file_emits_safe_failure_checkpoint(tmp_path: Path) -> None:
    progress = tmp_path / "progress.jsonl"
    missing_source = tmp_path / "missing.pdf"

    with pytest.raises(ValueError, match="source_missing"):
        process_document_file(missing_source, tmp_path / "out.jsonld", progress_output=progress)

    events = [
        json.loads(line)
        for line in progress.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert events[-1]["stage"] == "failed"
    assert events[-1]["percent"] == 100
    assert str(missing_source) not in json.dumps(events)
