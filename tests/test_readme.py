import association_measures.frequencies as fq
import association_measures.measures as am
from pandas import read_csv


def test_input():
    df = read_csv("tests/ucs-gold.ds.gz", comment='#', index_col=0,
                  sep="\t", quoting=3, keep_default_na=False)

    df.rename({'l2': 'item'}, axis=1, inplace=True)
    df = df[['item', 'f', 'f1', 'f2', 'N']]
    print(df[['item', 'f', 'f1', 'f2', 'N']].head())

    fq.expected_frequencies(df)

    print()
    print(df[['item', 'O11', 'O12', 'O21', 'O22']].head())

    print()
    print(df[['item', 'E11', 'E12', 'E21', 'E22', 'N']].head())

    print()
    print(df.columns)

    df = df[['item', 'f', 'f1', 'f2', 'N']]
    e = fq.expected_frequencies(df, inplace=False)
    print()
    print(df.columns)

    print()
    print([d.head() for d in e])


def test_ams():
    df = read_csv("tests/ucs-gold.ds.gz", comment='#', index_col=0,
                  sep="\t", quoting=3, keep_default_na=False)

    df = df[['l2', 'f', 'f1', 'f2', 'N']]
    print(df[['l2', 'f', 'f1', 'f2', 'N']].head())

    df['MI'] = am.mutual_information(df)
    print(df.head())

    df2 = am.calculate_measures(df, inplace=False)
    print(df2.columns)
    print(df2.head())

    df3 = am.calculate_measures(df,
                                measures=['log_likelihood', 'log_ratio'],
                                inplace=False)
    print(df3.columns)
    print(df3.head())
