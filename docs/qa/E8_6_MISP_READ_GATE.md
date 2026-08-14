# E8.6 MISP Read Integration Gate

## Decision objective

The E8.6 gate proves that the optional MISP adapter is read-only, bounded, secret-safe and preserves the source restrictions and CTI structure required for later governed use.

## Repository acceptance criteria

The dedicated `E8 MISP Read Integration Gate` must run on the exact pull-request head and pass all of the following:

1. fetch uses only `POST /events/restSearch` for this slice;
2. the API key is sent from runtime settings in the MISP `Authorization` header and is not embedded in evidence;
3. the requested event count is bounded by `DTMO_MISP_EVENT_LIMIT`;
4. event UUID/source/time/organisation metadata is preserved;
5. attributes/IOCs and their UUID/type/category/value/`to_ids`/time metadata are preserved;
6. MISP objects, object attributes and object references are preserved;
7. tags, TLP tags, galaxies and galaxy clusters are preserved;
8. event/attribute/object distribution and sharing-group metadata is retained;
9. imported evidence states that incoming restrictions are authoritative and that import does not authorize external sharing;
10. `cti_event` remains a canonical DTMO type instead of falsely coercing all MISP events into campaign/incident/indicator semantics;
11. production configuration rejects an enabled MISP connector without HTTPS and a runtime API key;
12. Ruff, mypy and compile checks succeed for the bounded slice.

## Explicit non-claims

A PASS is repository evidence only. It does not establish live connectivity to any MISP instance, production deployment, completeness/freshness of a real MISP dataset, validity of a particular external API key, owner acceptance, independent assurance, pentest acceptance or permission to redistribute imported intelligence.

No E8.7 write/share capability is accepted by this gate.
