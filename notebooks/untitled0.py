# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 16:23:35 2014

@author: fernandezjm
"""
import pandas as pd
import itertools as it


pd.DataFrame._metadata = ['system', 'other']

df_a = pd.DataFrame({'sample_nr': [0, 1, 2, 3, 4, 5, 6], \
'val0': [2, 3, 6, 8, 6, 7, 8], 'val1': [1, 2, 4, 3, 1, 6, 3]})

df_a = df_a.set_index('sample_nr')
for c in df_a:
   df_a[c].system = 'system_a'
   df_a[c].other = len(df_a.columns)

df_b = pd.DataFrame({'sample_nr': [10, 11, 12, 13, 14, 15, 16], \
'val2': [5, 4, 5, 5, 5, 5, 6], 'val3': [4, 4, 6, 6, 8, 6, 6]})

df_b = df_b.set_index('sample_nr')
for c in df_b:
   df_b[c].system = 'system_b'
   df_b[c].other = len(df_b.columns)

df_c = pd.DataFrame({'sample_nr': [10, 11, 12, 13, 14, 15, 16], \
'val0': [1, 3, 2, 1, 3, 7, 2], 'val1': [0, 2, 3, 4, 1, 3, 1]})

df_c = df_c.set_index('sample_nr')
for c in df_c:
   df_c[c].system = 'system_c'
   df_c[c].other = len(df_c.columns)

df_d = pd.DataFrame({'sample_nr': [0, 1, 2, 3, 4, 5, 6], \
'val2': [8, 8, 7, 7, 8, 6, 5], 'val3': [4, 4, 6, 6, 8, 6, 6]})

df_d = df_d.set_index('sample_nr')
for c in df_d:
   df_d[c].system = 'system_d'
   df_d[c].other = len(df_d.columns)

def copy_metadata(source):
   """ Copies metadata from source columns to a list of dictionaries of type
       [{('column name', key): value}]
   """
   return [dict([((column, key), \
                  getattr(source[column], key, '')) \
                 for key in source._metadata]) for column in source]

metadata = copy_metadata(df_b)

for kv in itertools.chain.from_iterable(metadata):
    object.__setattr__(df_a[kv[0]], kv[1], )
[[object.__setattr__(df_a[kv[0]], kv[1], column[kv]) \
        for kv in column] for column in metadata]

# Concatenado tipo 'append', hay índices repetidos y NaN en los campos vacíos
df = pd.concat([df_a, df_c, df_b, df_d], axis=0)
for column in df_a:
   for value in column:
       print value
       
def upper(letra):
    return letra.upper()

funciona = lambda xs, ys: filter(lambda (x,y):x==y, upper(xs))
combine = lambda value, column: map(None, value*len(column), dupelms(column, len(value)))
dupelms = lambda lst, n: reduce(lambda s,t: s+t, map(lambda l, n=n: [l]*n, lst))


[[upper(value) for value in column] for column in df_a]