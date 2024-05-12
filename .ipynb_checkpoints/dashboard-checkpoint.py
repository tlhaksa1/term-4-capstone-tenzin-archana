# Import packages
import streamlit as st
import pandas as pd
import numpy as np
import folium
import plotly as py 
from importlib import import_module
import plotly.graph_objects as go

# read in data
dat = pd.read_excel("maltreatment_data.xlsx")
dat.tail(10)

# only retain numbers (not percentages)
dat = dat[dat['DataFormat'] == 'Number']

# convert cases reported to a numeric value
dat['Data'] = pd.to_numeric(dat['Data'], errors='coerce')

# drop NA values
dat = dat.dropna()

# drop missing data 
dat = dat[dat['Category'] != 'Other/missing maltreatment type']

# Merge "Neglect" and "Medical Neglect" into only "Neglect" 
dat['Category'] = dat['Category'].replace('Medical neglect', 'Neglect')
dat = dat.groupby(['LocationType', 'Location', 'Category', 'TimeFrame', 'DataFormat']).agg({'Data': 'sum'}).reset_index()

# check dataset
dat.head(10)

# confirm data merge 
us_dat = dat[(dat['Location'] == 'United States') & (dat['Category'] == 'Neglect')]
us_dat.head(10)

    
# Display column names
print(dat.columns)


# Dashboard app 

def main():
    st.title("Child Maltreatment in the United States (2015-2022)")

    # Get user inputs for unit selection
    rb = st.radio("Select maltreatment type:", ("Emotional Abuse", "Physical Abuse", "Sexual Abuse", "Neglect", "Medical Neglect"), index=0)
    cb = st.checkbox ("Select Year:", ("2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"))
    
    # Add map
    # Dashboard app 

def main():
    st.title("Child Maltreatment by Type")

    # Get user input for year and maltreatment type
    year = st.radio ("Select year:", ("2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"), index=0)
    type = st.radio("Select maltreatment type:", ("Emotional Abuse", "Physical Abuse", "Sexual Abuse", "Neglect", "Medical Neglect"), index=0)

    

# Create the choropleth map

# Step 1: Get unique categories and years
unique_categories = dat['Category'].unique()
unique_years = dat['TimeFrame'].unique()

# Step 2: Create a subplot for each combination of category and year
fig = go.Figure()

for category in unique_categories:
    for year in unique_years:
        filtered_dat = dat[(dat['Category'] == category) & (dat['TimeFrame'] == year)]
        
        fig.add_trace(go.Choropleth(
            locations=filtered_dat['Location'],  # State names
            z=filtered_dat['Data'],  # Values to be mapped
            locationmode='USA-states',  # Set of locations match entries in `locations`
            colorscale='Viridis',
            colorbar_title='Count',
            text=filtered_dat['Category'],  # Additional text to display in hover
            name=f'{category} ({year})',  # Add category and year to subplot name
            visible=False  # Initially hide the subplot
        ))

# Update layout
fig.update_layout(
    title_text='US Map of Child Maltreatment by Category (2015-2022)',
    geo=dict(
        scope='usa',  # Set to plot only USA states
    ),
    updatemenus=[
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }
    ]
)

# Create frames for animation
frames = [dict(data=[go.Choropleth(visible=True if i == j * len(unique_years) else False) for i in range(len(unique_categories) * len(unique_years))]) for j in range(len(unique_years))]

# Add frames to animation
fig.frames = frames

# Show the map
fig.show()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()      
