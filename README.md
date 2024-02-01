
# Table of Contents

1.  [Objective](#org2b76a70)
2.  [Installation](#orgc039987)
3.  [Data Creation](#org33d5ce6)
4.  [API](#orgcd3df2f)
5.  [Data Extraction](#org17098fd)
6.  [Transform Data](#orgfdb4287)
7.  [App](#org72d8f56)



<a id="org2b76a70"></a>

# Objective

-   Illustrate a small process of data engineering
    -   Creation of fake data
    -   API creation and API requests
    -   Data Extraction
    -   Data transformation
    -   WebApp creation for dava visualisation
    -   Using workflows to check code syntax (black)


<a id="orgc039987"></a>

# Installation

-   Create a new virtual environment, using poetry, venv, conda
-   run `pip install -r requirements.txt`


<a id="org33d5ce6"></a>

# Data Creation

-   The first part of this project is to create fake data
-   It should be requestable with an API
-   Fake data creation using numpy
-   Unit tests for Sensor and Store classes `python tests/test_sensors.py` `python tests/test_store.py`


<a id="orgcd3df2f"></a>

# API

-   Creation of an api with FastAPI
-   We create it to simulate the provider&rsquo;s API, here the API is deployed locally.
-   To launch the api locally, run `uvicorn app:app --reload`


<a id="org17098fd"></a>

# Data Extraction

The goal is to request the API to build our data.
You must deploy the API locally before running the script.


<a id="orgfdb4287"></a>

# Transform Data

-   Computation of the daily traffic by store
-   Computation of the moving average daily traffic for the same day of the week over the last 4 weeks
-   Computation of this moving average change from one week to the next
-   Export to parquet file


<a id="org72d8f56"></a>

# App

-   Creation of a streamlit webapp
-   Choice of a store and a sensor to display its data and barplots about its most recent stats.
-   Run the app using `streamlit run app_streamlit.py`

