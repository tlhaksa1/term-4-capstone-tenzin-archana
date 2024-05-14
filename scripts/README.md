# Capstone project
## Team members: Tenzin Lhaksampa & Archana Balan
## Project: Child Maltreatment Cases in the US, 2015-2022


You should hand in the code for a data web app that you create based on an application of your interest. 

The project includes a 5 minute (maximum) video and one page (maximum) markdown readme file describing your project. Your MD readme file should include a link to the video that I can see or the video included in the repo. 

You name should be on your readme file, in the project video and in all code files as comments. 

The project due date is extremely firm for graduating seniors. 

## Grading rubric

The project must involve data, analysis – it can be prediction, regression, whatever, it has to involve data at some level (project will be rejected if this condition is failed to be met)  

There must be a streamlit app (the project will be rejected if this condition is not met) 

Each team must submit a write up in the form of your readme file, and a 5 minute video (the project will be rejected if this condition is not met). 

Then the project will be graded on: 

Is the app documented with instructions on use  

Effort, points will be deducted for low effort projects (like a simple BMI calculator or something like that) 

Correctness of results – was the data treated appropriately, was it cleaned appropriately, are there large conceptual or practical errors 

Communication – was the app well presented, do I have a sense of what it’s doing, is the web site and readme well presented? 



## Project Write-Up

- **Project Title**: Child Maltreatment in the US
  
- **Dataset**: Data for this capstone project is from the Annie E. Casey Foundation's [KIDS Count Data Center](https://datacenter.aecf.org/data?location=USA#USA/1/0/char/0).

- **Rationale**: Reporting requirements for child maltreatment (emotional abuse, physical abuse, sexual abuse, and neglect) vary by state. This dataset reports child maltreatment cases that can be compared across states, unlike other publicly available databases. Additionally, cases are confirmed by Child Protective Services (CPS). 

- **Objective**: Predict US child maltreatment cases 2023-2025 using historical data 2015-2022.

- **Prediction Analysis**: We used the child maltreatment 2015-2022 data to train 80% of the data and tested (validated) it on 20% of the data to predict cases in the next few years (2023-2025). We used a time-lagged linear regression model for each of the four types of child maltreatment. 

- **Streamlit App**
Instructions on using the app: In the Streamlit app, there are two pages. Users can interact with both pages in several ways. 
    1. **Dashboard**
        + On the dashboard page, we present a choropleth map of the US with corresponding colors for the child maltreatment case counts over time (2015-2022).
        + Hovering over each state will display more information on the year, state (denoted by a 2-letter code), and case count for that year.
        + Users can also click on radio buttons to display the type of child maltreatment with options for 'Total Maltreatment' (sum of the 4 types of maltreatment), 'Emotional Abuse', 'Physical Abuse', 'Sexual Abuse', and 'Neglect'.
        + At the bottom of the map, users can click the play button to see an animation of child maltreatment case counts by state and year; and click the stop button to view data for a given year.
        + The sliding bar at the bottom of the map allows users to view case counts for a specified year.
        + Lastly, the map has zooming in/out functionality. 
             
    2. **Prediction**: On the prediction page, we present a stacked bar graph of child maltreatment case counts from the Annie E. Casey Foundation's historical data (2015-2022) and the prediction data (2023-2025), based on the historical data. 
       + Users can select data to display by state using the dropdown menu. 
       + Each stacked bar graph displays the historical data and the predicted data per year. 
       + Each bar in the graph includes data on the types of child maltreatment and a legend specifying the type of data.
       + Users can hover over the bars to view more information on the historical and predicted case counts.
       + Finally, users can click on one type of child maltreatment in the legend to view historical and prediction information on that specified type of maltreatment.
      
-**Video Link**: https://youtu.be/Y71dCRQZVy4 
    
