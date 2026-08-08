from pathlib import Path
import tomllib


ROOT = Path(__file__).resolve().parents[2]


REQUIRED_GOVERNANCE_FILES = (
    "LICENSE",
    "NOTICE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SUPPORTED_VERSIONS.md",
    "docs/legal/LICENSING.md",
    "docs/legal/THIRD_PARTY.md",
)


def test_required_open_source_governance_files_exist() -> None:
    missing = [path for path in REQUIRED_GOVERNANCE_FILES if not (ROOT / path).is_file()]
    assert missing == []


def test_license_is_canonical_apache_2_0_text() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Apache License" in license_text
    assert "Version 2.0, January 2004" in license_text
    assert "TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION" in license_text
    assert "END OF TERMS AND CONDITIONS" in license_text


def test_python_package_declares_spdx_license() -> None:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)
    assert pyproject["project"]["license"] == "Apache-2.0"


def test_readme_exposes_license_and_governance_entry_points() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Apache License, Version 2.0" in readme
    for path in REQUIRED_GOVERNANCE_FILES:
        assert f"`{path}`" in readme or path in {"LICENSE", "NOTICE"}


def test_third_party_policy_does_not_relicense_external_material() -> None:
    policy = (ROOT / "docs/legal/THIRD_PARTY.md").read_text(encoding="utf-8")
    assert "does not replace the licences or terms" in policy
    assert "technically successful connector does not establish legal permission" in policy
