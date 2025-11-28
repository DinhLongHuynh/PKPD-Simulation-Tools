import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm


# Define the layout of the app
st.set_page_config(page_title='PKPD SiAn Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.sidebar.title('HOME')

# App introduction
st.title('💊 PKPD SiAn Tools')
st.caption('Version 2.0.1')
st.write("""PKPD SiAn Tools - PKPD Simulation and Analysis Tools 2.0.1 is the web application designed to help students and researchers to simulate and analyze different scenarios in clinical trials. The underlying mechanism of the simulation and analysis is in the *❓Helps* page. You can click the button below to see the mechanism.""")
st.link_button("❓Helps", "https://pkpd-sian-tools.streamlit.app/Helps")
st.write("""In version 2.0.1, the Simulation Tools are reorganized into Individual Simulation and Population Simulation. All Individual Simulations allow the flexible dosing regimen, while the Population PK Simulation now is available for single dose only.
This version also uses the generalized API in source code by the package pkpd_sian included in the same Repository.
         
The ongoing 2.1.0 version will be updated soon, which incorporates Physologically Based Pharmacokinetic Models. """)


# Sidebar options
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

- **Version 1.3.0:** The 💊 Combine Dosing Regimen page has been transformed into 💊 Multiple Dose PK Simulation, giving users the freedom to define the dosing regimen, including dose amount, starting time point, and infusion duration. 
             
- **Version 1.3.1:** All error messages were written as clear instructions so that users can easily fix simulation errors.
             
- **Version 1.4.0:** Multiple Compartmental Model is included, which allows to simulate more complex scenarios with consideration of one or more peripheral compartments.
             
- **Version 2.0.0:** Simulation Tools are reorganized into Individual Simulation and Population Simulation. All Individual Simulation allow the flexible dosing regimen, while the Population PK Simulation now is available for single dose only. This version also uses the generalized API in source code by the package pkpd_sian included in the same GitHub Repository.

- **Version 2.0.1:** The RMSE calculation is changed from mean_squared_error(squared=False) to root_mean_squared_error() due to the update of sklearn.metrics.''')


