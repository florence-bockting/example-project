import os
import pathlib
import requests
import pytest
from unittest.mock import patch, mock_open
from example_project.download_data import DownloadData  

@pytest.fixture
def download_data_instance(tmp_path):
    # Using a temporary directory for testing
    data_url = "http://www.bodowinter.com/tutorial/politeness_data.csv"  
    data_file = tmp_path / "test_data.csv"
    return DownloadData(data_url=data_url, target_path=str(tmp_path), data_file=str(data_file))

def test_set_cwd(download_data_instance, capsys):
    # Call the set_cwd method
    download_data_instance.set_cwd("examples")

    # Capture the printed output
    captured = capsys.readouterr()

    # Perform assertions on the printed output
    expected_path = pathlib.Path("examples")
    actual_path = pathlib.Path(captured.out.strip())

    # Ensure the actual path ends with the expected path
    assert actual_path.parts[-len(expected_path.parts):] == expected_path.parts
      
#%% 

@pytest.fixture
def download_data_instance(tmp_path):
    # Using a temporary directory for testing
    data_url = "http://www.bodowinter.com/tutorial/politeness_data.csv" 
    data_file = tmp_path / "test_data.csv"
    return DownloadData(data_url=data_url, target_path=str(tmp_path), data_file=str(data_file))

# Test the download_data method with different URLs
@pytest.mark.parametrize("data_url", ["https://osf.io/download/97g4j/", "https://osf.io/download/cvpmr"])
def test_download_data(download_data_instance, data_url, tmp_path):
    file_name = tmp_path / "test_data.csv"

    # Using the requests-mock library to mock the download process
    with patch("requests.get") as mock_get:
        mock_get.return_value.content = b"mocked data content"

        download_data_instance.download_data(data_url, file_name)

        # Check if the file was created and contains the expected content
        assert os.path.exists(file_name)
        with open(file_name, "rb") as file:
            content = file.read()
            assert content == b"mocked data content"

        mock_get.assert_called_once_with(data_url)


        