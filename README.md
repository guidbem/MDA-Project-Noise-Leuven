# MDA-Project: Noise in Leuven

## Main Files and Folders Description:
- *create_venv.ps1*         : PowerShell script to create a virtual environment using the requirements.txt file
- *requirements.txt*        : Contains the required packages for the project
- *pull_and_merge_data.py*  : Script to download all the available data and merge them as much as possible based on the source (meteo data, noise events and noise percentiles are all merged in single files each, with data from the whole year. The noise levels data are too big to be handled in one single file, so it is aggregated by month)
- *utils*                   : Contains methods and classes to be used in other scripts


## How to start the project locally:
After cloning the repository:
- Create a branch to start working on your analysis (on the terminal, use *git checkout -b branch_name*, ideally naming the branch based on the analysis, use a short name)
- Run the *create_venv.ps1* file on the terminal to create the virtual environment (if on mac or linux, create the venv manually)
- Run the full *pull_and_merge_data.py* to obtain ready-to-use parquet files with the project data (it takes a bit of time to run, as there is more than 18GB of data to be downloaded)
- When creating files for the analysis (like python scripts or jupyter notebooks), try to use names that are related to the analysis you are performing, makes it easier to avoid merge conflits in the future.


## Ideas:

- Separate the group in individual tasks:
    - 3/4 people focus on different questions/insights to be answered/extracted from the data.
    - 1 person focuses on writing the report and creating the slides
    - 1 person focuses on building the dashboard (streamlit or dash)
    - 1 person focuses on deploying the dashboard on cloud (AWS)

- Ideas for Questions/Insights:
    - Analyse the distribution of the noise events counts during the day grouped in different ways.
    - Analyse the effect of weather conditions on noise levels
    - Predict the type of noise based on the data
        - supervised learning (noise events as labels), with random forest, xgboost, etc..
        - can use as features the noise levels from previous seconds before and after the event time, like columns for t, t-1, t-2 and t+1, t+2, ... (number of seconds can be used as a hyperparameter to tune)
        - meteo data useful for features too
            - Temperature at QLC3
            - LC_RAD60 (radiation, weighted average on the hour)
            - LC_RAININ (rain intensity)
            - LC_WINDSPEED (wind speed)
            
        - featurize time data (day of the week, month/season, period of the day (noon, morning, etc...))
        - can use the certainty as weights when training or as part of the evaluation metric (incorrect predictions on uncertain labels are not that bad)


## How to obtain the necessary files and data for the app:

Run the code in the best_model.py file. It will generate and store the figures for the app. It will also store the best model in a .pkl file in order to use it to make predictions (put the labels) in a new set of data.