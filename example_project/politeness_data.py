
import requests
import os
import pathlib
import polars as pl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class DownloadData():
    def __init__(self, data_url, target_path, data_file):
        """Download, preprocess, and plot politeness data from Bodo Winter

        Parameters
        ----------
        data_url : str 
            Url from where to download the data set.
        target_path : str
            local working directory where data should be stored.
        data_file : str
            name of file to which data should be saved.

        """
        self.target_path = target_path
        self.data_url = data_url
        self.data_file = data_file
        
    def __call__(self):

        # set current working directory   
        self.set_cwd(self.target_path)
        # download data set from specified url
        self.download_data(self.data_url, file_name = self.data_file)
        
    def set_cwd(self, target_path):
        """Set current working directory to desired local path

        Parameters
        ----------
        target_path : str
            local path that should be used as current working directory.

        Returns
        -------
        current_working_directory : str
            Prints current working directory.

        """
        # set the current working directory 
        os.chdir(target_path)
        
        # get current working directory
        current_wd = pathlib.Path.cwd()
        # check whether current working directory is indeed correct
        # if not: returns an error
        assert  current_wd == target_path, "Current working directory does not match with target directory"
    
    
    def download_data(self, data_url, file_name):
        """Download data from url

        Parameters
        ----------
        data_url : str
            URL from which data should be downloaded.
        file_name : str
            Name by which downloaded data file should be locally saved.

        Returns
        -------
        None.

        """
        # get data from url
        response = requests.get(data_url)
        with open(file_name, "wb") as file:
            file.write(response.content)
            

class PolitenessData():
    def __init__(self, data_file):
        """Download, preprocess, and plot politeness data from Bodo Winter

        Parameters
        ----------
        data_file : str
            name of file to which data should be saved.

        Returns
        -------
        summary_stats : DataFrame
            Summary statistics of the politeness data.
        plot : plt.plot
            Plot of the politeness data.

        """
        self.data_file = data_file
        
    def __call__(self):

        # read and preprocess data set
        df, summary_stats = self.data_preprocessed(self.data_file)
        # show summary statistics
        print(summary_stats)
        # plot data
        self.plot_data(df)
  
   
    # install pyarrow via pip install pyarrow
    def data_preprocessed(self, data_file):
        """Read and preprocess data 

        Parameters
        ----------
        data_file : str
            name of locally saved data file.

        Returns
        -------
        df_joined : polars.DataFrame
            Preprocessed data set with 84 observations and 6 variables (subject, 
            gender, scenario, attitude, frequency, mean_pitch).
        summaries : polars.DataFrame
            Mean pitch value grouped by attitude (informel, polite) and gender 
            (female, male).

        """
        # read data
        df = pl.from_pandas(pd.read_csv(data_file))
        # compute mean pitch values, grouped by gender and attitude
        summaries = df.group_by("attitude", "gender").agg(
            mean_pitch = pl.col("frequency").mean()
            )
        # join summaries and df columns together
        df_joined = df.join(summaries, on = ["gender", "attitude"], how = "inner")
        # relable attitude values
        df_joined = df_joined.with_columns(pl.lit(df["attitude"].map_dict({"pol": "polite", "inf": "informal"})).alias("attitude"))

        return (df_joined, summaries)
    
    def plot_data(self, df):
        """Scatterplot showing the relation between pitch in Hz and gender and 
        attitude.

        Parameters
        ----------
        df : polars.DataFrame
            Preprocessed data set with 84 observations and 6 variables (subject, 
            gender, scenario, attitude, frequency, mean_pitch).

        Returns
        -------
        matplotlib.plot

        """
        
        # create color sequence for grouping variable 
        # (to be passed into plot)
        cols = np.where(df["attitude"] == "polite", "lightblue", "orange")
        
        # initialie new plot
        fig, axs = plt.subplots(constrained_layout = True)
        # plot mean values
        axs.scatter(df["gender"],df["mean_pitch"], c = cols,edgecolors='black')
        # plot additionally individual observations
        sns.swarmplot(data = pd.DataFrame(df, columns = df.columns),
                    x = "gender", y = "frequency", 
                    hue = "attitude",
                    alpha = 0.4, ax=axs)
        # relable x-axis
        axs.set_xticklabels(labels = ["Female", "Male"])
        axs.set_ylabel("pitch in Hz")
        plt.show()
       


