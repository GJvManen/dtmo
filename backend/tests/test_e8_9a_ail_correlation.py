from __future__ import annotations

from dtmo.ail_correlation import correlate_ail_indicator


def test_correlates_exact_canonical_intelligence_without_fuzzy_inference() -> None:
    hits = correlate_ail_indicator(
        indicator_type="domain",
        indicator_value="login-example.test",
        candidates=[
            {
                "source_id": "vendor-feed",
                "external_id": "adv-1",
                "item_type": "advisory",
                "title": "login-example.test",
                "summary": "Credential phishing campaign",
                "tags": ["phishing"],
            },
            {
                "source_id": "vendor-feed",
                "external_id": "adv-2",
                "item_type": "advisory",
                "title": "login-example.test.evil",
                "summary": "near match must not correlate",
            },
        ],
    )

    assert len(hits) == 1
    assert hits[0].relation == "canonical_exact_match"
    assert hits[0].external_id == "adv-1"


def test_correlates_misp_attribute_and_object_attribute_without_returning_raw_content() -> None:
    hits = correlate_ail_indicator(
        indicator_type="domain",
        indicator_value="login-example.test",
        candidates=[
            {
                "source_id": "misp",
                "external_id": "event-uuid",
                "item_type": "cti_event",
                "title": "Credential campaign",
                "raw": {
                    "secret_note": "must never be projected",
                    "_dtmo_misp": {
                        "attributes": [
                            {"uuid": "attribute-uuid", "type": "domain", "value": "login-example.test"}
                        ],
                        "objects": [
                            {
                                "uuid": "object-uuid",
                                "name": "network-connection",
                                "attributes": [
                                    {"uuid": "object-attribute-uuid", "type": "domain", "value": "login-example.test"}
                                ],
                            }
                        ],
                    },
                },
            }
        ],
    )

    assert {hit.relation for hit in hits} == {"misp_attribute", "misp_object_attribute"}
    projected = [hit.context for hit in hits]
    assert all("secret_note" not in str(context) for context in projected)
    assert any(context.get("object_uuid") == "object-uuid" for context in projected)


def test_correlates_vulnerability_identifier_and_preserves_bounded_product_context() -> None:
    hits = correlate_ail_indicator(
        indicator_type="cve",
        indicator_value="CVE-2026-12345",
        candidates=[
            {
                "source_id": "opencve",
                "external_id": "CVE-2026-12345",
                "item_type": "vulnerability",
                "title": "CVE-2026-12345",
                "metadata": {
                    "cve_id": "CVE-2026-12345",
                    "vendor": "Example Vendor",
                    "product": "Example Product",
                },
            }
        ],
    )

    relations = {hit.relation for hit in hits}
    assert "canonical_exact_match" in relations
    assert "vulnerability_identifier" in relations
    vuln_hit = next(hit for hit in hits if hit.relation == "vulnerability_identifier")
    assert vuln_hit.context == {
        "cve_id": "CVE-2026-12345",
        "vendor": "Example Vendor",
        "product": "Example Product",
    }


def test_ail_source_items_are_not_self_correlated() -> None:
    hits = correlate_ail_indicator(
        indicator_type="ip",
        indicator_value="203.0.113.10",
        candidates=[
            {
                "source_id": "ail",
                "external_id": "ip:None:203.0.113.10",
                "item_type": "indicator",
                "title": "203.0.113.10",
            }
        ],
    )
    assert hits == []


def test_requires_non_empty_indicator_value() -> None:
    try:
        correlate_ail_indicator(indicator_type="domain", indicator_value="   ", candidates=[])
    except ValueError as exc:
        assert "indicator value is required" in str(exc)
    else:
        raise AssertionError("expected ValueError")
