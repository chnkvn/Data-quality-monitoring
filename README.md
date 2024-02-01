
# Table of Contents

1.  [Data Creation](#org8b207ba)
2.  [API](#org3e34bf6)
3.  [Data Extraction](#orgae86475)
4.  [Transform Data](#org7c73672)
5.  [App](#orgb926869)



<a id="org8b207ba"></a>

# Data Creation

-   The first part of this project is to create fake data
-   It should be requestable with an API
-   Fake data creation using numpy


<a id="org3e34bf6"></a>

# API

-   Creation of an api with FastAPI
-   We create it to simulate the provider&rsquo;s API, here the API is deployed locally.
-   To launch the api locally, run `uvicorn app:app --reload`


<a id="orgae86475"></a>

# Data Extraction

The goal is to request the API to build our data.
You must deploy the API locally before running the script.


<a id="org7c73672"></a>

# Transform Data

-   Computation of the daily traffic by store
-   Computation of the moving average daily traffic for the same day of the week over the last 4 weeks
-   Computation of this moving average change from one week to the next
-   Export to parquet file


<a id="orgb926869"></a>

# App

-   Creation of a streamlit webapp
-   Choice of a store and a sensor to display its data and barplots about its most recent stats.
-   Run the app using `streamlit run app_streamlit.py`

