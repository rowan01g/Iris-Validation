#This script is run from the command console
#example: python read_cablam_text_file.py cablam_text_file.txt
#The script prompts you for two metrics from five and calculates the pearson correlation between them
#it also asks if you wish to see a scatter plot
from matplotlib import pyplot
from scipy.stats import pearsonr
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
	#convert str to float
	contour_level = [float(value) for value in contour_level]
	contour_type = [float(value) for value in contour_type]
	alpha_score = [float(value) for value in alpha_score]
	beta_score = [float(value) for value in beta_score]
	three_ten_score = [float(value) for value in three_ten_score]
	lists_of_metrics = [contour_level, contour_type, alpha_score, beta_score, three_ten_score]
	return lists_of_metrics

def prompt_for_lists(lists_of_metrics):
    """
    Prompts the user to select two lists to correlate
	Then calculates the pearson correlation 
    """
    lists_of_metrics_str = ["contour level", "contour type", "alpha score", "beta score", "three-ten score"]
    print("Select metrics to compare:")
    for i, lst in enumerate(lists_of_metrics_str):
        print(f"{i + 1}. {lst}")

    metric1_index = int(input("Enter the number for the first metric: ")) - 1
    metric2_index = int(input("Enter the number for the second metric: ")) - 1
    
    #checks that the numbers you have selected correspond to the lists_of_metrics
    if 0 <= metric1_index < len(lists_of_metrics) and 0 <= metric2_index < len(lists_of_metrics):
    	#calculates pearson correlation
        corr, _ = pearsonr(lists_of_metrics[metric1_index], lists_of_metrics[metric2_index])
        print(f"Pearson correlation between {lists_of_metrics_str[metric1_index]} and {lists_of_metrics_str[metric2_index]}: {corr:.3f}")
       
        #asks the user if they would like to produce a scatter plot 
        print("would you like to display a scatter plot?")
        scatter_y = input("(y/n)")
        if scatter_y == "y":
        	pyplot.scatter(lists_of_metrics[metric1_index], lists_of_metrics[metric2_index],
        		s = 15, c = '#1f77b4')
        	pyplot.show()
        else:
        	return lists_of_metrics[metric1_index]
        	return lists_of_metrics[metric2_index]
    else:
        print("Invalid list selection.")
        return None, None

if len(sys.argv) == 2:
	
	run_script = True 

	while run_script:
		filename = sys.argv[1]
		df = read_cablam_txt(filename)
		lists_of_metrics = create_metric_lists(df)
		prompt_for_lists(lists_of_metrics)
		print("Would you like to correlate two more metrics?") 
		again = input("(y/n)")
		if again == "n":
			run_script = False

else: 
	print("Please provide a file name" )


#contour_level: The contour level for protein behavior at which the residue falls, in fraction form (max of 1.0). Lower values indicate a more severe outlier. 0.05 is the default cutoff for outliers
#what is countour type??? 
#alpha_score: contour levels for expected alpha helix behavior. Higher values indicate greater confidence that the residue should be modeled as alpha helix. loose_alpha is the most reliable indicator, and its default cutoff is 0.001
#beta score: contour levels for expected beta behavior. Higher values indicate greater confidence that the residue should be modeled as beta sheet. regular_beta is the most reliable indicator, and its default cutoff is 0.001
#three-ten score: contour levels for expected three-ten helix behavior. Higher values indicate greater confidence that the residue should be modeled as three-ten helix. Its default cutoff is 0.001

