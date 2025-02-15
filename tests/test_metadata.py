# dependencies
import ndradexhyperfine


# test functions
def test_version():
    """Make sure the version is valid."""
    assert ndradexhyperfine.__version__ == "0.2.2"


def test_author():
    """Make sure the author is valid."""
    assert ndradexhyperfine.__author__ == "Akio Taniguchi"
