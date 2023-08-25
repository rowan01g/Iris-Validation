import numpy as np 
import pandas as pd
import sys 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def read_molprob_xlsx(filename): 
	"""
	pass a .xlsx file to this function to strip the spreadsheet to the residue number, 
	residue 3-letter code, High B, Ramachandran value, Rotamer value Cβ_deviation, CaBLAM score and Clashscore
	"""
	df = pd.read_excel(filename)
	df = df.drop(columns=["Alt", "Bond lengths", "Bond angles", "Cis Peptides",])

	#rename some columns
	df.rename(columns = {"High B" : "high_b"}, inplace = True)
	df.rename(columns = {"Clash > 0.4Å" : "clashscore"}, inplace = True)
	df.rename(columns = {"#" : "res_num"}, inplace = True)
	df.rename(columns = {"Cβ deviation" : "Cβ_deviation"}, inplace = True)

	#remove str from df 
	df["clashscore"] = df["clashscore"].str.extract(r'(\d+\.\d+|\d+)')
	df["CaBLAM"] = df["CaBLAM"].str.extract(r'(\d+\.\d+|\d+)')
	df["res_num"] = df["res_num"].str.extract(r'(\d+\.\d+|\d+)') 
	df["Ramachandran"] = df["Ramachandran"].str.extract(r'(\d+\.\d+|\d+)')
	df["Rotamer"] = df["Rotamer"].str.extract(r'(\d+\.\d+|\d+)')
	df["Cβ_deviation"] = df["Cβ_deviation"].str.extract(r'(\d+\.\d+|\d+)')
	
	#fills all nan values with 0 
	df = df.fillna(0)
	df = df.reset_index(drop = True)
	#removes all 0 valules in the res_num column - in other words removes empty cells from excel file
	#removes from RES NUMBER not Res - if there are missing residues these will be untouched in the df
	empty_cell = 0
	indicies = df[df['res_num'] == empty_cell].index 
	df.drop(index = indicies, inplace = True)
	df = df.reset_index(drop = True)

	df["Res"] = df["Res"].astype(str)
	Res = df["Res"].tolist()
	print(len(Res))
	Res = list(dict.fromkeys(Res))
	print(f'list of unique Amino acid 3 letter residues in this protein:')
	for aa in Res:
		print(f'\t-{aa}')

	# Removes all rows that dont contain one of the 20 amino acids and "R37"
	Amino_acids = ["ALA", "ARG", "ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE",
				"LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL",
				"R37", "MN", "AGS", "HYP", "EEP", "DTH", "ADP", "AGS", "MG",
				 "HIC","NAG", "BMA", "DG", "DC", "DT", "DA", "ATP", "ACT", 	"NAD", "ZN"] #mutated residues 
	df = df[df.applymap(lambda x: any(val in str(x) for val in Amino_acids)).any(axis=1)]

	#print(df)
	#print(df.iloc[0:-1, 0:])
	print('Dataframe:')
	print(df.iloc[0:50, 0:])
	print(len(df['res_num']))

	return df

def write_molprob(df):
	"""
	takes the df and creates a list containg the values of each column and then a dictionary
	then writes all lists to txt files for correlation
	"""
	#conversion of metric values - str to int and flt
	df["high_b"] = df["high_b"].astype(float)
	df["clashscore"] = df["clashscore"].astype(float)
	df["CaBLAM"] = df["CaBLAM"].astype(float)
	df["res_num"] = df["res_num"].astype(int)
	df["Ramachandran"] = df["Ramachandran"].astype(float)
	df["Rotamer"] = df["Rotamer"].astype(float)
	df["Cβ_deviation"] = df["Cβ_deviation"].astype(float)

	#Passes all items from the columns of the df to lists
	high_b = df["high_b"].tolist()
	clashscore = df["clashscore"].tolist()
	cablam = df["CaBLAM"].tolist()
	res_number = df["res_num"].tolist() 
	ramachandran = df["Ramachandran"].tolist()
	rotamer = df["Rotamer"].tolist()
	cb_deviation = df["Cβ_deviation"].tolist()

	# create a lists to be used as values and keys in dictionary
	metric_values = [high_b, clashscore, cablam, res_number, ramachandran, rotamer, cb_deviation]
	metric_name = ["high_b", "clashscore", "cablam","res_num", "ramachandran", "rotamer","Cβ_deviation"]

	#create dictionary
	pairs = zip(metric_name, metric_values)
	dict_of_metrics = dict(pairs)

	#write all metrics to txt files
	for name, values in dict_of_metrics.items():
		array = np.array(values)
		with open(name+".txt", "w") as f:
			for res, value in zip(res_number, array):
				f.write(f"{value}\n")

	print(f'Molprobity metrics:\n')
	for name, values in dict_of_metrics.items():
		print(f'\t-{name.title()}')
	print('\nwritten to file')
		
if len(sys.argv) == 2:
	filename = sys.argv[1]
	df = read_molprob_xlsx(filename)
	write_molprob(df)
else: 
	print("Please provide a filename")