"""
Script to measure the performance
"""

import timeit
import sys


# number of iterations
iterations = 1000
if len(sys.argv) > 1:
    iterations = int(sys.argv[1])


# code snippet to be executed only once
setup = """
import pandas as pd
import association_measures.frequencies as fq
import association_measures.measures as am

df = pd.read_csv('tests/data/brown.csv')

df = fq.observed_frequencies(df)
df = fq.expected_frequencies(df, observed=True)
"""


# code snippet whose execution time is to be measured
codes = [
    {
        'name': 'contingency_table',
        'code': 'fq.observed_frequencies(df)'
    },
    {
        'name': 'expected_frequencies',
        'code': 'fq.expected_frequencies(df)'
    },
    # asymptotic hypothesis tests
    {
        'name': 'z_score',
        'code': 'am.z_score(df)'
    },
    {
        'name': 't_score',
        'code': 'am.t_score(df)'
    },
    {
        'name': 'log_likelihood',
        'code': 'am.log_likelihood(df)'
    },
    {
        'name': 'simple_ll',
        'code': 'am.simple_ll(df)'
    },
    # point estimates of association strength
    {
        'name': 'min_sensitivity',
        'code': 'am.min_sensitivity(df)'
    },
    {
        'name': 'liddell',
        'code': 'am.liddell(df)'
    },
    {
        'name': 'dice',
        'code': 'am.dice(df)'
    },
    {
        'name': 'log_ratio',
        'code': 'am.log_ratio(df)'
    },
    # likelihood measures
    # ~2.5s for a ~25,000 rows on 8 threads
    # {
    #     'name': 'hypergeometric_likelihood',
    #     'code': 'am.hypergeometric_likelihood(df)'
    # },
    {
        'name': 'binomial_likelihood',
        'code': 'am.binomial_likelihood(df)'
    },
    # conservative estimates
    {
        'name': 'conservative_log_ratio',
        'code': 'am.conservative_log_ratio(df)'
    },
    # ~1.5s for a ~25,000 rows on 8 threads
    # {
    #     'name': 'conservative_log_ratio_poisson',
    #     'code': 'am.conservative_log_ratio(df, boundary="poisson")'
    # },
    # information theory
    {
        'name': 'mutual_information',
        'code': 'am.mutual_information(df)'
    },
    {
        'name': 'local_mutual_information',
        'code': 'am.local_mutual_information(df)'
    },
]

for code in codes:
    res = timeit.timeit(setup=setup, stmt=code['code'], number=iterations)
    print('Calculate {func} (iterations={iter}, df_size={size}): {res}'.format(
        iter=iterations, size=24168, res=res, func=code['name']
    ))
