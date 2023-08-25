# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:00:24 2023

@author: rowan
"""
import pandas as pd
import numpy as np
import sys  

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)


def read_q_score(filename):
	file = pd.read_excel(filename, header = 0)
	df = pd.DataFrame(data = file)
	df = df.fillna(0)
	df = df.iloc[0:,1:6]

	# filter the df and slice the df from where the string 'Res #' appears - removing non data portion of excel file
	filter_idx = df[df['Est.Res.'].str.contains("Res #", na = False)].index[0]
	df = df.loc[filter_idx:]
	df = df.reset_index(drop = True)
	df.columns = df.iloc[0]
	df = df[1:]

	print(df.iloc[0:, 0:])

	Amino_acids = ["ALA", "ARG", "ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE",
				"LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL",
				"R37", "MN", "AGS", "HYP", "EEP", "DTH", "ADP", "AGS", "MG",
				 "HIC","NAG", "BMA", "DG", "DC", "DT", "DA", "ATP", "ACT", 	"NAD", "ZN"] #mutated residues 
	df = df[df.applymap(lambda x: any(val in str(x) for val in Amino_acids)).any(axis=1)]

	print(df.iloc[0:, 0:])

	#removes rows that repeat the headers for new chains 
	#indices = df[df['Res #'].str.contains('Res #', na = False)].index 
	#df.drop(index = indices, inplace = True)
	#df = df.reset_index(drop = True)

	#drop rows where the res number is 0
	empty_cell = 0
	indicies = df[df['Res #'] == empty_cell].index 
	df.drop(index = indicies, inplace = True)
	df = df.reset_index(drop = True)

	#drop rows where q_backbone, q_sidechain and q_residue all equal 0.
	#effectively removes rows where there is amino acid information missing

#	cols = ['Q_backBone', 'Q_sideChain', 'Q_residue']
#	indices = df[cols].eq(0).all(axis = 1)
#	df.drop(index = df[indices].index, inplace = True)
#	df = df.reset_index(drop = True)

	#take rows where there are lone amino acids, detached from the main chain
	#append these rows onto the end of the data frame
	#this allows for better correlation with other metrics
	#identify these residues with having no backbone Q-score

#	cols = ['Q_backBone', 'Q_sideChain']
#	indices = df[cols].eq(0).all(axis = 1)
#	append_indices = df[indices]
#	df.drop(index = df[indices].index, inplace = True)
#	df = df.append(append_indices, ignore_index = True)
#	df = df.reset_index(drop = True)

	#print(df)

	return df

def write_q_score(df):

	# add column elemnts to list
	res_num = df['Res #'].tolist()
	Q_backbone = df['Q_backBone'].tolist()
	Q_sidechain = df['Q_sideChain'].tolist()
	Q_residue = df['Q_residue'].tolist()

	metric_lists = [res_num, Q_backbone, Q_sidechain, Q_sidechain]

	print(f'\nthe length of the list "res number" is {len(res_num)}')

	#for metric_list in metric_lists:
	#	print(metric_list)

	np.savetxt('res_num.txt', res_num, fmt = "%s")
	np.savetxt('Q_backbone.txt', Q_backbone, fmt = "%s")
	np.savetxt('Q_sidechain.txt', Q_sidechain, fmt = "%s")
	np.savetxt('Q_residue.txt', Q_residue, fmt = "%s")


if len(sys.argv) == 2:
	filename = sys.argv[1] 
	df = read_q_score(filename)
	write_q_score(df)


