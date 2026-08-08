# Third-party Software and Content Policy

DTMO depends on external software and is designed to integrate with external intelligence and vulnerability-data providers. The project licence does not replace the licences or terms governing those materials.

## Software dependencies

The dependency declarations in `pyproject.toml`, container manifests and frontend manifests are the source inventory for release engineering. Dependencies may use Apache-2.0, MIT, BSD, LGPL or other licences; their actual licence and notice requirements must be verified from the specific version distributed or deployed.

This document deliberately does not assert a licence for each dependency without version-specific evidence. A production release should generate an SBOM and licence inventory from the locked or resolved dependency set and retain that evidence with the release.

## External services and data

Connectors may consume CVE/NVD data, vendor advisories, public threat intelligence, historical incident reporting and other OSINT. Each provider may impose separate API, rate-limit, attribution, copyright, database-right, redistribution or commercial-use conditions.

Connector acceptance therefore requires provider-specific evidence, including where relevant:

- source and provider identity;
- applicable licence or terms URL/version/date;
- permitted use and redistribution boundaries;
- attribution requirements;
- credential and rate-limit constraints;
- retention or deletion obligations;
- confidence and provenance fields retained by DTMO.

A technically successful connector does not establish legal permission to redistribute provider content.

## Trademarks

Third-party names, logos and marks remain the property of their respective owners. Their presence in DTMO should be descriptive and must not imply endorsement.

## Release gate

Where licence compatibility or redistribution rights are uncertain, the affected component or content remains blocked from public distribution until reviewed. That legal/content gate is independent from CI success and from technical production-readiness evidence.
