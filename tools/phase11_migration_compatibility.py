from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = ROOT / "database" / "migrations" / "versions"


def _literal_assignment(tree: ast.Module, name: str) -> Any:
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise ValueError(f"missing {name}")


def inspect_migration_graph() -> dict[str, Any]:
    revisions: dict[str, str | None] = {}
    files: dict[str, str] = {}
    for path in sorted(VERSIONS.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        revision = _literal_assignment(tree, "revision")
        down_revision = _literal_assignment(tree, "down_revision")
        if not isinstance(revision, str):
            raise ValueError(f"non-string revision in {path.name}")
        if down_revision is not None and not isinstance(down_revision, str):
            raise ValueError(f"branch/merge migration not supported by bounded compatibility contract: {path.name}")
        if revision in revisions:
            raise ValueError(f"duplicate revision {revision}")
        functions = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        if "upgrade" not in functions or "downgrade" not in functions:
            raise ValueError(f"migration lacks upgrade/downgrade contract: {path.name}")
        revisions[revision] = down_revision
        files[revision] = path.name

    if not revisions:
        raise ValueError("no migrations found")
    referenced = {parent for parent in revisions.values() if parent is not None}
    missing = sorted(referenced - revisions.keys())
    if missing:
        raise ValueError(f"missing parent revisions: {missing}")
    heads = sorted(set(revisions) - referenced)
    roots = sorted(rev for rev, parent in revisions.items() if parent is None)
    if len(heads) != 1 or len(roots) != 1:
        raise ValueError(f"migration graph must be single-root/single-head; roots={roots}, heads={heads}")

    ordered: list[str] = []
    current = heads[0]
    while current is not None:
        ordered.append(current)
        current = revisions[current]
    ordered.reverse()
    if len(ordered) != len(revisions):
        raise ValueError("migration graph contains disconnected revisions")

    return {
        "decision": "pass",
        "migration_count": len(ordered),
        "root_revision": roots[0],
        "head_revision": heads[0],
        "ordered_revisions": ordered,
        "files": [files[r] for r in ordered],
        "single_linear_graph": True,
        "forward_migration_required_before_application_cutover": True,
        "automatic_database_down_migration_allowed": False,
        "mixed_version_window": "bounded: previous application revision may coexist only while schema changes remain backward-compatible",
        "live_migration_claimed": False,
        "production_equivalent_claimed": False,
        "production_authorization_claimed": False,
    }


def main() -> None:
    print(json.dumps(inspect_migration_graph(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
