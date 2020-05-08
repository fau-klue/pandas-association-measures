import pytest

from association_measures import binomial as bi


@pytest.mark.binomial
def test_choose():

    assert bi.choose(9, 3) == 84
    assert bi.choose(5, 2) == 10
    assert bi.choose(2, 2) == 1
    assert bi.choose(0, 0) == 1
    assert bi.choose(-3, 5) == 0
    assert bi.choose(-2, -2) == 0
    assert bi.choose(10, -2) == 0
    assert bi.choose(1000, 500) == 2.7028824094543644e+299
