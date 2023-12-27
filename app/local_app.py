import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import *


def get_titles():
    engine = create_engine('sqlite:///data/merged_titles_data.db')
    conn = engine.connect()
    metadata = db.MetaData()
    Skills = Table('title', metadata, autoload_with=engine)
    query = db.select(Skills)
    res= conn.execute(query)
    try:
        skills_df = pd.read_sql(query, conn)
        skills_df.head()
        keys=Skills.columns.keys()
        skills_df.columns = keys
        if skills_df.empty:
            return print("Error")
        elif skills_df is None:
            return print("Error")
        elif skills_df is not None:
            json_data=skills_df.to_dict(orient='records')
            return json_data
    except:
       return print("Error")

print(get_titles())

