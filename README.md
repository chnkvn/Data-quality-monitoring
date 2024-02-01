
# Table of Contents

1.  [Objective](#orgbcde96c)
2.  [Installation](#org764fd0b)
3.  [Data Creation](#org45e78d3)
4.  [API](#org89d1b64)
5.  [Data Extraction](#org4a8b440)
6.  [Transform Data](#org4b61430)
7.  [App](#org19e3f16)
8.  [Potential next steps](#orga60d5e3)



<a id="orgbcde96c"></a>

# Objective

-   Illustrate a small process of data engineering
    -   Creation of fake data: stores that have several sensors to count visitors and send data hourly
    -   API creation and API requests for Data extraction
    -   Data transformation: creation of new stats (daily traffic, moving average for each weekday)
    -   WebApp creation for data visualisation
    -   Using workflows to check code syntax (black for PEP8)


<a id="org764fd0b"></a>

# Installation

-   Create a new virtual environment, using poetry, venv, conda
-   run `pip install -r requirements.txt`


<a id="org45e78d3"></a>

# Data Creation

-   The first part of this project is to create fake data
-   It should be requestable with an API
-   Fake data creation using numpy
-   Unit tests for Sensor and Store classes `python tests/test_sensors.py` `python tests/test_store.py`


<a id="org89d1b64"></a>

# API

-   Creation of an api with FastAPI
-   We create it to simulate the provider&rsquo;s API, here the API is deployed locally.
-   To launch the api locally, run `uvicorn app:app --reload`


<a id="org4a8b440"></a>

# Data Extraction

The goal is to request the API to build our data.
You must deploy the API locally before running the script.


<a id="org4b61430"></a>

# Transform Data

-   Computation of the daily traffic by store
-   Computation of the moving average daily traffic for the same day of the week over the last 4 weeks
-   Computation of this moving average change from one week to the next
-   Export to parquet file


<a id="org19e3f16"></a>

# App

-   Creation of a streamlit webapp
-   Choice of a store and a sensor to display its data and barplots about its most recent stats.
-   Run the app using `streamlit run app_streamlit.py`


<a id="orga60d5e3"></a>

# Potential next steps

-   Add alert if the value of a sensor is below a fixed threshold
-   Containerize the repo in a Docker container to run it on the cloud
-   Store the data on the cloud

