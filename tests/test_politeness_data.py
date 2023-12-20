import pytest
import pandas as pd
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from example_project.politeness_data import PolitenessData

@pytest.fixture
def example_data_file(tmp_path):
    # Create a temporary CSV file with example data
    data = {
        'subject': [1, 2, 3],
        'gender': ['male', 'female', 'male'],
        'scenario': ['A', 'B', 'A'],
        'attitude': ['pol', 'inf', 'pol'],
        'frequency': [100, 150, 120],
        'mean_pitch': [200, 180, 220]
    }
    file_path = tmp_path / "example_data.csv"
    pd.DataFrame(data).to_csv(file_path, index=False)
    return str(file_path)

def test_data_preprocessed(example_data_file, capsys):
    # Initialize the PolitenessData class with the example data file
    politeness_data = PolitenessData(data_file=example_data_file)

    # Call the data_preprocessed method
    df_joined, summaries = politeness_data.data_preprocessed(example_data_file)

    # Perform assertions on the processed data
    assert isinstance(df_joined, pl.DataFrame)
    assert isinstance(summaries, pl.DataFrame)
    assert len(df_joined) == 3  # Assuming three rows in the example data
    assert len(summaries) == 2  # Assuming two unique combinations of attitude and gender

#%%

def test_plot_data(example_data_file, capsys):
    # Initialize the PolitenessData class with the example data file
    politeness_data = PolitenessData(data_file=example_data_file)

    # Call the data_preprocessed method to get the processed data
    df_joined, _ = politeness_data.data_preprocessed(example_data_file)

    # Call the plot_data method
    _, axs = politeness_data.plot_data(df_joined)

    # Perform assertions on the results
    assert isinstance(axs, plt.Axes)

    # Additional assertions for the plot characteristics
    assert len(axs.get_legend().get_texts()) == 2  # Expecting two legend items

