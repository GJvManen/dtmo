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
