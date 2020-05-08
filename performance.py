"""
Script to measure the performance
"""

import timeit
import sys

# Number of iterations
iterations = 1000
if len(sys.argv) > 1:
    iterations = int(sys.argv[1])

# code snippet to be executed only once
setup = """
import pandas as pd
import association_measures.frequencies as fq
import association_measures.measures as am

df = pd.read_csv('tests/brown.csv')

df = df.join(fq.observed_frequencies(df))
df = df.join(fq.expected_frequencies(df))
"""

# code snippet whose execution time is to be measured
codes = [
    {
    'name': 'contingency_table',
    'code': '''
fq.observed_frequencies(df)
    '''
    },
    {
    'name': 'expected_frequencies',
    'code': '''
fq.expected_frequencies(df)
    '''
    },
    {
    'name': 'z_score',
    'code': '''
df['am'] = am.z_score(df)
    '''
    },
    {
    'name': 't_score',
    'code': '''
df['am'] = am.t_score(df)
    '''
    },
    {
    'name': 'mutual_information',
    'code': '''
df['am'] = am.mutual_information(df)
    '''
    },
    {
    'name': 'dice',
    'code': '''
df['am'] = am.dice(df)
    '''
    },
    {
    'name': 'log_likelihood',
    'code': '''
df['am'] = am.log_likelihood(df)
    '''
    },
]

for code in codes:
    res = timeit.timeit(setup=setup, stmt=code['code'], number=iterations)
    print('Calculate {func} (iterations={iter}, df_size={size}): {res}'.format(iter=iterations, size=24168, res=res, func=code['name']))
