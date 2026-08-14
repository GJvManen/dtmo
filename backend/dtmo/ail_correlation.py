from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class CorrelationHit:
    source_id: str
    external_id: str | None
    item_type: str
    title: str
    relation: str
    matched_value: str
    context: dict[str, Any]


def _text_values(item: dict[str, Any]) -> list[str]:
    values = [str(item.get("title") or ""), str(item.get("summary") or "")]
    tags = item.get("tags")
    if isinstance(tags, list):
        values.extend(str(tag) for tag in tags)
    return values


def _exact_text_match(indicator: str, item: dict[str, Any]) -> bool:
    needle = indicator.casefold()
    return any(needle == value.strip().casefold() for value in _text_values(item) if value.strip())


def _misp_values(raw: dict[str, Any]) -> Iterable[tuple[str, str, dict[str, Any]]]:
    projection = raw.get("_dtmo_misp")
    if not isinstance(projection, dict):
        return []
    hits: list[tuple[str, str, dict[str, Any]]] = []
    attributes = projection.get("attributes")
    if isinstance(attributes, list):
        for attribute in attributes:
            if not isinstance(attribute, dict):
                continue
            value = attribute.get("value")
            if isinstance(value, str) and value:
                hits.append((value, "misp_attribute", {"type": attribute.get("type"), "uuid": attribute.get("uuid")}))
    objects = projection.get("objects")
    if isinstance(objects, list):
        for obj in objects:
            if not isinstance(obj, dict):
                continue
            obj_attrs = obj.get("attributes")
            if not isinstance(obj_attrs, list):
                continue
            for attribute in obj_attrs:
                if not isinstance(attribute, dict):
                    continue
                value = attribute.get("value")
                if isinstance(value, str) and value:
                    hits.append(
                        (
                            value,
                            "misp_object_attribute",
                            {
                                "object_uuid": obj.get("uuid"),
                                "object_name": obj.get("name"),
                                "type": attribute.get("type"),
                                "uuid": attribute.get("uuid"),
                            },
                        )
                    )
    return hits


def correlate_ail_indicator(
    *,
    indicator_type: str,
    indicator_value: str,
    candidates: Iterable[dict[str, Any]],
) -> list[CorrelationHit]:
    """Return deterministic, data-minimized correlations for one AIL-derived indicator.

    The caller supplies canonical DTMO candidate records and, where available,
    provenance-preserved MISP raw projections. The function never returns raw AIL
    paste/content fields and performs no fuzzy or semantic inference.
    """

    value = indicator_value.strip()
    if not value:
        raise ValueError("indicator value is required")
    hits: list[CorrelationHit] = []
    seen: set[tuple[str, str | None, str, str]] = set()

    for item in candidates:
        source_id = str(item.get("source_id") or "")
        external_id = item.get("external_id")
        external_id_value = str(external_id) if external_id is not None else None
        item_type = str(item.get("item_type") or "")
        title = str(item.get("title") or external_id_value or source_id or "correlated intelligence")

        if source_id == "ail" and external_id_value:
            continue

        if _exact_text_match(value, item):
            relation = "canonical_exact_match"
            context: dict[str, Any] = {"indicator_type": indicator_type}
            metadata = item.get("metadata")
            if isinstance(metadata, dict):
                vendor = metadata.get("vendor")
                product = metadata.get("product")
                if isinstance(vendor, str):
                    context["vendor"] = vendor
                if isinstance(product, str):
                    context["product"] = product
            key = (source_id, external_id_value, relation, value.casefold())
            if key not in seen:
                hits.append(CorrelationHit(source_id, external_id_value, item_type, title, relation, value, context))
                seen.add(key)

        raw = item.get("raw")
        if source_id == "misp" and isinstance(raw, dict):
            for misp_value, relation, context in _misp_values(raw):
                if misp_value.casefold() != value.casefold():
                    continue
                key = (source_id, external_id_value, relation, value.casefold())
                if key in seen:
                    continue
                hits.append(CorrelationHit(source_id, external_id_value, item_type, title, relation, value, context))
                seen.add(key)

        if item_type == "vulnerability":
            metadata = item.get("metadata")
            if isinstance(metadata, dict):
                cve_id = metadata.get("cve_id") or external_id_value
                aliases = metadata.get("aliases")
                values = [str(cve_id or "")]
                if isinstance(aliases, list):
                    values.extend(str(alias) for alias in aliases)
                if any(candidate.casefold() == value.casefold() for candidate in values if candidate):
                    relation = "vulnerability_identifier"
                    context = {
                        "cve_id": cve_id,
                        "vendor": metadata.get("vendor"),
                        "product": metadata.get("product"),
                    }
                    key = (source_id, external_id_value, relation, value.casefold())
                    if key not in seen:
                        hits.append(CorrelationHit(source_id, external_id_value, item_type, title, relation, value, context))
                        seen.add(key)

    return hits
