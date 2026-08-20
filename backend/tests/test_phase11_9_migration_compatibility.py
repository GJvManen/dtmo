from tools.phase11_migration_compatibility import inspect_migration_graph


def test_migration_graph_is_single_linear_forward_contract() -> None:
    evidence = inspect_migration_graph()
    assert evidence["decision"] == "pass"
    assert evidence["migration_count"] >= 1
    assert evidence["single_linear_graph"] is True
    assert evidence["forward_migration_required_before_application_cutover"] is True
    assert evidence["automatic_database_down_migration_allowed"] is False
    assert evidence["live_migration_claimed"] is False
    assert evidence["production_equivalent_claimed"] is False
    assert evidence["production_authorization_claimed"] is False
    assert len(evidence["ordered_revisions"]) == evidence["migration_count"]
    assert len(evidence["files"]) == evidence["migration_count"]
