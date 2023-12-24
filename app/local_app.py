import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests

@st.cache_data
def load_data_s():

    # Make a GET request to the FastAPI endpoint
    response_s = requests.get('http://0.0.0.0:3000/get_skills')

    try:
        response_s.raise_for_status()
        data_s = response_s.json()
        st.success("Data retrieved successfully!")
        st.write(data_s)
    except requests.RequestException as e:
        st.error(f"Failed to retrieve data. Error: {e}")
    except ValueError as e:
        st.error(f"Failed to parse JSON. Error: {e}")

@st.cache_data
def load_data_t(url_t:str):
    response_t = requests.get(url_t)
    if response_t.status_code == 200:
        st.write(response_t.json())
        '''        json_titles = response_t.json()
        job_titles_df = pd.DataFrame(json_titles)
        st.write(job_titles_df)
        '''
    else:
        st.error(f"Failed to retrieve CSV data. Status Code: {response_t.status_code}")



# load_data_t('http://0.0.0.0:3000/get_titles')

if st.button('Button'):
    load_data_s()