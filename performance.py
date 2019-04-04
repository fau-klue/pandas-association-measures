"""
Script to measure the performance
"""

import timeit

# Number of iterations
iterations = 1000

# Calculate contingency_table (iterations=10000): 8.784129375000703
# Calculate expected_frequencies (iterations=10000): 4.428030898001452


# code snippet to be executed only once
setup = """
import pandas as pd
import numpy as np
import association.measures as am

df = pd.DataFrame({'f1': np.random.randint(100, size=10),
                   'f2': np.random.randint(100, size=10),
                   'O11': np.random.randint(100, size=10),
                   'N': [100] * 10})
"""

# code snippet whose execution time is to be measured
code_1 = '''
df['O11'], df['O21'], df['O22'] = am.contingency_table(df['f1'], df['f2'], df['O11'], df['N'])
'''

code_2 = '''
df['E11'] = am.expected_frequencies(df['f1'], df['f2'], df['N'])
'''

res1 = timeit.timeit(setup=setup, stmt=code_1, number=iterations)
print('Calculate contingency_table (iterations={iter}): {res}'.format(iter=iterations, res=res1))
res2 = timeit.timeit(setup=setup, stmt=code_2, number=iterations)
print('Calculate expected_frequencies (iterations={iter}): {res}'.format(iter=iterations, res=res2))
