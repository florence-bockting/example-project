import pathlib

from example_project.download_data import DownloadData
from example_project.politeness_data import PolitenessData

#%% Set variables
# here we use pathlib.PureWindowsPath s.t. we don't need to care about
# direction of backslashes
target_path = pathlib.PureWindowsPath(r"C:\Users\flobo\OneDrive\Dokumente\Phd-teaching\IntroPython\example-project\examples\data") 
# data set
data_url = "http://www.bodowinter.com/tutorial/politeness_data.csv"    
data_file = "pitch_data.csv"

#%% Download data
# download politeness data and save data file in target directory
data_download = DownloadData(data_url, target_path, data_file)
# set working directory
data_download.set_cwd(target_path)
# download data set
data_download.download_data(data_url, data_file)

#%% Preprocess data
# initialize class and create a new instance
pol_data = PolitenessData(data_file)
# preprocess data set
df, df_sum = pol_data.data_preprocessed(data_file)
# plot data 
pol_data.plot_data(df)
