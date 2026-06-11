import json
import struct
import sys
import zlib
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from document_processor import process_document_file


def write_png_with_text(path: Path, text: str) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(kind + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", crc)

    raw = b"\x00\xff\xff\xff"
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
        + chunk(b"tEXt", b"Receipt\x00Synthetic receipt total 12.34")
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


def write_pdf(path: Path) -> None:
    path.write_text(
        "%PDF-1.4\n1 0 obj <<>> stream\nBT (Synthetic PDF invoice total 23.45) Tj ET\nendstream\nendobj\n%%EOF\n",
        encoding="latin-1",
    )


def write_docx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types></Types>")
        archive.writestr(
            "word/document.xml",
            "<w:document><w:body><w:t>Synthetic Office document item Alpha</w:t></w:body></w:document>",
        )


def test_process_live_acceptance_file_types(tmp_path: Path) -> None:
    fixtures = [
        ("receipt.png", lambda path: write_png_with_text(path, "Synthetic receipt total 12.34"), "receipt_image"),
        ("document.pdf", lambda path: write_pdf(path), "pdf"),
        ("document.docx", lambda path: write_docx(path), "office"),
        ("table.csv", lambda path: path.write_text("item,total\nalpha,12.34\n", encoding="utf-8"), "csv_table"),
    ]

    for name, writer, expected_kind in fixtures:
        source = tmp_path / name
        writer(source)
        output = tmp_path / f"{name}.jsonld"
        result = process_document_file(source, output)
        assert result.file_kind == expected_kind
        assert output.exists()
        doc = json.loads(output.read_text(encoding="utf-8"))
        graph = doc["@graph"]
        assert any(node.get("@type") == "case-investigation:InvestigativeAction" for node in graph)
        assert any(node.get("@type") == "uco-tool:Tool" for node in graph)
        assert any(node.get("@type") == "uco-core:UcoObject" for node in graph)


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

    try:
        process_document_file(missing_source, tmp_path / "out.jsonld", progress_output=progress)
    except ValueError as exc:
        assert str(exc) == "source_missing"
    else:
        raise AssertionError("missing source should fail")

    events = [
        json.loads(line)
        for line in progress.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert events[-1]["stage"] == "failed"
    assert events[-1]["percent"] == 100
    assert str(missing_source) not in json.dumps(events)
