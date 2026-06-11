---
name: image-to-case-uco
description: Process image files into validated CASE/UCO or CAC knowledge graphs. Use when the user provides images, receipts, screenshots, scans, photos, OCR output, or asks to convert an image file into CASE/UCO/CAC JSON-LD.
---

# Image To CASE/UCO

## Workflow

1. Identify the image artifact:
   - Record file path, file name, extension, MIME type, byte size, dimensions, and SHA256.
   - Model the source image as `ObservableObject` with `FileFacet` and `ContentDataFacet`.
   - Use `ContentDataFacet(hash=[Hash(hash_method=["SHA256"], hash_value=...)])`.

2. Extract text:
   - Prefer a real OCR engine when available (`tesseract`, cloud OCR, or an application OCR service).
   - If OCR is unavailable and the image is visible in the prompt, use vision-assisted transcription and mark that method in the graph.
   - Preserve raw OCR text with `ExtractedStringsFacet(strings=[ExtractedString(...)])` on the source image observable.

3. Analyze the content:
   - Parse domain facts from OCR text, such as receipt totals, timestamps, merchant names, addresses, line items, payment methods, identifiers, or account fragments.
   - Keep uncertain values in annotations or descriptions; do not overstate them as verified facts.
   - Redact or preserve masked values as they appear. Never infer full payment card numbers, personal identifiers, or secrets from partial values.

4. Map to ontologies with the CASE/UCO MCP:
   - Always read the MCP tool schema before calling a tool.
   - Use `search_classes`, `find_classes_for_domain`, `guide_mapping`, and `get_class_details` to select classes.
   - Use existing UCO/CASE/CAC classes first. If no adequate class exists, model source evidence plus extracted attributes using `Event`, `Annotation`, `Dictionary`, or a documented local extension rather than inventing unvalidated terms.

5. Serialize:
   - Use `CASEGraph` and generated classes where possible.
   - Use UUID-ending IRIs so `case_validate` does not emit identifier info findings.
   - For receipt-like images, a good baseline is:
     - Source image: `ObservableObject` + `FileFacet` + `ContentDataFacet` + `ExtractedStringsFacet`
     - Merchant: `Organization`
     - Address: `Location` + `SimpleAddressFacet`
     - Payment card fragment: `PaymentCard` plus a conservative description or `AccountFacet(account_identifier=masked_value)`
     - Transaction facts: `Event` with `event_context` references and `event_attribute=[ProperDictionary(...)]`
     - Processing provenance: `InvestigativeAction` with `instrument=[Tool(...)]`, `object=[source_image]`, and `result=[derived_event]`

6. Validate before reporting success:
   - Run `case_validate --built-version case-1.4.0 output.jsonld`.
   - If validation fails, fix the graph and re-run validation.
   - Do not call the graph complete until validation reports `Conforms: True`.

## Receipt Example Pattern

Use this shape for point-of-sale receipts:

```python
from case_uco import CASEGraph
from case_uco.uco.observable import ObservableObject, FileFacet, ContentDataFacet, ExtractedStringsFacet, ExtractedString
from case_uco.uco.types import Hash, ProperDictionary, DictionaryEntry
from case_uco.uco.core import Event

graph = CASEGraph(kb_prefix="https://example.org/kb/receipt/")

receipt_image = graph.create(
    ObservableObject,
    has_facet=[
        FileFacet(file_name=[file_name], file_path=[file_path], size_in_bytes=size),
        ContentDataFacet(hash=[Hash(hash_method=["SHA256"], hash_value=sha256)], mime_type=[mime], size_in_bytes=size),
        ExtractedStringsFacet(strings=[ExtractedString(string_value=ocr_text, encoding="UTF-8", language="eng")]),
    ],
)

facts = ProperDictionary(entry=[
    DictionaryEntry(key="receipt.check_number", value="322430"),
    DictionaryEntry(key="payment.amount_usd", value="27.81"),
])

graph.create(
    Event,
    name="Point-of-sale transaction",
    event_type=["point-of-sale purchase", "receipt transaction"],
    event_context=[receipt_image],
    event_attribute=[facts],
)
```

## Validation Pitfalls

- Use `SHA256`, not `SHA-256`, for `HashNameVocab`.
- Avoid non-vocabulary values in controlled vocabulary fields unless an informational finding is acceptable for a draft. For final examples, prefer descriptions or dictionary attributes.
- `case_validate` may report info findings for non-UUID IRIs. Use identifiers ending in UUIDs for clean conformance.
- If a graph instantiates extension classes, validate with the extension ontology and shapes using `--ontology-graph`, `--inference rdfs`, and `--allow-info` when appropriate.
