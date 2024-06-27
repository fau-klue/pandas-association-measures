from association_measures.grids import topography
from pandas import DataFrame


def test_map():
    assert isinstance(topography(), DataFrame)
