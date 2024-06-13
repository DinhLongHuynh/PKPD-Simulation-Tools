import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm


# Define the layout of the app
st.set_page_config(page_title='PKPD SiAn Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.sidebar.title('HOME')
st.title('💊 PKPD SiAn Tools')
st.caption('Version 1.2.0')
st.write("""PKPD SiAn Tools - PKPD Simulation and Analysis Tools 1.2.0 is the web application developed by Dinh Long Huynh, a current Master's Student at Uppsala University, Sweden.

This application helps students and researchers to simulate and analyze different scenarios in clinical trials. The simulation uses a one-compartmental model and the analysis can be conducted based on both non-compartment and one-compartment models. The underlying mechanism of the simulation and analysis is in the *❓Helps* page. You can click the button below to see the mechanism.""")
st.link_button("❓Helps", "https://pkpd-sian-tools.streamlit.app/Helps")
st.write("""With the 1.2.0 version, the 💊 PK Analysis tab was updated with the new features of Non-compartmental Analysis and One-compartmental Analysis, which can take input from users and generate the PK parameters.
The ongoing 1.2.1 version will be updated soon, which incorporates the AI data cleaning tools, which can draw several error warnings for the imported data. """)


st.sidebar.success('Select a page above')






