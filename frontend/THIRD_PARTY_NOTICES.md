# Frontend third-party notices

This file records the direct third-party packages introduced for the DTMO Phase 11.10b canonical application shell. Exact versions are governed by `package.json` and the committed npm lockfile.

| Package | Purpose | Upstream license |
|---|---|---|
| React / react-dom | Browser component runtime | MIT |
| React Router DOM | Canonical client-side routing | MIT |
| TanStack Query | Governed server-state request lifecycle | MIT |
| Vite | Frontend build tooling | MIT |
| @vitejs/plugin-react | React build integration | MIT |
| TypeScript | Static type checking | Apache-2.0 |
| @types/react / @types/react-dom | Type declarations | MIT |

The repository license for DTMO remains Apache License 2.0. Third-party packages retain their own licenses and notices. This summary is not a substitute for the dependency lockfile, generated SBOM or upstream license texts.

No package listed here grants the browser authority to call upstream intelligence/case-analysis services directly. Service-specific licensing and deployment boundaries remain separate from the DTMO browser dependency set.
