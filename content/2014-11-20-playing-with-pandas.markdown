Title: Playing with pandas
Published: True
Location: Santander, ES
Googlewebfonts: "Bree+Serif"
Tags: pandas, python

## Select all (but one) columns of a dataframe

A fast and easy way to select all columns rather than those included in a list:

    :::python
    df = pd.DataFrame(randn(8, 4), columns=['A', 'B', 'C', 'D'])
    
              A         B         C         D
    0  0.630446 -1.454207 -0.021687  1.095301
    1  0.374037  1.301607 -1.316152 -0.272031
    2  1.102625 -1.109953  1.058960  0.725778
    3  0.619485  1.500641 -0.370432 -0.356188
    4  0.323979  0.008434  0.616835 -0.632381
    5 -0.721451  0.852577  1.071660 -0.087884
    6  0.440051 -0.340789  0.602363 -0.442707
    7 -0.890141  1.062083  0.959767 -0.627261

    df[df.columns - ['B', 'C']]

              A         D
    0  0.630446  1.095301
    1  0.374037 -0.272031
    2  1.102625  0.725778
    3  0.619485 -0.356188
    4  0.323979 -0.632381
    5 -0.721451 -0.087884
    6  0.440051 -0.442707
    7 -0.890141 -0.627261
    
    # Another (more flexible) way to do the same:
    
    df.ix[:, df.columns - ['B', 'C']]


## Remove outliers (actually, clipping their values up to a maximum):

For this example, let's first add some outliers to the previous df:

    :::python

    for outlier in range(10):
       df[random.choice(df.columns)][randint(0, len(df))] *= 3.0

    df['ID'] = ['system%i' % randint(1, 4) for i in range(len(df))]
    
    df
              A         B         C         D       ID
    0  1.891338 -1.454207 -0.021687  9.857711  system2
    1  1.122112  1.301607 -1.316152 -0.272031  system3
    2  1.102625 -3.329858  1.058960  0.725778  system3
    3  0.619485  4.501923 -0.370432 -1.068563  system3
    4  0.323979  0.008434  0.616835 -0.632381  system2
    5 -0.721451  0.852577  1.071660 -0.087884  system3
    6  0.440051 -1.022366  1.807089 -0.442707  system2
    7 -0.890141  3.186248  0.959767 -0.627261  system1

For example, if we know that values must lie in the range [-2, 2] we would like
to clip all entries with an absolute value >2 to exactly +/- 2.00.

    :::python
    df[df.columns - ['ID']] = df[df.columns - ['ID']].clip(lower=-2.0, upper=2.0)

    df
              A         B         C         D       ID
    0  1.891338 -1.454207 -0.021687  2.000000  system2
    1  1.122112  1.301607 -1.316152 -0.272031  system3
    2  1.102625 -2.000000  1.058960  0.725778  system3
    3  0.619485  2.000000 -0.370432 -1.068563  system3
    4  0.323979  0.008434  0.616835 -0.632381  system2
    5 -0.721451  0.852577  1.071660 -0.087884  system3
    6  0.440051 -1.022366  1.807089 -0.442707  system2
    7 -0.890141  2.000000  0.959767 -0.627261  system1i

Or directly using np.where:

    :::python
    numeric = df.columns - ['ID']
    df[numeric] = np.where(abs(df[numeric]) > 2.0,
                               2.0*sign(df[numeric]), df[numeric])
  