import requests
import os
import pathlib

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
            