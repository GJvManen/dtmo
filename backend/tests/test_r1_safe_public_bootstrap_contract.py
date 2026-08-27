from pathlib import Path


def _env_value(name: str) -> str:
    for raw in Path('.env.example').read_text(encoding='utf-8').splitlines():
        if raw.startswith(f'{name}='):
            return raw.split('=', 1)[1]
    raise AssertionError(f'missing {name}')


def test_local_reference_profile_enables_only_credentialless_public_collection_defaults():
    assert _env_value('DTMO_FEATURE_LIVE_CONNECTORS') == 'true'
    assert _env_value('DTMO_FEATURE_VULNERABILITY_LOOKUP_CONNECTOR') == 'true'
    assert _env_value('DTMO_VULNERABILITY_LOOKUP_API_TOKEN') == ''
    assert _env_value('DTMO_FEATURE_OPENCVE_CONNECTOR') == 'false'
    assert _env_value('DTMO_OPENCVE_API_TOKEN') == ''
    assert _env_value('DTMO_FEATURE_OPENCTI_READ') == 'false'


def test_installation_guide_preserves_evidence_and_external_service_boundaries():
    text = Path('docs/installation/INSTALLATION_GUIDE.md').read_text(encoding='utf-8')
    assert 'credentialless **CISA KEV** path and **CIRCL Vulnerability-Lookup**' in text
    assert 'OpenCVE remains disabled by default' in text
    assert 'MISP, AIL, Taranis AI, IntelOwl, Cortex, OpenCTI and TheHive also remain disabled' in text
    assert 'not proof of upstream completeness, local exposure, compromise, remediation or production readiness' in text
