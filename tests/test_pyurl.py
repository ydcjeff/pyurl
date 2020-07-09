import pytest

from pyurl.pyurl import add, log, no_view, remove, sync


@pytest.mark.parametrize(
    "a",
    [
        "https://www.bloomberg.com/asia",
        "https://pytorch.org/blog/",
        "https://blog.tensorflow.org/",
        "https://www.androidauthority.com/",
        "https://www.androidcentral.com/",
        "https://edition.cnn.com/",
        "https://www.bbc.com/news/world",
    ],
)
def test_add(a):
    test_add_output = add(a)
    assert test_add_output == 1


@pytest.mark.parametrize(
    "a",
    [
        "https://www.bloomberg.com/asia",
        "https://pytorch.org/blog/",
        "https://blog.tensorflow.org/",
        "https://www.androidauthority.com/",
        "https://www.androidcentral.com/",
        "https://edition.cnn.com/",
        "https://www.bbc.com/news/world",
    ],
)
def test_add_again(a):
    test_add_output = add(a)
    assert test_add_output == 0


def test_log():
    test_log_output = log(True)
    assert test_log_output == 1
    test_log_output = log(False)
    assert test_log_output == 0


def test_no_view():
    test_no_view_output = no_view(False, True)
    assert test_no_view_output == 0
    test_no_view_output = no_view(False, False)
    assert test_no_view_output == 0
    test_no_view_output = no_view(True, True)
    assert test_no_view_output == 1
    test_no_view_output = no_view(True, False)
    assert test_no_view_output == 1


@pytest.mark.parametrize(
    "s",
    [
        "https://www.bloomberg.com/asia",
        "https://pytorch.org/blog/",
        "https://blog.tensorflow.org/",
        "https://www.androidauthority.com/",
        "https://www.androidcentral.com/",
        "https://edition.cnn.com/",
        "https://www.bbc.com/news/world",
        "all",
    ],
)
def test_sync(s):
    test_sync_output = sync(s, True)
    assert test_sync_output == 0


@pytest.mark.parametrize(
    "r",
    [
        "https://www.bloomberg.com/asia",
        "https://pytorch.org/blog/",
        "https://blog.tensorflow.org/",
        "https://www.androidauthority.com/",
        "https://www.androidcentral.com/",
        "https://edition.cnn.com/",
        "https://www.bbc.com/news/world",
    ],
)
def test_remove(r):
    test_remove_output = remove(r)
    assert test_remove_output == 1
