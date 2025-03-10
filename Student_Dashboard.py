import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    department_columns = [f'{dept} Enrolled' for dept in department_filter]
    filtered_data = filtered_data[['Year', 'Term'] + department_columns]

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

# Ensure the department enrollment columns are numeric
department_columns = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']
filtered_data[department_columns] = filtered_data[department_columns].apply(pd.to_numeric, errors='coerce')

# Fill NaN values with 0 (you can change this if needed)
filtered_data[department_columns] = filtered_data[department_columns].fillna(0)

# Enrollment Breakdown by Department
st.subheader('Enrollment Breakdown by Department')
department_enrollment = filtered_data[['Year', 'Term'] + department_columns]

# Set 'Year' and 'Term' as index for the plot
fig, ax = plt.subplots(figsize=(12, 8))
department_enrollment.set_index(['Year', 'Term']).plot(kind='bar', stacked=True, ax=ax)

plt.title('Enrollment Breakdown by Department')
plt.ylabel('Number of Enrollments')
plt.xlabel('Year and Term')
st.pyplot(fig)

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

st.subheader('Retention Rate Trends Over Time')
# Plot retention rate trends over time
fig, ax = plt.subplots(figsize=(10, 6))

# Loop through each term to plot the retention rate
for term in df['Term'].unique():
    term_data = df[df['Term'] == term]
    ax.plot(term_data['Year'], term_data['Retention Rate (%)'], label=f'{term} Term')

# Set labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Retention Rate (%)')
ax.set_title('Retention Rate Trends Over Time')

# Show legend
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

st.subheader('Student Satisfaction Scores Over the Years')
# Plot student satisfaction scores over time
fig, ax = plt.subplots(figsize=(10, 6))

# Loop through each term to plot the student satisfaction scores
for term in df['Term'].unique():
    term_data = df[df['Term'] == term]
    ax.plot(term_data['Year'], term_data['Student Satisfaction (%)'], label=f'{term} Term')

# Set labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Student Satisfaction (%)')
ax.set_title('Student Satisfaction Scores Over the Years')

# Show legend
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

st.subheader('Enrollment Trends by Department')
# Plot retention rates by department
fig, ax = plt.subplots(figsize=(10, 6))

# Loop through each department to plot enrollment trends
for dept in ['Engineering', 'Business', 'Arts', 'Science']:
    ax.plot(df['Year'], df[f'{dept} Enrolled'], label=f'{dept} Enrollment')

# Set labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Number of Enrollments')
ax.set_title('Enrollment Trends by Department')

# Show legend
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

st.subheader('Student Satisfaction Trends by Department')
# Compare satisfaction levels by department
fig, ax = plt.subplots(figsize=(10, 6))

# Loop through each department to plot satisfaction trends
for dept in ['Engineering', 'Business', 'Arts', 'Science']:
    ax.plot(df['Year'], df['Student Satisfaction (%)'], label=f'{dept} Satisfaction')

# Set labels and title
ax.set_xlabel('Year')
ax.set_ylabel('Satisfaction (%)')
ax.set_title('Student Satisfaction Trends by Department')

# Show legend
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)

# Provide Key Findings & Actionable Insights
st.subheader('Key Findings & Actionable Insights')

# Example insights based on trends
average_retention_rate = filtered_data['Retention Rate (%)'].mean()
average_satisfaction = filtered_data['Student Satisfaction (%)'].mean()

# Retention Rate Insights
if average_retention_rate < 80:
    st.write("The average retention rate is below 80%. It may be necessary to investigate the causes of student attrition.")
else:
    st.write("The average retention rate is above 80%, indicating a relatively stable retention pattern.")

# Student Satisfaction Insights
if average_satisfaction < 75:
    st.write("The average student satisfaction is below 75%. Conducting surveys to understand student concerns and addressing them might help improve this.")
else:
    st.write("The average student satisfaction is above 75%, indicating generally positive student experiences.")

# Add additional insights for selected filters
if len(year_filter) > 0 and len(term_filter) > 0:
    st.write(f"Displaying data for the selected years: {', '.join(map(str, year_filter))} and terms: {', '.join(term_filter)}.")
else:
    st.write("No specific filters were applied. Displaying data for all available years and terms.")

# Optional: Display average retention and satisfaction rates
st.write(f"Average Retention Rate: {average_retention_rate:.2f}%")
st.write(f"Average Student Satisfaction: {average_satisfaction:.2f}%")
