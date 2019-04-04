"""
Script to measure the performance
"""

import timeit

# Number of iterations
iterations = 1000

# code snippet to be executed only once
setup = """
import pandas as pd
import numpy as np
import association.measures

df = pd.DataFrame({'f1': np.random.randint(100, size=10),
                   'f2': np.random.randint(100, size=10),
                   'O11': np.random.randint(100, size=10),
                   'N': [100] * 10})
"""

# code snippet whose execution time is to be measured
code1 = '''
df.apply(association.measures.expected_frequencies, axis=1)
'''

code2 = '''
df.apply(association.measures.contingency_table, axis=1)
'''

res1 = timeit.timeit(setup=setup, stmt=code1, number=iterations)
res2 = timeit.timeit(setup=setup, stmt=code2, number=iterations)

print('Calculate expected_frequencies (iterations={iter}): {res}'.format(iter=iterations, res=res1))
print('Calculate contingency_table (iterations={iter}): {res}'.format(iter=iterations, res=res2))
