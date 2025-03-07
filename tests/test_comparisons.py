from association_measures.comparisons import rbo


def test_rbo(log_ratio_dataframe):

    df = log_ratio_dataframe
    left = df.sort_values(by='lrc.positive', ascending=False).index.to_list()
    right = df.sort_values(by='lrc.normal', ascending=False).index.to_list()
    r = rbo(left, right, k=20, p=.95)

    assert round(r, 2) == 0.93
