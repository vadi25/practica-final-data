import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Load the merged skills data from the CSV file
merged_skills_df = pd.read_csv('data/merged_skills_data.csv')

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
st.title('Skills Dashboard')

# Sidebar
st.sidebar.header('Filter Options')


# Skill count selector
skill_count = st.sidebar.radio('Select Number of Skills to Display:', ['Top 10', 'Top 20', 'All'])


# Filter by salary or trending
filter_by = st.sidebar.radio('Filter By:', ['Salary', 'Trending'])


# Main content
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
fig.update_layout(showlegend=False, xaxis=dict(showticklabels=False, title=None),)

# Display the plot using Plotly
st.plotly_chart(fig)

