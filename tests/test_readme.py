import association_measures.frequencies as fq
import association_measures.measures as am
from association_measures.grids import topography


def test_frequencies(ucs_dataframe):

    # contingency table notation
    df = ucs_dataframe
    obs = fq.observed_frequencies(df)
    print()
    print(obs[['O11', 'O12', 'O21', 'O22']].head())

    # frequency signature notation
    df.rename({'l2': 'item'}, axis=1, inplace=True)
    df = df[['item', 'f', 'f1', 'f2', 'N']]
    df.index.name = 'id'
    print()
    print(df.head())

    # keywords
    tmp = df[['item', 'f', 'f1']].rename({'f': 'f1', 'f1': 'N1'}, axis=1)
    tmp['f2'] = df['f2'] - df['f']
    tmp['N2'] = df['N'] - df['f1']
    print()
    print(tmp.head())

    # expected frequencies
    exp = fq.expected_frequencies(df)
    print()
    print(exp[['E11', 'E12', 'E21', 'E22']].head())

    # observed frequencies
    obs = fq.observed_frequencies(df)
    print()
    print(obs[['O11', 'O12', 'O21', 'O22']].head())

    # raw
    print()
    print(df.head())


def test_measures(ucs_dataframe):

    df = fq.expected_frequencies(ucs_dataframe, observed=True)
    df['item'] = ucs_dataframe['l2']
    df = df.set_index('item')

    df_ams = am.log_likelihood(df)
    print(df_ams.head())

    df_ams = am.score(df, measures=['log_likelihood'])
    print(df_ams.head())

    df_ams = am.score(df, freq=False)
    print(df_ams.head())

    df_ams = am.score(df, measures=['log_likelihood'], signed=False, freq=False)
    print(df_ams.head())


def test_topography():

    print(topography())
