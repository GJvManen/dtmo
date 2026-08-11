# RC11.1 Source Framework Core Gate

Status: PENDING_CI

## Objective

Introduce one governed adapter registry and execution dispatcher for all executable catalog sources without weakening existing source transport, provenance, credential or publication controls.

## Acceptance criteria

- every catalog entry with `execution_status == supported` maps to exactly one registered adapter profile;
- anonymous and credentialed execution are selected by the framework, not by the console;
- credentialed adapters fail closed when their logical secret reference is absent;
- the framework inventory exposes execution characteristics but never secret values;
- the existing unified console run path uses the framework dispatcher;
- unsupported/planned catalog sources remain fail closed;
- existing pinned HTTPS, DNS re-resolution, non-global address rejection, redirect rejection, response bounds, provenance and human review/share approval boundaries remain unchanged;
- lint, type checking, unit/regression tests, container smoke, accessibility, connector, recovery, performance, observability and staging-emulator gates pass on the exact PR head.

## Migration boundary

This slice does not yet rewrite every existing parser into a new class hierarchy. It establishes the central registry/dispatcher contract first so subsequent Red Hat, Ubuntu, Debian and other vendor adapters can be thin framework adapters. Existing accepted executors remain the implementation behind the registered profiles until migrated in bounded follow-up slices.

## Release decision

Do not mark PASS or merge until the full exact-head GitHub Actions evidence set is `completed/success`.
