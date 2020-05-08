import association_measures.frequencies as fq
import association_measures.measures as am
from pandas import read_csv


def test_input():

    df = read_csv("tests/ucs-gold-100.ds", comment='#', index_col=0,
                  sep="\t", quoting=3, keep_default_na=False)

    df.rename({'l2': 'item'}, axis=1, inplace=True)

    df = df[['item', 'f', 'f1', 'f2', 'N']]
    print(df[['item', 'f', 'f1', 'f2', 'N']].head())

    obs = fq.observed_frequencies(df)
    print()
    print(obs[['O11', 'O12', 'O21', 'O22']].head())

    exp = fq.expected_frequencies(df)
    print()
    print(exp[['E11', 'E12', 'E21', 'E22']].head())

    df = df.set_index('item')
    print()
    print(df.head())
    obs = fq.observed_frequencies(df)
    print()
    print(obs[['O11', 'O12', 'O21', 'O22']].head())


def test_ams():

    df = read_csv("tests/ucs-gold-100.ds", comment='#', index_col=0,
                  sep="\t", quoting=3, keep_default_na=False)
    df.rename({'l2': 'item'}, axis=1, inplace=True)

    df = df[['item', 'f', 'f1', 'f2', 'N']]
    print(df[['item', 'f', 'f1', 'f2', 'N']].head())

    df_ams = am.calculate_measures(df, ['log_likelihood', 'log_ratio'])
    print(df_ams.head())

    df_ams = am.calculate_measures(df)
    print(df_ams.head())

    df = df.set_index('item')
    df_ams = am.calculate_measures(df)
    print(df_ams.head())
