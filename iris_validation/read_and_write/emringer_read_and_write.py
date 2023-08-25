import pandas as pd
import numpy as np
import sys  

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def read_emringer_txt(filename):

	column_widths = [3, 5, 14] # due to fixed-width format, idenitifies the columns 
	df = pd.read_fwf(filename, widths = column_widths, header = None)
	df = df.iloc[:, [0,1,2,]]
	df.columns = ["chain", "res_num", "emringer"]

	#sets elements in the df emringer column to 0 if it contains a string
	df['emringer'] = pd.to_numeric(df['emringer'], errors='coerce')
	df = df.fillna(0)
	print(df.iloc[0:20, 0:])

	#add df values to list
	res_num = df["res_num"].tolist()
	emringer = df["emringer"].tolist()
	#conversion of list values into float and int
	res_num = [int(value) for value in res_num]
	emringer = [float(value) for value in emringer]

	print(f'number of residues: {len(res_num)}')

	return res_num, emringer

def find_anomaly(res_num):
  prev = res_num[0] 
  for i, x in enumerate(res_num[1:]):
    if x != prev + 1:
      return i + 1
    prev = x
  return -1

def write_emringer(res_num, emringer):
	#easy way to write list into text file ising numpy library 
	np.savetxt("res_num.txt", res_num, fmt = "%s")
	np.savetxt("emringer.txt", emringer, fmt = "%s")

if len(sys.argv) == 2: 
	filename = sys.argv[1]
	res_num, emringer = read_emringer_txt(filename)
	print(find_anomaly(res_num))
	write_emringer(res_num, emringer)