#!/usr/bin/env python3
"""FOAF/ORG identity and roles exemplar for docs/recipes/foaf-org-identity-roles.md."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from case_uco import CASEGraph
from case_uco.case.investigation import Investigation
from case_uco.uco.core import Relationship
from case_uco.uco.identity import Identity, Person, SimpleNameFacet
from case_uco.uco.observable import AccountFacet, ObservableObject

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "foaf-org-identity.jsonld"

EXTRA_CONTEXT = {
    "foaf": "http://xmlns.com/foaf/0.1/",
    "org": "http://www.w3.org/ns/org#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}


def build() -> CASEGraph:
    graph = CASEGraph(extra_context=EXTRA_CONTEXT)
    tz = timezone.utc

    person_id = "kb:person-1"
    person = graph.create(
        Person,
        id=person_id,
        name="Alex Morgan (synthetic)",
        has_facet=[SimpleNameFacet(given_name=["Alex"], family_name=["Morgan"])],
    )
    graph.add_type(person_id, "foaf:Person")
    graph.add_property(person_id, "foaf:mbox", "mailto:alex.morgan@example.org")

    org_id = "kb:org-taskforce"
    org = graph.create(Identity, id=org_id, name="Regional ICAC Task Force (synthetic)")
    graph.add_type(org_id, "org:Organization")
    graph.add_type(org_id, "foaf:Organization")

    membership_id = "kb:membership-1"
    graph.upsert_node(
        membership_id,
        types="org:Membership",
        properties={
            "org:member": {"@id": person_id},
            "org:organization": {"@id": org_id},
            "org:role": "Digital forensic examiner",
        },
    )
    graph.add_property(org_id, "org:hasMembership", {"@id": membership_id})

    account_id = "kb:account-signal"
    account = graph.create(
        ObservableObject,
        id=account_id,
        name="Signal account (synthetic)",
        has_facet=[AccountFacet(account_identifier="+15551234567", is_active=True)],
    )
    graph.add_type(account_id, "foaf:OnlineAccount")
    graph.add_property(account_id, "foaf:accountName", "+15551234567")
    graph.add_property(person_id, "foaf:holdsAccount", {"@id": account_id})

    graph.create(
        Relationship,
        source=[person],
        target=org,
        kind_of_relationship="member-of",
        start_time=[datetime(2024, 1, 1, tzinfo=tz)],
        is_directional=True,
    )

    graph.create(
        Investigation,
        name="Synthetic case 2026-FOAF-001",
        description=[
            "Person, organization, membership, and account kept distinct.",
            "No owl:sameAs — uncertain attribution uses Relationship, not identity collapse.",
        ],
        object=[person, org, account],
    )
    return graph


def main() -> None:
    graph = build()
    graph.write(str(OUTPUT))
    print(f"wrote {OUTPUT} ({len(graph)} nodes)")


if __name__ == "__main__":
    main()
