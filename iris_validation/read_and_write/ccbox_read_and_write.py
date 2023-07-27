import pandas as pd
import numpy as np
import sys  

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def read_ccbox_txt(filename):

	column_widths = [6, 4, 5, 25 ] # due to fixed-width format, idenitifies the columns 
	df = pd.read_fwf(filename, widths = column_widths, header = None, skiprows = 1 )
	df = df.iloc[:, [0,1,2,3]]
	df.columns = ["chain", "res_num", "res_code", "ccbox"]

	#remove the end portion of the ccbox text file that is not part of the data
	filter_word = "CC per"
	slice_df = df[df["chain"] == filter_word].index[0]
	df = df.iloc[:slice_df]

	#add df values to list
	res_num = df["res_num"].tolist()
	ccbox = df["ccbox"].tolist()
	#conversion of list values into float and int
	res_num = [int(value) for value in res_num]
	ccbox = [float(value) for value in ccbox]

	return res_num, ccbox

def write_ccbox(res_num, ccbox):
	#easy way to write list into text file ising numpy library 
	np.savetxt("res_num.txt", res_num, fmt = "%s")
	np.savetxt("ccbox.txt", ccbox, fmt = "%s")

if len(sys.argv) == 2: 
	filename = sys.argv[1]
	res_num, ccbox = read_ccbox_txt(filename)
	write_ccbox(res_num, ccbox)