"""Intentional failure to verify PR status-check blocking. Remove after checking."""


def test_intentional_failure_for_ci_block_check():
    assert False, "intentional failure — verify PR is blocked when pytest fails"
