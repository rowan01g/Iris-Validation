import pandas as pd
import numpy as np
import sys  

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def read_emringer_txt(filename):

	column_widths = [3, 5, 14] # due to fixed-width format, idenitifies the columns 
	df = pd.read_fwf(filename, widths = column_widths, header = None, skiprows = 1 )
	df = df.iloc[:, [0,1,2,]]
	df.columns = ["chain", "res_num", "emringer"]

	#add df values to list
	res_num = df["res_num"].tolist()
	emringer = df["emringer"].tolist()
	#conversion of list values into float and int
	res_num = [int(value) for value in res_num]
	emringer = [float(value) for value in emringer]

	return res_num, emringer

def write_emringer(res_num, emringer):
	#easy way to write list into text file ising numpy library 
	np.savetxt("res_num.txt", res_num, fmt = "%s")
	np.savetxt("emringer", emringer, fmt = "%s")

if len(sys.argv) == 2: 
	filename = sys.argv[1]
	res_num, emringer = read_emringer_txt(filename)
	write_emringer(res_num, emringer)