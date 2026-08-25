# Phase 11.10q — Sharing & Exchange functional recovery

## Purpose

Sharing & Exchange no longer uses a manually copied canonical UUID as the primary operator journey. The workspace discovers recent canonical intelligence through the same-origin `/api/v1/command-center` projection and lets an operator select an object before entering the existing governed review, approval and MISP export chain.

The canonical Threat Intelligence detail view now also provides a direct **Review & share** pivot for the selected canonical object. The pivot carries only the canonical item identifier to `/workbench/sharing?item={item_id}`; the Sharing workspace then reloads governance state from the server-authorized sharing API.

## Canonical population and selection

The discovery list is sourced from DTMO canonical persistence. It does not query MISP directly and does not fabricate targets when persistence is empty or unavailable. A canonical UUID field remains available only under **Advanced deep link / troubleshooting** for deterministic deep links and support workflows.

Selecting a target or following the Threat Intelligence pivot loads `/api/v1/sharing/items/{item_id}`. Existing review state, separation-of-duties evidence, authoritative source restrictions, export eligibility and persisted MISP delivery evidence remain object-specific.

## Authority boundaries

Object discovery, selection and navigation grant no mutation authority. Independent review and separate sharing approval remain server-authorized. Following the Threat Intelligence pivot cannot record review, approve sharing, trigger export, publish or synchronize anything by itself. MISP export remains limited to an explicitly eligible, approved canonical revision and creates an unpublished event (`published=false`). Publication and synchronization are not exposed by this recovery slice.

A discovery failure or empty canonical target list is not evidence that MISP is healthy, that no intelligence exists upstream, or that an object is ready to share. The interface fails closed and preserves the advanced deep-link fallback without converting absence into a governance conclusion.

## Acceptance

`backend/tests/test_phase11_10q_object_driven_sharing.py` enforces canonical discovery, direct Threat Intelligence → Sharing pivoting, object-driven state loading and authority boundaries. `.github/workflows/phase11-10q-object-driven-sharing.yml` provides the dedicated exact-head gate.
