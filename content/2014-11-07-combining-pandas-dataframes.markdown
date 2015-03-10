Title: Combining pandas dataframes
Published: true
Tags: python, pandas, code
comments: true

Although still touching bases with pandas I came across a problem whose
answer was not found after skimming through Wes McKinney's [_"Python for Data
 Analysis"_](http://www.bookdepository.com/Python-for-Data-Analysis-Wes-McKinney/9781449319793)
book.

Long story short, starting with a bunch of CSV files transferred from a remote
system, a series of dataframes are produced one corresponding to each file.
These CSVs may contain hetereogeneous information from different components,
not necessarily for the very same period.

As an example, let's assume the index being the sample indicator. For simplicity
all the tests are done with these dataframes:


```python
df_a = pd.DataFrame({'sample_nr': [0, 1, 2, 3],
                     'val0': [2, 3, 6, 8],
                     'val1': [1, 2, 4, 3]})
df_a = df_a.set_index('sample_nr')

df_b = pd.DataFrame({'sample_nr': [10, 11, 12, 13],
                     'val2': [5, 4, 5, 5],
                     'val3': [4, 4, 6, 6]})
df_b = df_b.set_index('sample_nr')

df_c = pd.DataFrame({'sample_nr': [10, 11, 12, 13],
                     'val0': [1, 3, 2, 1],
                     'val1': [0, 2, 3, 4]})
df_c = df_c.set_index('sample_nr')

df_d = pd.DataFrame({'sample_nr': [0, 1, 2, 3],
                     'val2': [8, 8, 7, 7],
                     'val3': [4, 4, 6, 6]})
df_d = df_d.set_index('sample_nr')
```


    df_a:                         df_b:
               val0  val1                   val2  val3
    sample_nr                    sample_nr  
    0             2     1    10            5     4
    1             3     2    11            4     4
    2             6     4    12            5     6
    3             8     3    13            5     6


    df_c:                    df_d:
               val0  val1               val2  val3
    sample_nr                sample_nr
    10            1     0    0             8     4
    11            3     2    1             8     4
    12            2     3    2             7     6
    13            1     4    3             7     6



The result of glueing everything together is:

- {df_a, df_c} and {df_d, df_b} are concatenated along their axis (as the result
of `df_a.merge(df_c, how='outer')`).

- {df_a, df_d} and {df_c, df_b} are put together horizontally, as we could get
by running `df_a.join(df_d)`.


But... **what if** we have not a-priori clue of how each operands look like and
would like to perform a "glue *all together now*" operation?

#&lt;tl;dr/&gt;

At this point, I found two options:

1. Using `pd.concat` function.
2. Using `pd.combine_first` function.

The latter was at first glance the simplest choice:

```python
df = pd.DataFrame()
for _df in [df_a, df_b, df_c, df_d]:
    df = df.combine_first(_df)
```

which produces the desired output:

    df:
               val0  val1  val2  val3
    sample_nr
    0             2     1     8     4
    1             3     2     8     4
    2             6     4     7     6
    3             8     3     7     6
    10            1     0     5     4
    11            3     2     4     4
    12            2     3     5     6
    13            1     4     5     6


The first option was, however, my choice due to the way that input data is
obtained:

```python
df = pd.concat([dataframize(a_file) for a_file in files], axis=0)
```

Where `dataframize` simply takes an input CSV and returns a pd.DataFrame()
object.
The outcome still needs some adjustment (indices are duplicate and half of the 
values are empty).

    df:
               val0  val1  val2  val3
    sample_nr
    0             2     1   NaN   NaN
    1             3     2   NaN   NaN
    2             6     4   NaN   NaN
    3             8     3   NaN   NaN
    0           NaN   NaN     8     4
    1           NaN   NaN     8     4
    2           NaN   NaN     7     6
    3           NaN   NaN     7     6
    10            1     0   NaN   NaN
    11            3     2   NaN   NaN
    12            2     3   NaN   NaN
    13            1     4   NaN   NaN
    10          NaN   NaN     5     4
    11          NaN   NaN     4     4
    12          NaN   NaN     5     6
    13          NaN   NaN     5     6

So at the end this was the code used:

```python
df = pd.concat([dataframize(a_file) for a_file in files], axis=0)
# properly merge the columns and restore the metadata
_df = _df.groupby(_df.index).last()
```

The real reason of why choosing this and not `pd.combine_first`... maybe
in a future post.

