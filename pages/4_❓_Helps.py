import streamlit as st
import pandas as pd

st.set_page_config(page_title='Helps', page_icon='❓', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title('Helps')
st.write('''This page contains further interpretation of the parameters and variables using in the different simulation applications.
         
The application provides the common standard units used in clinical trial, i.e. hour for time, mg for dose, mg/L for concentration.
However, the units can be flexible depends on users' case. In this scenario, users should keep in mind the units when import and interpret the simulation results.''')

st.header('Combine Dosing Reigmen Simulation PK')
st.caption('Further description of the parameters and variables used in the simulation:')
st.write('- **Dose IV (mg)**: The data type is **float**. This is the dose of intravenous drug.')
st.write('- **Infusion Duration (h)**: The data type is **integer**. This is the infusion time of the i.v. drugs. Because the scenario is prolonged infusion drugs, the value of Infusion Duration should be higher than 0 hour.')
st.write('- **Dose IM (mg)**: The data type is **float**. This is the dose of intramuscular drug in mg. However, it can be used for oral drugs as well.')
st.write('- **Start point IM (h)**: The data type is **integer**. This is the time point when the intramuscular drug is injected. If the starting point IM is set as 0 hour, that means we start the IM drug from the begining, at the same time with IV drug.')
st.write('- **Interval Dose IM (h)**: The data type is a **list of integer**. The values are the relative time points when you want to inject the i.m. drug. Because time points are relative, the first i.m. dose always starts at 0 hour. For example, if you want to inject triple dose a day of an i.m drug, the input should be: 0,8,16 hour.')
st.write('- **Clearance (L/h)**: The data type is **float**. This is the clearance.')
st.write('- **Volume of Distribution (L)**: The data type is **float**. This is the Volume of Distribution.')
st.write('- **Elimination Constant (h-1)**: The data type is **float**. This is the elimination rate constant, or ke.')
st.write('- **Absorption Constant (h-1)**: The data type is **float**. This is the absorption rate constant, or ka.')
st.write('- **Bioavailability**: The data type is **float**. This is the total bioavailability of drugs in the scale from 0 to 1. For example, if the bioavailability is 85%, the input value should be 0.85.')
st.write('- **Simulation Range (h)**: The data type is **integer**. This is the endpoint of the time range on the simulation plot. For example, if you input 100, the plot will show the simulation within the range between 0 and 100 hour.')

st.header('PK Simulation')
st.caption('Further description of the parameters and variables used in the simulation:')

st.header('PD Simulation')
st.caption('Further description of the parameters and variables used in the simulation:')

