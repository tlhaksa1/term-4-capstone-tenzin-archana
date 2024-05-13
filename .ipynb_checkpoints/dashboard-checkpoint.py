### DS4PH Term 4 Capstone Project
# Group Members: Tenzin Lhaksampa and Archana Balan

# Import packages
import streamlit as st
import pandas as pd
import numpy as np
import folium
import plotly as py 
from importlib import import_module

# read in data
dat = pd.read_excel("matreatment_data.xlsx")
dat.head()
# check columns 
#print(dat.columns)
#print("\n", dat.shape)

# only retain numbers (not percentages)
dat = dat[dat['DataFormat'] == 'Number']

# convert cases reported to a numeric value
dat['Data'] = pd.to_numeric(dat['Data'], errors='coerce')

# rename and retain only relevant columns 
dat.rename({'LocationCode':'State', 
            'Category':'Type', 
            'TimeFrame':'Year', 
            'Data':'Case'}, 
           axis=1, 
           inplace=True)

# drop NA values
dat = dat.dropna()

# print data frame shape and column names
print(dat.columns)
print("\n", dat.shape)

# drop missing data 
dat = dat[dat['Type'] != 'Other/missing maltreatment type']
#dat.shape

# drop US data
dat = dat[dat['State'] != 'US']
#dat.shape

# Capitalize words in the 'Type' column using str.title() method
dat['Type'] = dat['Type'].str.title()
dat.head() # check

# merge "Neglect" and "Medical Neglect" into only "Neglect" 
dat['Type'] = dat['Type'].replace('Medical neglect', 'Neglect')
dat = dat.groupby(['State', 'Type', 'Year']).agg({'Case': 'sum'}).reset_index()

#print(dat.shape) # check shape
print("\n", dat.head()) # check dataset

# confirm data merge using MD as an example
md_dat = dat[(dat['State'] == 'MD') & (dat['Type'] == 'Neglect')]
md_dat.head(10)



## Total Maltreatment ##
# Calculate the total case count of child maltreatment across types
# Group by "State" and "Type", and sum the "Case" column
sum_dat = dat.groupby(['State', 'Year'])['Case'].sum().reset_index()

# generate the max number of cases 
max_value = dat['Case'].max()

# Display the resulting DataFrame
print(sum_dat.head())

print("\nHighest Total Maltreatment Case Count in the US:", max_value)

#print("\n", sum_dat.shape)



## Maltreatment Types ##
# data frames per maltreatment type 
emotional = dat[dat['Type'] == 'Emotional Abuse'][['State', 'Year', 'Case']]
physical = dat[dat['Type'] == 'Physical Abuse'][['State', 'Year', 'Case']]
sexual = dat[dat['Type'] == 'Sexual Abuse'][['State', 'Year', 'Case']]
neglect = dat[dat['Type'] == 'Neglect'][['State', 'Year', 'Case']]

print("Emotional Abuse\n", emotional.head(3))
print("\nPhysical Abuse\n", physical.head(3)) 
print("\nSexual Abuse\n", sexual.head(3))
print("\nNeglect\n", neglect.head(3))



### Streamlit App ###
import plotly.express as px

# Create choropleth map for total maltreatment over time 
fig = px.choropleth(sum_dat,
                    locations='State',  # Column containing state names
                    locationmode='USA-states',  # Set of locations match entries in the `State` column
                    color='Case',  # Column containing the values to be mapped
                    animation_frame='Year',  # Column containing the year
                    color_continuous_scale="Viridis_r",  # Color scale
                    labels={'Case': 'Case Count'},  # Label for color axis
                    scope='usa',  # Set to plot only USA states
                    title='Total Child Maltreatment Cases in the US, 2015-2022',  # Title of the plot
                   )

# Update layout 
fig.update_layout(
    coloraxis_colorbar=dict(title="Cases Count"),  # Title for color bar
    coloraxis_colorbar_ticks="outside",  # Display color bar ticks outside the color bar
    coloraxis=dict(cmin=0, cmax=80000),  # Minimum value for the color axis
    height=600,  # Set the height of the plot
    width=800,  # Set the width of the plot
)

# Show the map
fig.show()


# Prepare data by type of child maltreatment

# Define a list of abuse types
abuse_types = ['Emotional abuse', 'Physical abuse', 'Sexual abuse', 'Neglect']

# Create an empty dictionary to store DataFrames for each abuse type
abuse_data = {}

# Loop through each abuse type
for abuse_type in abuse_types:
    # Filter the DataFrame for the current abuse type and select desired columns
    abuse_data[abuse_type.lower().replace(' ', '_')] = dat[dat['Type'] == abuse_type][['State', 'Year', 'Case']]


