import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests

@st.cache_data
def load_data_s():
    response_s = requests.get('http://server:3000/get_skills')

    try:
        response_s.raise_for_status()
        data_s = response_s.json()
        data_s_df = pd.DataFrame(data_s)
        return data_s_df
    except requests.RequestException as e:
        st.error(f"Failed to retrieve data. Error: {e}")
    except ValueError as e:
        st.error(f"Failed to parse JSON. Error: {e}")

@st.cache_data
def load_data_t():
    response_t = requests.get('http://server:3000/get_titles')
    try:
        response_t.raise_for_status()
        data_t = response_t.json()
        data_t_df = pd.DataFrame(data_t)
        return data_t_df
        
    except requests.RequestException as e:
        st.error(f"Failed to retrieve data. Error: {e}")
    except ValueError as e:
        st.error(f"Failed to parse JSON. Error: {e}")


# Load the data from the API
merged_skills_df = load_data_s()
job_titles_df = load_data_t()

# Set background color and pastel colors
st.markdown(
    """
    <style>
        body {
            background-color: #f0f0f0;
        }
        .st-ec {
            background-color: #f0f0f0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

pastel_palette = sns.color_palette("pastel")

# Streamlit App
st.title('Dashboard')

# Sidebar
st.sidebar.header('Filter Options')

# Choose between skills and job titles
selected_chart = st.sidebar.radio('Choose Chart:', ['Skills', 'Job Titles'])

if selected_chart == 'Skills':
    # Skill count selector
    skill_count = st.sidebar.radio('Select Number of Skills to Display:', ['Top 10', 'Top 20', 'All'])

    # Filter by salary or trending
    filter_by = st.sidebar.radio('Filter By:', ['Salary', 'Trending'])

    # Main content for skills
    st.write(f"Showing {skill_count} Skills")

    # Display the skills based on the selected filter
    if filter_by == 'Salary':
        top_skills = merged_skills_df.sort_values(by='salary_avg', ascending=False).reset_index(drop=True)
        # Display the top skills based on the selected count
        if skill_count == 'Top 10':
            top_skills = top_skills.head(10)
        elif skill_count == 'Top 20':
            top_skills = top_skills.head(20)
        else:
            top_skills = top_skills

        fig = px.bar(top_skills, x='salary_avg', y='skill', orientation='h', text='salary_avg',
                     labels={'salary_avg': 'Average Salary'},
                     title='Top Skills by Salary',
                     color_discrete_sequence=['#9c27b0'])
    else:
        trending_skills = merged_skills_df.sort_values(by='count', ascending=False).reset_index(drop=True)
        # Display the top skills based on the selected count
        if skill_count == 'Top 10':
            trending_skills = trending_skills.head(10)
        elif skill_count == 'Top 20':
            trending_skills = trending_skills.head(20)
        else:
            trending_skills = trending_skills

        fig = px.bar(trending_skills, x='count', y='skill', orientation='h', text='count',
                     labels={'count': 'Mentions'},
                     title='Top Trending Skills',
                     color_discrete_sequence=['#ff4081'])

    # Customize the layout
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False, title=None), yaxis=dict(autorange='reversed', title=None))

    # Display the plot using Plotly
    st.plotly_chart(fig)

else:    

    # Main content for job titles
    st.write("Job Titles Graph")

    # Choose between count and salary for job titles
    selected_metric = st.sidebar.radio('Filter By:', ['Trending', 'Salary'])

    if selected_metric == 'Salary':
        
        top_jobs = job_titles_df.sort_values(by='salary_avg', ascending=False).reset_index(drop=True)
        # Display a bar chart of job title average salaries
        job_fig = px.bar(top_jobs, x='salary_avg', y='title', orientation='h', text='salary_avg',
                                       labels={'salary_avg': 'Average Salary'},
                                       title='Job Titles Average Salary',
                                       color_discrete_sequence=['#009688'])


    else:
        top_jobs = job_titles_df.sort_values(by='count', ascending=False).reset_index(drop=True)
        # Display a bar chart of job title counts
        job_fig = px.bar(top_jobs, x='count', y='title', orientation='h', text='count',
                                      labels={'count': 'Count'},
                                      title='Job Titles Count',
                                      color_discrete_sequence=['#009688'])
        

    # Customize the layout
    job_fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    job_fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False, title=None), yaxis=dict(autorange='reversed', title=None))

    # Display the job titles salary plot using Plotly
    st.plotly_chart(job_fig)
