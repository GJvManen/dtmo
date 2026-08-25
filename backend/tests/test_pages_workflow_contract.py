from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"


def test_pages_workflow_skips_deploy_when_pages_is_unconfigured() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")
    workflow = yaml.safe_load(source)

    assert workflow["name"] == "Publish DTMO Pages"
    assert "gh api \"repos/${GITHUB_REPOSITORY}/pages\"" in source
    assert 'echo "enabled=false" >> "$GITHUB_OUTPUT"' in source
    assert "documentation deployment remains disabled" in source
    assert source.count("if: steps.pages.outputs.enabled == 'true'") == 3


def test_pages_workflow_does_not_enable_pages_implicitly() -> None:
    source = WORKFLOW.read_text(encoding="utf-8")

    assert "enablement: true" not in source
    assert "actions/configure-pages@v5" in source
    assert "actions/deploy-pages@v4" in source
