from __future__ import annotations

import pytest

from dtmo.intelligence import (
    ConfidenceAssessment,
    ConfidenceLevel,
    SourceReliability,
    calculate_confidence,
)


def test_authoritative_primary_source_reaches_very_high_confidence() -> None:
    assessment = calculate_confidence(
        reliability=SourceReliability.AUTHORITATIVE,
        corroborating_sources=2,
        primary_source=True,
        content_integrity_verified=True,
    )

    assert assessment.score == 100
    assert assessment.level is ConfidenceLevel.VERY_HIGH
    assert "primary source available" in assessment.rationale
    assert "content integrity verified" in assessment.rationale


def test_unknown_uncorroborated_source_remains_low_confidence() -> None:
    assessment = calculate_confidence(reliability=SourceReliability.UNKNOWN)

    assert assessment.score == 45
    assert assessment.level is ConfidenceLevel.LOW


def test_corroboration_bonus_is_capped() -> None:
    three_sources = calculate_confidence(
        reliability=SourceReliability.RELIABLE,
        corroborating_sources=3,
    )
    ten_sources = calculate_confidence(
        reliability=SourceReliability.RELIABLE,
        corroborating_sources=10,
    )

    assert ten_sources.score == three_sources.score
    assert ten_sources.rationale == three_sources.rationale


def test_negative_corroborating_source_count_is_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_confidence(
            reliability=SourceReliability.RELIABLE,
            corroborating_sources=-1,
        )


def test_confidence_assessment_requires_valid_score_and_rationale() -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        ConfidenceAssessment(
            score=101,
            level=ConfidenceLevel.VERY_HIGH,
            rationale=("invalid",),
        )

    with pytest.raises(ValueError, match="requires a rationale"):
        ConfidenceAssessment(
            score=50,
            level=ConfidenceLevel.MEDIUM,
            rationale=(),
        )
