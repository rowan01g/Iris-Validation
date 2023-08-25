#from the command console, pass two txt files containg values to be correlated
#calculate the pearson correlation 
#plot a scatter


from matplotlib import pyplot
from scipy.stats import pearsonr
import pandas as pd 
import sys 

# create df of both txt files 
def create_df(filename1, filename2):
	df = pd.read_csv(filename1)
	df2 = pd.read_csv(filename2)
	return df, df2

#vpass columns of df into lists
def create_lists(df, df2, filename1, filename2):
	list1 = df[filename1].tolist()
	list2 = df2[filename2].tolist()
	return list1, list2

def pearson_calc(list1, list2, filename1, filename2):
	list1 = np.array(list1)
	list2 = np.array(list2)
	corr, _ = pearsonr(list1, list2)
	print(f"the pearson correlation between {filename1} and {filename2} is: {corr:.3f}")
	return corr

def scatter(list1, list2):
	pyplot.scatter(list1, list2, s = 15)
	pyplot.show()

if len(sys.argv) == 3:
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    df, df2 = create_df(filename1, filename2)
    list1, list2 = create_lists(df, df2)
    pearson_corr = pearson_calc(list1, list2, filename1, filename2)
    scatter(list1, list2)















#pearson r 

#scattter plot 
