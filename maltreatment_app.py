import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def dashboard():
    st.title('Child Maltreatment Cases in the US, 2015-2022')
    st.write('''  
    ### By Tenzin Lhaksampa and Archana Balan

    ### **Choose Maltreatment Type**

    (Hover over states for more details)

    ''')

    

    # Load data
    dashboard_dat = load_dashboard_data()

    # Calculate total maltreatment cases over time
    dashboard_dat_sum = dashboard_dat.groupby(['State', 'Year'])['Case'].sum().reset_index()


    # Display Dashboard
    display_dashboard(dashboard_dat,dashboard_dat_sum)

  
def load_dashboard_data():
    return pd.read_csv('./data/dashboard_processed.csv')
   

def display_dashboard(dat, dat_all):
    # Define abuse types
    abuse_types = ['Emotional Abuse', 'Physical Abuse', 'Sexual Abuse', 'Neglect']

    # Radio button to select maltreatment type
    rb_total_or_type = st.radio("###", ['Total Maltreatment'] + abuse_types)

    if rb_total_or_type == 'Total Maltreatment':
    # Show total maltreatment cases over time
        st.write("### Total Child Maltreatmet Cases in the US, 2015-2022")
        fig_total = px.choropleth(dat_all,
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
        st.write(f"### Child {rb_total_or_type} Cases in the US, 2015-2022")
        fig_type = px.choropleth(dat[dat['Type'] == rb_total_or_type],
                                 locations='State',
                                 locationmode='USA-states',
                                 color='Case',
                                 animation_frame='Year',
                                 color_continuous_scale='Viridis_r',
                                 labels={'Case': 'Case Count'},
                                 scope='usa',
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
    **Data Source**: <a href="https://datacenter.aecf.org/data?location=USA#USA/1/0/char/0" target="_blank">The Annie E. Casey Foundation (AECF®) | KIDS COUNT Data Center</a>. Child maltreatment cases were confirmed by the Child Protective Services.
    ''', unsafe_allow_html=True)

    st.write('**Footnote**. Data for states that did not report any data or reported a low number of case may not display any information in the map.')  

def predicted_trends():
    st.title('Child Maltreatment Trends in the US')
    st.write('''  
    ### By Tenzin Lhaksampa and Archana Balan

    ##### Historical trends from 2015-2022 were used to predict trends for 2023-2025.

    ### **Choose State/Location**

    (Click on legend to view individual maltreatment type)

    ''')

    # Load data
    dat = load_predicted_data()

    # Display predicted trends
    display_predicted_trends(dat)

def load_predicted_data():
    # Read data
    return pd.read_csv("./data/maltreatment_predictions.csv")


def display_predicted_trends(dat):
    # Dropdown to select state
    state_selected = st.selectbox('', dat['Location'].unique())

    # Filter DataFrame based on selected state
    dat_st = dat[dat['Location'] == state_selected]

    # Melt DataFrame to have years as a single column
    dat_st_melted = pd.melt(dat_st, id_vars=['Location', 'Category'], var_name='Year', value_name='Cases')
    # Add a new column 'Type' indicating historical or predicted
    dat_st_melted['Data_Type'] = dat_st_melted['Year'].apply(lambda x: 'Historical' if int(x) <= 2022 else 'Predicted')

    # Define colors
    colors = {'Emotional abuse': '#b55cbd', 'Physical abuse': '#4161c9', 'Sexual abuse': '#9f323f', 'Neglect': '#c2c330'}

    # Create subplots
    plot_list = []

    for mt in dat_st_melted['Category'].unique():
        plot_df = dat_st_melted[dat_st_melted['Category'] == mt]
        for tp in dat_st_melted['Data_Type'].unique():
            if tp == 'Predicted':
                first_trace=False
            else:
                first_trace = True  # Flag to ensure only one legend item per category
            plot_df_tp = plot_df[plot_df['Data_Type'] == tp]
            plot_list.append(go.Bar(
                x=plot_df_tp['Year'],  # Categories on X-axis
                y=plot_df_tp['Cases'],  # Values on Y-axis
                name= mt,
                marker=dict(color=colors[mt]),
                legendgroup=mt,
                showlegend=first_trace  # Show legend only for the first trace
            ))

    # Combine the plots
    fig = go.Figure(data=plot_list)
    fig.update_layout(
        barmode='stack',
        title='Maltreatment Cases in ' + state_selected,
        titlefont=dict(color='black', size=22),
        xaxis=dict(
            title='Year',
            tickvals=dat_st_melted['Year'],  # Set tick positions to match the categories
            ticktext=dat_st_melted['Year'],
            titlefont=dict(color='black', size=18),
            tickfont=dict(color='black', size=16)
        ),
        yaxis=dict(title='Cases',
                   titlefont=dict(color='black', size=18),
                   tickfont=dict(color='black', size=16)
                   ),
        bargap=0.15,  # Gap between bars
        bargroupgap=0.1,  # Gap between groups of bars
        height=500,
        width=1200,  # Set width of the figure
        legend=dict(
            orientation="h",
            x=0.5,
            y=-0.3,
            # x=1.2,
            # y=0.3,
            xanchor="center",
            yanchor="bottom",
            font=dict(
                size=16,
                color="black"
            )
        )
    )

    # Add vertical dotted line
    midpoint = 2022.5
    fig.add_shape(
        type="line",
        x0=midpoint, x1=midpoint, y0=0, y1=2,
        xref='x', yref='paper',
        line=dict(color="grey", width=2, dash="dot")
    )

    # Add annotations (labels) to the left and right of the line

    fig.add_annotation(
        x=2018, y=1.1,  # Position slightly to the left of the line
        xref='x', yref='paper',
        text='Historical',
        showarrow=False,
        font=dict(color="black", size=18),
        align='right'
    )
    fig.add_annotation(
        x=2024, y=1.1,  # Position slightly to the right of the line
        xref='x', yref='paper',
        text='Predicted',
        showarrow=False,
        font=dict(color="black", size=18),
        align='left'
    )




    # Display the plot using Streamlit
    st.plotly_chart(fig, use_container_width=True)

def main():


    st.sidebar.title('Child Maltreatment in the US')

    page = st.sidebar.radio("", ['Dashboard of Cases', 'Predicted Trends in Cases'])

    if page == 'Dashboard of Cases':
        dashboard()
    elif page == 'Predicted Trends in Cases':
        predicted_trends()

if __name__ == "__main__":
    main()
