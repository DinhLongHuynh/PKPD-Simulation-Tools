import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm


# Define the layout of the app
st.set_page_config(page_title='PKPD SiAn Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.sidebar.title('HOME')
st.title('💊 PKPD SiAn Tools')
st.caption('Version 1.3.0')
st.write("""PKPD SiAn Tools - PKPD Simulation and Analysis Tools 1.3.0 is the web application developed by Dinh Long Huynh, a current Master's Student at Uppsala University, Sweden.

This application helps students and researchers to simulate and analyze different scenarios in clinical trials. The simulation uses a one-compartmental model and the analysis can be conducted based on both non-compartment and one-compartment models. The underlying mechanism of the simulation and analysis is in the *❓Helps* page. You can click the button below to see the mechanism.""")
st.link_button("❓Helps", "https://pkpd-sian-tools.streamlit.app/Helps")
st.write("""In version 1.3.1, all error messages were written as clear instructions so that users can easily fix simulation errors.
         
The ongoing 1.4.0 version will be updated soon, which incorporates two new features, including automatical data cleaning tools, which helps draw several error warnings for the imported data and One-compartmental Analysis for multiple dosing regimen.""")

# Sidebar options
st.sidebar.success('Select a page above')
update_history = st.sidebar.checkbox('Check Update History',value=False)
st.write('\n')
st.write('\n')

if update_history:
    st.header('🗒 Update History')
    st.write('''- **Version 1.0.0:** The software was initialized with simulation tools only, for PK and PD, which take into account interindividual variability.

- **Version 1.0.1:** The Combine Dose Regimen simulation was updated, which enables the simulation of two different dosing regimens.

- **Version 1.1.0:** The PK analysis was introduced, with file importing, characterizing, and data visualization.

             
- **Version 1.1.1:** More optional manipulation of data visualization in PK analysis was updated.

- **Version 1.1.2:** The similarity algorithm to automatically assign the data columns title in PK analysis was introduced.

- **Version 1.2.0:** Non-compartmental and One-compartmental Analyses were introduced.

- **Version 1.2.1:** The PK analysis provided the user with the demo datasets, which can be used as the application trial.

- **Version 1.3.0:** The 💊 Combine Dosing Regimen page has been transformed into 💊 Multiple Dose PK Simulation, giving users the freedom to define the dosing regimen, including dose amount, starting time point, and infusion duration. ''')





