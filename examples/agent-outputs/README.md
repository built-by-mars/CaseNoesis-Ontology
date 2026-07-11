# Agent-Produced Worked Examples

Complete worked examples produced by an AI agent using this SDK and its MCP
server (moved here from the former top-level `example_agentmcp_outputs/`
directory in v1.19.0). Each example pairs the Python source that builds the
graph with the validated JSON-LD output.

| Example | What it demonstrates |
|---------|---------------------|
| `wifi_capture.py` / `.jsonld` | Three-layer network investigation — acquisition (Wireshark capture), observed network (17 TCP flows, DNS chains, IPv6), and analysis layer (5 service attributions with confidence scores) |
| `cellbrite_samsung_extraction.py` / `.jsonld` | Mobile device forensics — Cellebrite extraction with WhatsApp messages, GPS locations, app artifacts, and device metadata |
| `field_office_custody.py` / `.jsonld` | Chain of custody — evidence transfer from a field office with provenance records and handling documentation |
| `usn_journal_example.py` / `.jsonld` | Windows USN Journal — four NTFS change entries (create, modify, rename, delete) with structured reason flags, directory hierarchy, rename before/after modeling, and forensic provenance |

Rebuild any example with the project virtualenv and re-validate:

```bash
.venv/bin/python examples/agent-outputs/wifi_capture.py
case_validate --built-version case-1.4.0 examples/agent-outputs/wifi_capture.jsonld
```