# Create a choropleth map for each abuse type
for abuse_type in abuse_types:
    # Filter the DataFrame for the current abuse type and select desired columns
    abuse_data = dat[dat['Type'] == abuse_type][['State', 'Year', 'Case']]
    
    # Create a choropleth map for the current abuse type
    fig = px.choropleth(abuse_data,
                        locations='State',  # Column containing state names
                        locationmode='USA-states',  # Set of locations match entries in `locations`
                        color='Case',  # Column containing the values to be mapped
                        animation_frame='Year',  # Column containing the time frame (year)
                        color_continuous_scale="Viridis_r",  # Color scale
                        labels={'Case': 'Case Count'},  # Label for color axis
                        scope='usa',  # Set to plot only USA states
                        title=f'Child {abuse_type} Cases in the US, 2015-2022'  # Title of the plot
                        )
    # Update layout 
    fig.update_layout(
        coloraxis_colorbar=dict(title="Case Count"),  # Title for color bar
        coloraxis_colorbar_ticks="outside",  # Display color bar ticks outside the color bar
        coloraxis=dict(cmin=0, cmax=80000),  # Minimum value for the color axis
        height=600,  # Set the height of the plot
        width=800,  # Set the width of the plot
    )
    
    # Show the map
    fig.show()


## Streamlit app
import streamlit as st
import pandas as pd
import plotly.express as px

# Read data
dat = pd.read_excel("matreatment_data.xlsx")

# Clean the data
dat = dat[dat['DataFormat'] == 'Number']
dat['Data'] = pd.to_numeric(dat['Data'], errors='coerce')
dat.rename(columns={'LocationCode': 'State', 'Category': 'Type', 'TimeFrame': 'Year', 'Data': 'Case'}, inplace=True)
dat = dat.dropna()
dat['Type'] = dat['Type'].str.title()
dat['Type'] = dat['Type'].replace('Medical Neglect', 'Neglect')
dat = dat.groupby(['State', 'Type', 'Year']).agg({'Case': 'sum'}).reset_index()

# Define abuse types
abuse_types = ['Emotional Abuse', 'Physical Abuse', 'Sexual Abuse', 'Neglect']

# Calculate total maltreatment cases over time
sum_dat = dat.groupby(['State', 'Year'])['Case'].sum().reset_index()

# Streamlit app
st.write('''
# Child Maltreatment Cases in the US, 2015-2022
     
##### Cases Confirmed by Child Protective Services

### By Tenzin Lhaksampa and Archana Balan

### **Choose Maltreatment Type**

(Hover over states for more details)

''')


# Radio button to select maltreatment type
rb_total_or_type = st.radio("", ['Total Maltreatment'] + abuse_types)


if rb_total_or_type == 'Total Maltreatment':
    # Show total maltreatment cases over time
    fig_total = px.choropleth(sum_dat,
                              locations='State',
                              locationmode='USA-states',
                              color='Case',
                              animation_frame='Year',
                              color_continuous_scale='Viridis_r',
                              labels={'Case': 'Case Count'},
                              scope='usa',
                              )
    fig_total.update_layout(
        coloraxis_colorbar=dict(title="Cases Count"),
        coloraxis_colorbar_ticks="outside",
        coloraxis=dict(cmin=0, cmax=80000),
        height=600,
        width=800,
    )
    st.plotly_chart(fig_total)

else:
    # Show maltreatment cases by type over time
    st.write(f"### {rb_total_or_type} Cases Over Time")
    fig_type = px.choropleth(dat[dat['Type'] == rb_total_or_type],
                             locations='State',
                             locationmode='USA-states',
                             color='Case',
                             animation_frame='Year',
                             color_continuous_scale='Viridis_r',
                             labels={'Case': 'Case Count'},
                             scope='usa',
                             title=f'Child {rb_total_or_type} Cases in the US, 2015-2022'
                             )
    fig_type.update_layout(
        coloraxis_colorbar=dict(title="Cases Count"),
        coloraxis_colorbar_ticks="outside",
        coloraxis=dict(cmin=0, cmax=80000),
        height=600,
        width=800,
    )
    st.plotly_chart(fig_type)

st.write('''
**Data Source**: <a href="https://datacenter.aecf.org/data?location=USA#USA/1/0/char/0" target="_blank">The Annie E. Casey Foundation (AECF®) | KIDS COUNT Data Center</a>
''', unsafe_allow_html=True)

st.write('**Footnote**. Data for states that did not report any data or reported a low number of case may not display any information in the map.')  