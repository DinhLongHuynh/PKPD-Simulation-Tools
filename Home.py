import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm


# Define the layout of the app
st.set_page_config(page_title='PKPD Simulation Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.sidebar.title('HOME')
st.title('PKPD Simulation Tools')
st.caption('Version 1.1.0')
st.write("""PKPD Simulation Tools 1.1.0 is the web application developed by Dinh Long Huynh, a current Master's Student at Uppsala University, Sweden

This application helps students and researchers to simulate different scenarios in clinical trials, using the pharmacokinetic one-compartment model.
         
With the 1.1.0 version, the application was updated with the new feature 💊 PK Analysis, which can take input from users, characterize it and generate several visualization plots.
The "Non-compartmental Analysis" and "One-compartmental analysis" are still in progress and will come soon.""")
st.sidebar.success('Select a page above')



