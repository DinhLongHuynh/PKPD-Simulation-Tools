from pkpd_sian import __version__


def test_semantic_version_present():
    major, minor, patch = __version__.split(".")
    assert major.isdigit()
    assert minor.isdigit()
    assert patch.isdigit()
