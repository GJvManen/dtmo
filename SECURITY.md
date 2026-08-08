# DTMO Security Policy

DTMO is a cybersecurity platform and security reports are handled as sensitive operational information.

## Supported versions

See `SUPPORTED_VERSIONS.md`. Until the first production release, only the current `main` branch and an explicitly identified release-candidate branch are considered for security fixes.

## Reporting a vulnerability

Do not publish exploitable vulnerability details, credentials, personal data, operational secrets, private indicators or other sensitive evidence in a public issue or pull request.

Use GitHub Private Vulnerability Reporting / Security Advisories for this repository when available. If that channel is unavailable, contact the repository owner through a private channel listed on the owner's GitHub profile and provide only the minimum information needed to establish a secure reporting channel.

A useful report includes:

- affected revision or release;
- affected component and deployment assumptions;
- impact and realistic attack preconditions;
- reproducible steps or a minimal proof of concept;
- relevant logs or evidence with secrets and personal data removed;
- suggested remediation when known.

## Handling principles

Security work must preserve DTMO's existing governance boundaries: least privilege, RBAC, separation of review from share approval, immutable provenance where required, privacy minimisation and explicit human publication approval. A successful connector, recovery or automated test must never imply authority to publish intelligence.

Public disclosure should occur only after a fix or mitigation is available and disclosure timing has been coordinated with affected maintainers or vendors where appropriate.

## Scope boundaries

This policy does not authorize testing against third-party systems, schools, vendors, data providers or infrastructure. Researchers must only test systems they own or have explicit permission to assess.
