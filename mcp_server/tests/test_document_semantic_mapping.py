"""Tier T0 tests for deterministic document semantic mapping."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from document_semantic_mapping import extract_semantic_entities

SYNTHETIC_ARTICLE = """
11/06/2026, 20:06
38-Year-Old Riverton Man Charged With Online Solicitation

RIVERton — The Maryland State Police Internet Crimes Against Children Task Force
announced that a 38-year-old Riverton man was charged with sexual solicitation
after an investigation into online activity. Officers executed a search warrant
at a residence in Riverton on DECEMBER 12, 2025.

Contact the task force at tips@example-agency.test or call (555) 010-2000.
More information: https://example-agency.test/icac/release-001
"""


def test_semantic_mapping_extracts_typed_entities_with_anchors() -> None:
    entities = extract_semantic_entities(SYNTHETIC_ARTICLE, run_seed="t0-article")
    classes = {entity.ontology_class for entity in entities}
    assert "uco-identity:Person" in classes
    assert "uco-location:Location" in classes
    assert "uco-identity:Organization" in classes
    assert "uco-core:Event" in classes
    assert "uco-observable:EmailAddress" in classes
    assert "uco-observable:PhoneAccount" in classes
    assert "uco-observable:URL" in classes

    for entity in entities:
        assert 0 <= entity.start < entity.end <= len(SYNTHETIC_ARTICLE)
        assert SYNTHETIC_ARTICLE[entity.start : entity.end] == entity.matched_text


def test_semantic_mapping_is_bounded_and_deterministic() -> None:
    first = extract_semantic_entities(SYNTHETIC_ARTICLE, run_seed="t0-article")
    second = extract_semantic_entities(SYNTHETIC_ARTICLE, run_seed="t0-article")
    assert first == second
    assert len(first) <= 48


FRAUD_CRYPTO_WARRANT_SNIPPET = """
| Groomer | Marcus Hale, aka "Coach Mike" | Telegram @northstar_mike_synth |
Apartment 4B, **1555 Oak Street, San Jose, California 95110**, including any computers
within the control of **Dylan Reyes** (DOB 1991-07-02, synthetic).
| Applying Agent | Special Agent Jordan Ellis, FBI |
"""


def test_semantic_mapping_extracts_warrant_markdown_anchors() -> None:
    entities = extract_semantic_entities(
        FRAUD_CRYPTO_WARRANT_SNIPPET,
        run_seed="fraud-crypto-warrant-t0",
    )
    classes = {entity.ontology_class for entity in entities}
    labels = {entity.label for entity in entities}
    assert "uco-identity:Person" in classes
    assert "uco-location:Location" in classes
    assert "uco-observable:InstantMessagingAddress" in classes
    assert any("Dylan Reyes" in label for label in labels)
    assert any("1555 Oak Street" in label for label in labels)
    assert any("Telegram @northstar_mike_synth" in label for label in labels)
    assert not any(label.startswith("Location THE UNITED") for label in labels)
    assert not any(label.startswith("Location the Matter") for label in labels)


FRAUD_CRYPTO_CHAT_LOG = """
[2026-01-04 09:12 UTC]
Coach Mike (@northstar_mike_synth): Welcome back — portfolio review today.
Marcus Hale (@northstar_mike_synth): Copy that.
Priya Sundaram (@priya_analyst_synth): Analyst notes attached below.
"""


FRAUD_CRYPTO_VICTIM_STATEMENT = """
| Role | Name |
| Victim | Eleanor Vance |
| Groomer | Marcus Hale, aka "Coach Mike" |
| Analyst | Priya Sundaram |
"""


FRAUD_CRYPTO_EXCHANGE_RECORDS = """
Account holder: Dylan Reyes
Registered user: Eleanor Vance
Exchange return notes for account DR-8812.
"""


def test_semantic_mapping_extracts_chat_speaker_display_names() -> None:
    entities = extract_semantic_entities(
        FRAUD_CRYPTO_CHAT_LOG,
        run_seed="fraud-crypto-chat-t0",
    )
    person_labels = [entity.label for entity in entities if entity.ontology_class == "uco-identity:Person"]
    im_labels = [
        entity.label
        for entity in entities
        if entity.ontology_class == "uco-observable:InstantMessagingAddress"
    ]
    assert any("Marcus Hale" in label for label in person_labels)
    assert any("Coach Mike" in label for label in person_labels)
    assert any("Priya Sundaram" in label for label in person_labels)
    assert any("@northstar_mike_synth" in label for label in im_labels)
    assert any("@priya_analyst_synth" in label for label in im_labels)


def test_semantic_mapping_extracts_role_table_persons() -> None:
    entities = extract_semantic_entities(
        FRAUD_CRYPTO_VICTIM_STATEMENT,
        run_seed="fraud-crypto-victim-t0",
    )
    person_labels = [entity.label for entity in entities if entity.ontology_class == "uco-identity:Person"]
    assert any("Eleanor Vance" in label for label in person_labels)
    assert any("Marcus Hale" in label and "Coach Mike" in label for label in person_labels)
    assert any("Priya Sundaram" in label for label in person_labels)


def test_semantic_mapping_extracts_exchange_account_holders() -> None:
    entities = extract_semantic_entities(
        FRAUD_CRYPTO_EXCHANGE_RECORDS,
        run_seed="fraud-crypto-exchange-t0",
    )
    person_labels = [entity.label for entity in entities if entity.ontology_class == "uco-identity:Person"]
    assert any("Dylan Reyes" in label for label in person_labels)
    assert any("Eleanor Vance" in label for label in person_labels)
