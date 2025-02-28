import association_measures.measures as am
from pandas import DataFrame


def test_nas():

    d = DataFrame(data={'O11': 0, 'O12': 10, 'O21': 10, 'O22': 100}, index=['test'])
    scores = am.score(d)
    print(scores[['mutual_information', 'local_mutual_information']])

    d = DataFrame(data={'O11': 0, 'O12': 10, 'O21': 0, 'O22': 100}, index=['test'])
    scores = am.score(d)
    print(scores[['ipm', 'ipm_expected']])
