from __future__ import annotations

from unittest.mock import patch

from dtmo.api import routes


def test_object_store_is_not_created_during_api_module_startup() -> None:
    routes.get_intelligence_lake.cache_clear()
    assert routes.get_intelligence_lake.cache_info().currsize == 0

    with patch.object(
        routes,
        "MinioObjectStore",
        side_effect=ValueError("storage credentials intentionally absent"),
    ):
        assert routes.get_intelligence_lake.cache_info().currsize == 0


def test_object_store_configuration_is_enforced_when_ingestion_needs_it() -> None:
    routes.get_intelligence_lake.cache_clear()

    with patch.object(
        routes,
        "MinioObjectStore",
        side_effect=ValueError("storage credentials intentionally absent"),
    ):
        try:
            routes.get_intelligence_lake()
        except ValueError as exc:
            assert str(exc) == "storage credentials intentionally absent"
        else:
            raise AssertionError("ingestion storage initialization must fail closed")
