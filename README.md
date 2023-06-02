# MDA-Project: Noise in Leuven

## Main Files and Folders Description:
- *create_venv.ps1*         : PowerShell script to create a virtual environment using the requirements.txt file
- *requirements.txt*        : Contains the required packages for the project
- *pull_and_merge_data.py*  : Script to download all the available data and merge them as much as possible based on the source (meteo data, noise events and noise percentiles are all merged in single files each, with data from the whole year. The noise levels data are too big to be handled in one single file, so it is aggregated by month)
- *utils*                   : Contains methods and classes to be used in other scripts

## How to start the project locally:
After cloning the repository:
- Run the *create_venv.ps1* file on the terminal to create the virtual environment (if on mac or linux, create the venv manually and run *pip install -r requirements.txt*).
- Run the full *pull_and_merge_data.py* to obtain ready-to-use parquet files with the project data (it takes a bit of time to run, as there is more than 18GB of data to be downloaded). This has to be ran before both the instructions below.
- Run the *prepare_data_analysis.py* to obtain the required data for the analysis and app (large data manipulations, also can take some time).
- Run the *prepare_data_model.py* to obtain the required data to train, test and evaluate the noise event prediction model.
- Run the *best_model.py* script to generate and store the figures for the app and the best model in a .pkl file.