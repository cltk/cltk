from cltkv1 import __version__


def test_vergision():
    assert __version__ == "1.0.0a"


def test_true():
    assert True is True


def test_false():
    assert True is not False
