import pandas as pd
import numpy as np


df = pd.read_csv('./csv/0-2岁.csv')
df.drop(columns=[df.columns[0]], inplace=True)
df.fillna(value='', inplace=True)

def books(cat, fom, count):
	length = len(df)
	p = np.random.permutation(length)
	columns = df.columns

	retval = []
	for i in range(fom, count):
		x = {key:df.loc[p[i], key] for key in columns}
		retval.append(x)
	
	return retval





