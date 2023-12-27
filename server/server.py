from fastapi import FastAPI, File, UploadFile
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as db
from sqlalchemy import create_engine
from sqlalchemy import *




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_skills")
def get_skills():
    engine = create_engine('sqlite:///../data/merged_skills_data.db')
    conn = engine.connect()
    metadata = db.MetaData()
    Skills = Table('skill', metadata, autoload_with=engine)
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



'''
def get_skills():
    # Read the CSV file
    skills_df = pd.read_csv('../data/merged_skills_data.csv')
    # Convert the DataFrame to JSON
    json_data = skills_df.to_dict(orient='records')
    return json_data
'''

@app.get("/get_titles")
def get_titles():
    engine = create_engine('sqlite:///../data/merged_titles_data.db')
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



'''
def get_titles():
    # Read the CSV file
    titles_df = pd.read_csv('../data/merged_titles_data.csv')
    # Convert the DataFrame to JSON
    json_data = titles_df.to_dict(orient='records')
    return json_data
'''


@app.get("/health")
def health_check():
    return {"status": "OK"}