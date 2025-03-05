import os
import subprocess

# Install matplotlib if not already installed
subprocess.check_call([os.sys.executable, "-m", "pip", "install", "matplotlib"])

import matplotlib.pyplot as plt

import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv('university_student_dashboard_data.csv')

# Sidebar for filters
st.sidebar.header('Filters')
year_filter = st.sidebar.multiselect('Select Year(s)', df['Year'].unique())
term_filter = st.sidebar.multiselect('Select Term(s)', df['Term'].unique())
department_filter = st.sidebar.multiselect('Select Department(s)', ['Engineering', 'Business', 'Arts', 'Science'])

# Filter data based on user input
filtered_data = df.copy()
if year_filter:
    filtered_data = filtered_data[filtered_data['Year'].isin(year_filter)]
if term_filter:
    filtered_data = filtered_data[filtered_data['Term'].isin(term_filter)]
if department_filter:
    filtered_data = filtered_data[['Year', 'Term'] + [f'{dept} Enrolled' for dept in department_filter]]

# Title
st.title('University Student Trends Dashboard')

# Display the filtered data as a table
st.subheader('Filtered Data')
st.write(filtered_data)

# Key Metrics & KPIs
st.subheader('Key Metrics')
term_summary = filtered_data.groupby(['Year', 'Term']).agg({
    'Applications': 'sum',
    'Admitted': 'sum',
    'Enrolled': 'sum',
    'Retention Rate (%)': 'mean',
    'Student Satisfaction (%)': 'mean'
}).reset_index()

st.write(term_summary)

# Plots
st.subheader('Retention Rate Trends Over Time')
fig, ax = plt.subplots(figsize=(10, 6))
for term in filtered_data['Term'].unique():
    term_data = filtered_data[filtered_data['Term'] == term]
    ax.plot(term_data['Year'], term_data['Retention Rate (%)'], label=f'{term} Term')

ax.set_xlabel('Year')
ax.set_ylabel('Retention Rate (%)')
ax.set_title('Retention Rate Trends Over Time')
ax.legend()
st.pyplot(fig)

st.subheader('Student Satisfaction Trends Over Time')
fig, ax = plt.subplots(figsize=(10, 6))
for term in filtered_data['Term'].unique():
    term_data = filtered_data[filtered_data['Term'] == term]
    ax.plot(term_data['Year'], term_data['Student Satisfaction (%)'], label=f'{term} Term')

ax.set_xlabel('Year')
ax.set_ylabel('Student Satisfaction (%)')
ax.set_title('Student Satisfaction Trends Over Time')
ax.legend()
st.pyplot(fig)

# Enrollment Breakdown by Department
# Ensure numeric data for department enrollment columns
department_columns = [f'{dept} Enrolled' for dept in department_filter]

# Convert enrollment columns to numeric, coercing errors to NaN
filtered_data[department_columns] = filtered_data[department_columns].apply(pd.to_numeric, errors='coerce')

# Optionally, fill NaN values with 0 (or another method depending on your data)
filtered_data[department_columns] = filtered_data[department_columns].fillna(0)

# Plotting Enrollment Breakdown by Department
department_enrollment = filtered_data[['Year', 'Term'] + department_columns]

# Set 'Year' and 'Term' as index for the plot
department_enrollment.set_index(['Year', 'Term']).plot(kind='bar', stacked=True, figsize=(12, 8))

plt.title('Enrollment Breakdown by Department')
plt.ylabel('Number of Enrollments')
plt.xlabel('Year and Term')
st.pyplot()


# Comparison Between Spring vs. Fall Term
st.subheader('Comparison Between Spring vs. Fall Term')
spring_fall_comparison = filtered_data[filtered_data['Term'].isin(['Spring', 'Fall'])]

# Applications, Admissions, and Enrollments
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot for Applications, Admissions, and Enrollments
ax[0].plot(spring_fall_comparison['Year'], spring_fall_comparison['Applications'], label='Applications', marker='o')
ax[0].plot(spring_fall_comparison['Year'], spring_fall_comparison['Admitted'], label='Admitted', marker='x')
ax[0].plot(spring_fall_comparison['Year'], spring_fall_comparison['Enrolled'], label='Enrolled', marker='s')
ax[0].set_title('Applications, Admissions, and Enrollments (Spring vs Fall)')
ax[0].set_xlabel('Year')
ax[0].set_ylabel('Count')
ax[0].legend()

# Plot Retention Rate and Satisfaction
ax[1].plot(spring_fall_comparison['Year'], spring_fall_comparison['Retention Rate (%)'], label='Retention Rate', marker='o')
ax[1].plot(spring_fall_comparison['Year'], spring_fall_comparison['Student Satisfaction (%)'], label='Satisfaction', marker='x')
ax[1].set_title('Retention Rate and Satisfaction (Spring vs Fall)')
ax[1].set_xlabel('Year')
ax[1].set_ylabel('%')
ax[1].legend()

plt.tight_layout()
st.pyplot(fig)

# Provide Key Findings & Actionable Insights
st.subheader('Key Findings & Actionable Insights')
# Example insights based on trends
if filtered_data['Retention Rate (%)'].mean() < 80:
    st.write("The average retention rate is below 80%. It may be necessary to investigate the causes of student attrition.")
if filtered_data['Student Satisfaction (%)'].mean() < 75:
    st.write("The average student satisfaction is below 75%. Conducting surveys to understand student concerns and addressing them might help improve this.")
if len(year_filter) > 0 and len(term_filter) > 0:
    st.write(f"Displaying data for the selected years: {', '.join(map(str, year_filter))} and terms: {', '.join(term_filter)}.")

