from dtmo.ncsc_csaf_adapter import CSAFAdapterError, parse_csaf_document, parse_csaf_index
from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import SourceExecutionError, _parse_rss


def test_ncsc_rss_catalog_source_is_executable() -> None:
    source = catalog_by_id("ncsc-nl-advisories-rss")
    assert source is not None
    assert source.execution_profile == "rss-2.0"
    assert source.execution_status == "supported"
    assert source.endpoint_url.startswith("https://advisories.ncsc.nl/")


def test_ncsc_rss_parser_normalizes_advisory_and_preserves_raw_provenance() -> None:
    payload = b"""<?xml version='1.0' encoding='UTF-8'?>
    <rss version='2.0'><channel><title>NCSC-NL</title><item>
      <guid>https://advisories.ncsc.nl/advisory?id=NCSC-2026-0001</guid>
      <title>NCSC-2026-0001 voorbeeldadvies</title>
      <link>https://advisories.ncsc.nl/advisory?id=NCSC-2026-0001</link>
      <description>Beveiligingsadvies met mitigerende maatregelen.</description>
      <pubDate>Tue, 11 Aug 2026 06:00:00 GMT</pubDate>
    </item></channel></rss>"""
    records = _parse_rss(payload, "authoritative")
    assert len(records) == 1
    record = records[0]
    assert record.external_id.endswith("NCSC-2026-0001")
    assert record.object_type == "security-advisory"
    assert record.source_reliability == "authoritative"
    assert record.confidence == 92
    assert record.raw["title"] == "NCSC-2026-0001 voorbeeldadvies"


def test_rss_parser_fails_closed_on_invalid_or_empty_payload() -> None:
    for payload in (b"not xml", b"<rss><channel></channel></rss>"):
        try:
            _parse_rss(payload, "authoritative")
        except SourceExecutionError:
            pass
        else:
            raise AssertionError("malformed/empty RSS must fail closed")


def test_ncsc_csaf_catalog_source_is_executable() -> None:
    source = catalog_by_id("ncsc-nl-advisories")
    assert source is not None
    assert source.execution_profile == "csaf-2.0"
    assert source.execution_status == "supported"
    assert source.endpoint_url == "https://advisories.ncsc.nl/csaf/"


def test_ncsc_csaf_index_is_bounded_and_path_restricted() -> None:
    payload = "\n".join(f"2026/ncsc-2026-{index:04d}.json" for index in range(1, 40)).encode()
    paths = parse_csaf_index(payload)
    assert len(paths) == 25
    assert paths[0] == "2026/ncsc-2026-0001.json"
    try:
        parse_csaf_index(b"https://evil.example/advisory.json")
    except CSAFAdapterError:
        pass
    else:
        raise AssertionError("absolute or cross-origin CSAF index entries must fail closed")


def test_ncsc_csaf_document_normalizes_and_retains_raw_payload() -> None:
    payload = {
        "document": {
            "title": "Kwetsbaarheden verholpen in Example Product",
            "tracking": {
                "id": "NCSC-2026-0280",
                "initial_release_date": "2026-08-07T09:00:00Z",
            },
            "notes": [
                {
                    "category": "summary",
                    "title": "Omschrijving",
                    "text": "De leverancier heeft kwetsbaarheden verholpen.",
                }
            ],
        },
        "vulnerabilities": [{"cve": "CVE-2026-12345"}],
    }
    record = parse_csaf_document(
        payload,
        reliability="authoritative",
        document_url="https://advisories.ncsc.nl/csaf/v2/2026/ncsc-2026-0280.json",
    )
    assert record.external_id == "NCSC-2026-0280"
    assert record.object_type == "security-advisory"
    assert record.confidence == 96
    assert record.summary.startswith("De leverancier")
    assert record.raw == payload


def test_ncsc_csaf_document_fails_closed_without_tracking_identity() -> None:
    try:
        parse_csaf_document(
            {"document": {"title": "Missing identity", "tracking": {}}},
            reliability="authoritative",
            document_url="https://advisories.ncsc.nl/csaf/v2/2026/missing.json",
        )
    except CSAFAdapterError:
        pass
    else:
        raise AssertionError("CSAF documents without tracking identity must fail closed")
