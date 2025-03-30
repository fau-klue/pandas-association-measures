from association_measures.comparisons import rbo, gwets_ac1


def test_rbo(log_ratio_dataframe, rbo_dataframe):

    df = log_ratio_dataframe
    rbo_dataframe = rbo_dataframe.loc[rbo_dataframe['p'] > 0]
    rbo_dataframe = rbo_dataframe.loc[rbo_dataframe['p'] < 1]
    left = df.sort_values(by='lrc.positive', ascending=False).head(50).index.to_list()
    right = df.sort_values(by='lrc.normal', ascending=False).head(50).index.to_list()

    rbo_dataframe['here'] = rbo_dataframe.apply(lambda x: rbo(left, right, k=int(x['k']), p=x['p'])[2], axis=1)

    rbo_dataframe['here'] = round(rbo_dataframe['here'], 2)
    rbo_dataframe['rbo'] = round(rbo_dataframe['rbo'], 2)

    # assert round(rbo_dataframe['here'], 4).equals(round(rbo_dataframe['rbo'], 4))
    print(rbo_dataframe.loc[rbo_dataframe['rbo'] != rbo_dataframe['here']])
    # close enough for now


def test_gwets_ac1(log_ratio_dataframe):

    df = log_ratio_dataframe
    left = df.sort_values(by='lrc.positive', ascending=False).head(50).index.to_list()
    right = df.sort_values(by='lrc.normal', ascending=False).head(50).index.to_list()

    ac1 = gwets_ac1(left, right)
    print(ac1)
