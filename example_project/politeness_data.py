import polars as pl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pyarrow # needed for the function pl.from_pandas() 

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
            name of locally saved data file..

        Returns
        -------
        df_joined : polars.DataFrame
            Preprocessed data set with 84 observations and 6 variables (subject, 
            gender, scenario, attitude, frequency, mean_pitch).
        summaries : polars.DataFrame
            Mean pitch value grouped by attitude (informal, polite) and gender 
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
        axs.scatter(df["gender"],df["mean_pitch"], c = cols, 
                    edgecolors='black')
        # plot additionally individual observations
        sns.swarmplot(data = pd.DataFrame(df, columns = df.columns),
                      x = "gender", y = "frequency", 
                      hue = "attitude",
                      alpha = 0.4, ax=axs)
        # relable x-axis
        axs.set_xticklabels(labels = ["Female", "Male"])
        axs.set_ylabel("pitch in Hz")
        return (fig, axs)