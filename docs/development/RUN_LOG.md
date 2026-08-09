# DTMO Continuous Development Run Log

This file is the chronological audit record for continuous development runs. Detailed run records are stored under `docs/development/runs/`.

## Runs

- [RUN-20260809-110 — RC9.9 manual/non-automatable WCAG 2.2 AA critical-journey review](runs/RUN-20260809-110.md) — `BLOCKED`: criterion-level review of the four accepted critical surfaces found `A11Y-001`: asynchronous principal/session resolution changes identity/role text and reveals RBAC-governed controls without live/status semantics; measured contrast, 200% resize, 320 CSS px reflow, text-spacing, full focus-order and genuine VoiceOver/NVDA evidence also remain explicitly unevidenced.
- [RUN-20260809-109 — RC9.8 exact-head acceptance](runs/RUN-20260809-109.md) — `PASS`: PR #65 exact head `34d2cce17372843cb51229648d1e5e62a66e4c04` passed all 27 registered workflows; retained artifact `9038468839` (`sha256:c0ded460c73d6c10c8bb61fb4334711ef9f2723924034337b3b7a828b01eb97a`) independently proved the bounded automated accessibility subset across all four accepted critical surfaces with 1/1 JUnit test passing, real backend-session RBAC calls, preserved human share approval and no product-wide WCAG/assistive-technology certification claim; merged as `5ca5c5e2cffde0700dde8b5aabd6ee3940f1b9c8`.
- [RUN-20260809-108 — RC9.8 WCAG 2.2 AA critical-journey gate](runs/RUN-20260809-108.md) — `CI_VALIDATION_PENDING`: added one bounded Chromium accessibility gate across the accepted share-approval, analyst-search, CISO-revocation and auditor-read-only surfaces; validates document language/title, landmark/heading structure, duplicate IDs, image alternatives, accessible control names, keyboard focusability and visible focus; exact-head CI and retained accessibility evidence are required before PASS, and no product-wide WCAG certification is claimed.
- [RUN-20260809-107 — RC9.7 exact-head acceptance](runs/RUN-20260809-107.md) — `PASS`: PR #63 exact head `6da6f5b6d2e65c7b6be99697f564eb76d5d1ec51` passed all 26 registered workflows; retained artifact `9038307443` (`sha256:fab6f3c93359cb5f3effd363bbb86c99dc632a5c6b3a78f006ad5e07f92d1d86`) independently proved Chromium, Firefox and WebKit execution across all four accepted critical surfaces, with 3/3 JUnit cases passing, real backend-session RBAC calls and preserved human share approval; merged as `1e886ac3fbb1d6711a7bfe191aeaff919d648451`.
- [RUN-20260809-106 — RC9.7 supported-browser critical-journey gate](runs/RUN-20260809-106.md) — `CI_VALIDATION_PENDING`: added one bounded Playwright compatibility gate across Chromium, Firefox and WebKit for the accepted share-approval, analyst-search, CISO-revocation and auditor-read-only journeys; real backend-session RBAC is preserved, business-operation calls are synthetic, and exact-head CI plus retained browser evidence are required before PASS.
- [RUN-20260809-105 — RC9.6 exact-head acceptance](runs/RUN-20260809-105.md) — `PASS`: PR #61 exact head `7e75f45fca15dc11be3a3c10d2d26797bdcdf92a` passed all 25 registered workflows; retained artifact `9038042763` (`sha256:9a0f218d68ea82a6cd564c923e8b5e90ec6550a43de853999faee87be8bfa62c`) independently proved responsive usability across 360×800, 768×1024 and 1440×900 viewports for all four accepted critical surfaces, with no blocking horizontal overflow, viewport-contained controls, minimum 24 px control dimensions, real backend-derived RBAC and no business mutations; merged as `a21cd14033f89a9294b060ef7bd071f7f026b281`.
- [RUN-20260809-104 — RC9.6 responsive-layout browser gate](runs/RUN-20260809-104.md) — `CI_VALIDATION_PENDING`: added one bounded Chromium responsive-layout gate across the accepted share-approval, analyst-search, CISO-revocation and auditor-read-only surfaces at representative mobile/tablet/desktop viewports; verifies no blocking horizontal overflow and viewport-contained usable controls; exact-head CI and retained browser evidence are required before PASS.
- [RUN-20260809-103 — RC9.5 exact-head acceptance](runs/RUN-20260809-103.md) — `PASS`: PR #59 exact head `cbd3dfc973a6daf06347e3ba4df2b5415848a063` passed all 24 registered workflows; retained artifact `9037726559` (`sha256:d5b0c7713abd6af3ac761e6999b3608c2b3b7093c682634d6c6f6fb2c971903d`) independently proved keyboard-only Chromium operation, no pointing-device use, visible focus, reachability and operability across all four accepted critical surfaces; merged as `187928c66143e0c8470082097fafba740da691c6`.
- [RUN-20260809-102 — RC9.5 keyboard navigation accessibility gate](runs/RUN-20260809-102.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-101 — RC9.4 exact-head acceptance](runs/RUN-20260809-101.md) — `PASS`: PR #57 exact head `487dbe1320a4ef820ff32f1c9ef8f8c7652a4868` passed all 23 registered workflows; retained artifact `9037246175` (`sha256:884950bf6789ecccedda51f0b2ff956a64328b30a9922ecf72414cc923707dc6`) independently proved Chromium execution, backend-derived `read:audit`, analyst backend denial, persisted PostgreSQL audit rendering, audit-chain validity and no browser-induced audit mutation; merged as `c7877015869bf58dec3a5f2628d71c4b0c2cf97a`.
- [RUN-20260809-100 — RC9.4 bounded auditor read-only browser journey](runs/RUN-20260809-100.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-099 — RC9.3 exact-head acceptance](runs/RUN-20260809-099.md) — `PASS`: PR #55 exact head `e945702adff884f174a40393b3121f3aed99648b` passed all 22 registered workflows; retained artifact `9037014726` (`sha256:69256fdcaa01c5b9832bd711a669ff73ef4db5923cc0bc66beab47034cf2b795`) independently proved Chromium execution, backend-derived `revoke:tokens`, analyst backend denial, CISO revocation, Redis token state and persistent audit-chain validity; merged as `3743203bc1a6d93743af53fcb8d4257af153a710`.
- [RUN-20260809-098 — RC9.3 bounded CISO token-revocation browser journey](runs/RUN-20260809-098.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-097 — RC9.2 exact-head acceptance](runs/RUN-20260809-097.md) — `PASS`: PR #53 exact head `ebc9a7ca2ebb1c0e9b55c057eaad82d3f04e5afd` passed all 21 registered workflows; retained artifact `9036721912` (`sha256:308f98282c5520b3d96bc04f9b14c382dbdb83c1fc8817809c87ea03ce94a82e`) independently proved Chromium execution, backend-derived `read:intelligence`, loading/empty/success states and real backend 503 behavior; merged as `22bf74bb6c5c367195a3e67b0c8db4ec0489a449`.
- [RUN-20260809-096 — RC9.2 analyst browser operational states](runs/RUN-20260809-096.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-095 — RC9.1 exact-head acceptance](runs/RUN-20260809-095.md) — `PASS`: PR #50 exact head `005512e124ff6c37a5acd3d2b8e4ba8c823d4a01` passed all 20 required workflows; retained browser artifact `9036392289` (`sha256:111d879e048f5978927472da996020f398448dd0752407f60a3366dbfbbf0fd6`) independently proved Chromium execution, blocked reviewer self-approval, distinct-publisher approval, hidden service-account approval controls and backend-derived permissions; merged as `ef59eba29d7fa8b2d88b5674e7bb00e98c0dab18`.
- [RUN-20260809-094 — RC9.1 browser fixture persistence remediation](runs/RUN-20260809-094.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-093 — RC9.1 first deterministic CI remediation](runs/RUN-20260809-093.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-092 — RC9.1 governed browser share-approval E2E](runs/RUN-20260809-092.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-090 — RC8.8 capacity limits and scaling guidance](runs/RUN-20260809-090.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-089 — RC8.7 acceptance and merge](runs/RUN-20260809-087.md) — `PASS`.
- [RUN-20260809-087 — RC8.7 exact-head evidence acceptance](runs/RUN-20260809-087.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-086 — RC8.7 bounded concurrency saturation](runs/RUN-20260809-086.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-085 — RC8.6 exact-head acceptance and merge](runs/RUN-20260809-085.md) — `PASS`.
- [RUN-20260809-084 — RC8.6 degraded-dependency performance/correctness](runs/RUN-20260809-084.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-083 — RC8.5 exact-head acceptance and merge](runs/RUN-20260809-083.md) — `PASS`.
- [RUN-20260809-082 — RC8.5 branch reconciliation against current main](runs/RUN-20260809-082.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260809-080 — Apache-2.0 and open-source governance baseline](runs/RUN-20260809-080.md) — `PASS`.
- [RUN-20260808-079 — Current-state documentation reconciliation acceptance](runs/RUN-20260808-079.md) — `PASS`.
- [RUN-20260808-077 — Current-state documentation, workflow and graph reconciliation](runs/RUN-20260808-077.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260808-075 — RC8.4 exact-head acceptance and merge](runs/RUN-20260808-075.md) — `PASS`.
- [RUN-20260808-074 — RC8.4 bounded ingestion-throughput performance harness](runs/RUN-20260808-074.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260808-073 — RC8.3 exact-head acceptance and merge](runs/RUN-20260808-073.md) — `PASS`.
- [RUN-20260808-072 — RC8.3 bounded OpenSearch search-read performance harness](runs/RUN-20260808-072.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260808-071 — RC8.2 exact-head acceptance and merge](runs/RUN-20260808-071.md) — `PASS`.
- [RUN-20260808-070 — RC8.2 bounded API-read performance harness](runs/RUN-20260808-070.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260808-069 — RC8.1 exact-head acceptance and merge](runs/RUN-20260808-069.md) — `PASS`.
- [RUN-20260808-068 — RC8.1 Phase 5 workload profile](runs/RUN-20260808-068.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260808-067 — RC7.10 exact-head acceptance and merge](runs/RUN-20260808-067.md) — `PASS`: Phase 4 accepted.
- [RUN-20260808-066 — Phase 4 external connector acceptance](runs/RUN-20260808-066.md) — `CI_VALIDATION_PENDING`.
- [RUN-20260807-065 — RC7.9 exact-head acceptance and merge](runs/RUN-20260807-065.md) — `PASS`.

## Current decision

`RUN-20260809-110` is `BLOCKED`. RC9.1 through RC9.8 remain accepted for their bounded scopes, but Phase 6 remains `IN PROGRESS`. Manual/source-level review found `A11Y-001`: asynchronous session resolution updates principal/role state and reveals RBAC-governed controls without live/status semantics. Product-wide WCAG 2.2 AA remains unevidenced; measured contrast, 200% resize, 320 CSS px reflow, text-spacing, full focus-order and genuine assistive-technology evidence remain open. Issue #1 external production gates remain open.

## Exactly one next priority

Remediate `A11Y-001` by making asynchronous principal/session resolution programmatically announced on all four critical surfaces, add bounded regression evidence, and preserve backend-derived RBAC and separate human share approval.