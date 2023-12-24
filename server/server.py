from fastapi import FastAPI, File, UploadFile
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware




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
    # Read the CSV file
    skills_df = pd.read_csv('../data/merged_skills_data.csv')
    # Convert the DataFrame to JSON
    json_data = skills_df.to_dict(orient='records')
    return json_data

@app.get("/get_titles")
def get_titles():
    # Read the CSV file
    titles_df = pd.read_csv('../data/merged_titles_data.csv')
    # Convert the DataFrame to JSON
    json_data = titles_df.to_dict(orient='records')
    return json_data

@app.get("/health")
def health_check():
    return {"status": "OK"}