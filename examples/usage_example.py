import pathlib
from example_project.download_data import DownloadData
from example_project.politeness_data import PolitenessData
   
# here we use pathlib.PureWindowsPath s.t. we don't need to care about
# direction of backslashes
target_path = pathlib.PureWindowsPath(r"C:\Users\flobo\OneDrive\Dokumente\Phd-teaching\example-project\examples\data") 
# data set
data_url = "http://www.bodowinter.com/tutorial/politeness_data.csv"    
data_file = "pitch_data.csv"

downloaded_data = DownloadData(data_url, target_path, data_file)
# set working directory
downloaded_data.set_cwd(target_path)

# download data set
downloaded_data.download_data(data_url, data_file)

# initialize class and create a new instance
pol_data = PolitenessData(data_file)

# preprocess data set
df, df_sum = pol_data.data_preprocessed(data_file)

# plot data 
_, axs = pol_data.plot_data(df)
