# from cltkv1 import __version__

# def test_version():
#     assert __version__ == "1.0.0a"


def test_true():
    assert True is True


def test_false():
    assert True is not False


if __name__ == "__main__":
    import cltkv1

    print(dir(cltkv1))
    print(cltkv1.__package__)
    print(cltkv1.__path__)
    print(cltkv1.__file__)
    print(cltkv1.__name__)
    print(cltkv1.__doc__)
    print(cltkv1.__checking__)
