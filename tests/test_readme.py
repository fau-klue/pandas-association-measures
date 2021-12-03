import association_measures.frequencies as fq
import association_measures.measures as am
from pandas import read_csv


def test_input():

    # frequency signature notation
    df = read_csv("tests/ucs-gold-100.ds", comment='#', index_col=0,
                  sep="\t", quoting=3, keep_default_na=False)
    df.rename({'l2': 'item'}, axis=1, inplace=True)
    df = df[['item', 'f', 'f1', 'f2', 'N']]
    df.index.name = 'id'
    print()
    print(df.head())

    # keywords
    tmp = df[['item', 'f', 'f1']].rename({'f': 'f1', 'f1': 'N1'}, axis=1)
    tmp['f2'] = df['f2'] - df['f']
    tmp['N2'] = df['N'] - df['f1']
    print(tmp.head())

    # contingency notation
    obs = fq.observed_frequencies(df)
    print()
    print(obs[['O11', 'O12', 'O21', 'O22']].head())

    # expected frequencies
    exp = fq.expected_frequencies(df)
    print()
    print(exp[['E11', 'E12', 'E21', 'E22']].head())

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


def test_score():

    df = read_csv("tests/ucs-gold-100.ds", comment='#', index_col=0,
                  sep="\t", quoting=3, keep_default_na=False)
    df.rename({'l2': 'item'}, axis=1, inplace=True)

    ucs_dataframe = df[['item', 'f', 'f1', 'f2', 'N']].set_index('item')

    # frequency signature notation with int parameters:
    f1 = int(ucs_dataframe['f1'].iloc[0])
    N = int(ucs_dataframe['N'].iloc[0])
    print(ucs_dataframe[['f', 'f2']].head())
    df_sig = am.score(ucs_dataframe[['f', 'f2']], f1, N, measures=['log_likelihood'])
    print("f1: ", f1)
    print("N: ", N)
    print(df_sig.head())

    # corpus frequency notation with int parameters:
    tmp = ucs_dataframe[['f', 'f1']].rename({'f': 'f1', 'f1': 'N1'}, axis=1)
    tmp['N2'] = ucs_dataframe['N'] - ucs_dataframe['f1']
    tmp['f2'] = ucs_dataframe['f2'] - ucs_dataframe['f']
    N1 = int(tmp['N1'].iloc[0])
    N2 = int(tmp['N2'].iloc[0])
    print(tmp[['f1', 'f2']].head())
    print("N1: ", N1)
    print("N2: ", N2)
    df_cor = am.score(tmp[['f1', 'f2']], N1=N1, N2=N2, measures=['log_likelihood'])
    print(df_cor.head())

    # parameters
    df_cor = am.score(tmp[['f1', 'f2']], N1=N1, N2=N2, measures=['conservative_log_ratio'], freq=False, alpha=.01)
    print(df_cor.head())

    df_cor = am.score(tmp[['f1', 'f2']], N1=N1, N2=N2, measures=['conservative_log_ratio'], freq=False, alpha=1)
    print(df_cor.head())
