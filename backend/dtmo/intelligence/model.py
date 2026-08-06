from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class IntelligenceType(StrEnum):
    """Canonical DTMO intelligence categories."""

    INCIDENT = "incident"
    ADVISORY = "advisory"
    VULNERABILITY = "vulnerability"
    INDICATOR = "indicator"
    CAMPAIGN = "campaign"
    THREAT_ACTOR = "threat_actor"
    MALWARE = "malware"
    VENDOR_NOTICE = "vendor_notice"


class IntelligenceSeverity(StrEnum):
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SourceReliability(StrEnum):
    """Simplified Admiralty-style source reliability classification."""

    AUTHORITATIVE = "authoritative"
    RELIABLE = "reliable"
    USUALLY_RELIABLE = "usually_reliable"
    UNKNOWN = "unknown"
    UNRELIABLE = "unreliable"


class ConfidenceLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


_RELIABILITY_SCORE: dict[SourceReliability, int] = {
    SourceReliability.AUTHORITATIVE: 95,
    SourceReliability.RELIABLE: 85,
    SourceReliability.USUALLY_RELIABLE: 70,
    SourceReliability.UNKNOWN: 45,
    SourceReliability.UNRELIABLE: 15,
}


@dataclass(frozen=True, slots=True)
class ConfidenceAssessment:
    score: int
    level: ConfidenceLevel
    rationale: tuple[str, ...]

    def __post_init__(self) -> None:
        if not 0 <= self.score <= 100:
            raise ValueError("confidence score must be between 0 and 100")
        if not self.rationale:
            raise ValueError("confidence assessment requires a rationale")


def calculate_confidence(
    *,
    reliability: SourceReliability,
    corroborating_sources: int = 0,
    primary_source: bool = False,
    content_integrity_verified: bool = False,
) -> ConfidenceAssessment:
    """Calculate a deterministic confidence score with an auditable rationale.

    The score is intentionally conservative. Corroboration is capped so multiple
    low-quality copies cannot inflate confidence beyond the source's quality.
    """

    if corroborating_sources < 0:
        raise ValueError("corroborating_sources cannot be negative")

    score = _RELIABILITY_SCORE[reliability]
    rationale = [f"source reliability: {reliability.value}"]

    corroboration_bonus = min(corroborating_sources, 3) * 4
    if corroboration_bonus:
        score += corroboration_bonus
        rationale.append(f"{min(corroborating_sources, 3)} corroborating source(s)")

    if primary_source:
        score += 3
        rationale.append("primary source available")

    if content_integrity_verified:
        score += 2
        rationale.append("content integrity verified")

    score = min(score, 100)
    if score >= 90:
        level = ConfidenceLevel.VERY_HIGH
    elif score >= 75:
        level = ConfidenceLevel.HIGH
    elif score >= 50:
        level = ConfidenceLevel.MEDIUM
    else:
        level = ConfidenceLevel.LOW

    return ConfidenceAssessment(score=score, level=level, rationale=tuple(rationale))
