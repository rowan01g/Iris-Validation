#reads a cablam text file and exports each metric column as its own sepearte text file for further correlation analyses

import pandas as pd 
import sys 


def read_cablam_txt(filename):
	"""reads the cablam txt file and converts into a dataframe then prints"""
	column_widths = [3, 3, 5, 20, 9, 9, 18, 8 ,8 ,8 ] # due to fixed-width format, idenitifies the columns 
	df = pd.read_fwf(filename, widths = column_widths, header = None, skiprows = 1 ) #  reads file and removes the column titles
	df = df.replace(":", "", regex = True) # removes ":" from values
	df_no_recc = df.iloc[:, [0,1,2,4,5,7,8,9]]
	df_no_recc.columns = ["chain", "residue#", "AA", "contour_level", "contour_type", "alpha_score", "beta_score", "three_ten_score"]
	return df

def create_metric_lists(df):
	"""takes the values of each column from the df and adds them to a list"""
	chain = df.iloc[:, 0].tolist()
	residue = df.iloc[:, 1].tolist()
	AA = df.iloc[:, 2].tolist()
	contour_level = df.iloc[:, 4].tolist()
	contour_type = df.iloc[:, 5].tolist()
	alpha_score = df.iloc[:, 7].tolist()
	beta_score = df.iloc[:, 8].tolist()
	three_ten_score = df.iloc[:, 9].tolist()
	#did not include chain, residue, AA - these are string values 

	#append two zeros to the beginning and three zeros to the end of the lists 
	#cabalm does not calculate values for the first 3 and last 3 residues
	#necessary for correlation with other metrics 
	metric_values = [contour_level, contour_type, alpha_score, beta_score, three_ten_score]

	#convert str to float
	contour_level = [float(value) for value in contour_level]
	contour_type = [float(value) for value in contour_type]
	alpha_score = [float(value) for value in alpha_score]
	beta_score = [float(value) for value in beta_score]
	three_ten_score = [float(value) for value in three_ten_score]

	
	return metric_values

def create_metric_dict(metric_values):
	metric_name = ["contour_level", "contour_type", "alpha_score", "beta_score", "three_ten_score"]
	pairs = zip(metric_name, metric_values)
	dict_of_metrics = dict(pairs)
	return dict_of_metrics

def export_metrics_as_txt(dict_of_metrics, filename):
	for metric_name, metric_values in dict_of_metrics.items():
		with open(filename +"_" + metric_name + ".txt", "w") as file:
			for value in metric_values:
				file.write(str(value) +"\n")


if len(sys.argv) == 2:

	filename = sys.argv[1]
	df = read_cablam_txt(filename)
	metric_values = create_metric_lists(df)
	dict_of_metrics = create_metric_dict(metric_values)
	export_metrics_as_txt(dict_of_metrics, filename)

else:
	print("Pleasqe provide a filename")



