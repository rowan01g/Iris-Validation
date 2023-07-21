import pandas as pd
import sys 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def create_molprob_df(filename): 
	"""
	pass a .xlsx file to this function to strip the spreadsheet to the residue number, 
	residue 3-letter code, ??"High B"??, Ramachandran value, rotamer value and Cβ_deviation
	"""
	df = pd.read_excel(filename)
	df = df.drop(columns=["Alt", "Bond lengths", "Bond angles", "Cis Peptides", "Clash > 0.4Å" ])

	# Indices of rows to remove (every 2nd index row)
	indices_to_remove = [i for i in range(0, len(df), 2)]
	df = df.drop(indices_to_remove)
	df = df.reset_index(drop=True)

	# Indices of rows to remove (every 20th index row)
	indices_to_remove = [i for i in range(20, len(df), 21)]
	df = df.drop(df.index[indices_to_remove])
	df = df.reset_index(drop=True)

	#rename some columns
	df.rename(columns = {"#" : "Res_num"}, inplace = True)
	df.rename(columns = {"Cβ deviation" : "Cβ_deviation"}, inplace = True)

	#removes everything excpet numerical values
	df["Res_num"] = df["Res_num"].str.extract(r'(\d+\.\d+|\d+)')
	df["Ramachandran"] = df["Ramachandran"].str.extract(r'(\d+\.\d+|\d+)')
	df["Rotamer"] = df["Rotamer"].str.extract(r'(\d+\.\d+|\d+)')
	df["Cβ_deviation"] = df["Cβ_deviation"].str.extract(r'(\d+\.\d+|\d+)')

	# Removes all rows that dont contain one of the 20 amino acids and "R37"
	Amino_acids = ["ALA", "ARG", "ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE",
				"LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL", "R37"]
	df = df[df.applymap(lambda x: any(val in str(x) for val in Amino_acids)).any(axis=1)]

	#replaces all NaN (not a number) values in the df to 0, convert str to float
	df = df.fillna(0)

	return df

def create_molprob_list_dict(df):
	"""
	takes the df and creates a list containg the values of each column and then a dictionary
	"""
	#Passes all items from the columns of the df to lists 
	res_number = df["Res_num"].tolist() 
	ramachandran = df["Ramachandran"].tolist()
	rotamer = df["Rotamer"].tolist()
	cb_deviation = df["Cβ_deviation"].tolist()

	#conversion of str to int and flt
	df["Res_num"] = df["Res_num"].astype(int)
	df["Ramachandran"] = df["Ramachandran"].astype(float)
	df["Rotamer"] = df["Rotamer"].astype(float)
	df["Cβ_deviation"] = df["Cβ_deviation"].astype(float)

	# create a lists to be used as values and keys in dictionary
	metric_values = [res_number, ramachandran, rotamer, cb_deviation]
	metric_name = ["Res_num", "Ramachandran", "Rotamer","Cβ_deviation"]

	#create dictionary
	pairs = zip(metric_name, metric_values)
	dict_of_metrics = dict(pairs)
	return dict_of_metrics

def export_metrics_as_txt(dict_of_metrics):
	"""
	export each column in the df as txt files
	"""
	for metric_name, metric_values in dict_of_metrics.items():
		with open("1lf2_molprob" +"_" + metric_name + ".txt", "w") as file:
			for value in metric_values:
				file.write(str(value) +"\n")

if len(sys.argv) == 2:
	filename = sys.argv[1]
	df = create_molprob_df(filename)
	dict_of_metrics = create_molprob_list_dict(df)
	export_metrics_as_txt(dict_of_metrics)
else: 
	print("Please provide a filename")