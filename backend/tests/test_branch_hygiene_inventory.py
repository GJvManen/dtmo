from tools import branch_hygiene_inventory as hygiene


def test_inventory_is_read_only_and_retains_evidence_namespaces(monkeypatch):
    monkeypatch.setattr(
        hygiene,
        "git",
        lambda *args: (
            "origin/main aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n"
            "origin/audit/run-old bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\n"
            "origin/candidate-test cccccccccccccccccccccccccccccccccccccccc\n"
            "origin/feature-merged dddddddddddddddddddddddddddddddddddddddd\n"
            "origin/feature-open eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
            if args and args[0] == "for-each-ref"
            else ""
        ),
    )
    monkeypatch.setattr(
        hygiene,
        "is_ancestor",
        lambda tip, base: tip
        in {
            "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            "cccccccccccccccccccccccccccccccccccccccc",
            "dddddddddddddddddddddddddddddddddddddddd",
        },
    )

    records = {record.branch: record for record in hygiene.inventory("main", "origin")}

    assert records["audit/run-old"].classification == "RETAIN"
    assert records["candidate-test"].classification == "RETAIN"
    assert records["feature-merged"].classification == "DELETE_ELIGIBLE_REVIEW"
    assert records["feature-open"].classification == "RETAIN_REVIEW"


def test_inventory_tool_contains_no_branch_delete_operation():
    source = (hygiene.__file__ and open(hygiene.__file__, encoding="utf-8").read()) or ""
    assert "git branch -d" not in source
    assert "git push" not in source
    assert "delete-ref" not in source
