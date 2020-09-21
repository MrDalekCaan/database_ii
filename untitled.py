import pandas as pd
import numpy as np


df = pd.read_csv('./csv/0-2岁.csv')
df.drop(columns=[df._columns[0]], inplace=True)
df.fillna(value='', inplace=True)

def books(cat, fom, count, low, high):
	length = len(df)
	p = np.random.permutation(length)
	columns = df._columns

	retval = []
	end = count + fom
	end = min(length, end)
	for i in range(fom, end):
		x = {key:df.loc[p[i], key] for key in columns}
		retval.append(x)
	
	return retval





