# R1 Implementation Status

R1 is being delivered incrementally.

This first bounded slice changes only the supported local/reference bootstrap defaults for public credentialless collection and the corresponding tests/documentation. Broader readiness classification in the canonical UI, Administration IA, source lifecycle improvements and cross-workspace integration remain later bounded slices.

Current repository-controlled change:

- enable the live connector scheduler in `.env.example` for local/reference use;
- keep credentialless CISA KEV available through the built-in scheduler baseline;
- enable CIRCL Vulnerability-Lookup by default;
- keep OpenCVE and credential-bearing external framework integrations disabled until configured;
- preserve all existing security and evidence boundaries.
