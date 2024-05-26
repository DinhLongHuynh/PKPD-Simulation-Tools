import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm


# Core code 
def pd_simulation(Emax=6.43, EC50=5.38, Ebaseline=1, hill=1, n_patients=1, omegaEmax=0, omegaEC50=0, omegaEbaseline=0, omegahill=0, 
                  E_limit=None, sampling_conc=100):
    Ebaseline_CV = norm.rvs(loc=0, scale=omegaEbaseline, size=n_patients)
    Emax_CV = norm.rvs(loc=0, scale=omegaEmax, size=n_patients)
    EC50_CV = norm.rvs(loc=0, scale=omegaEC50, size=n_patients)
    hill_CV = norm.rvs(loc=0, scale=omegahill, size=n_patients)
    Ebaseline_var = (Ebaseline * np.exp(Ebaseline_CV)).reshape(n_patients, 1)
    Emax_var = (Emax * np.exp(Emax_CV)).reshape(n_patients, 1)
    EC50_var = (EC50 * np.exp(EC50_CV)).reshape(n_patients, 1)
    hill_var = (hill * np.exp(hill_CV)).reshape(n_patients, 1)
    sampling_conc = np.linspace(0,sampling_conc,1000)
    conc_list = np.array(sampling_conc).reshape(1, len(sampling_conc))
    E_array = Ebaseline_var + Emax_var * (conc_list ** hill_var) / (EC50_var + conc_list)
    E_df = pd.DataFrame(E_array, columns=sampling_conc)
    
    fig = go.Figure()
    for i in range(n_patients):
        pd_data = E_df.iloc[i, :]
        fig.add_trace(go.Scatter(x=sampling_conc, y=pd_data, mode='lines',showlegend=False))
    if E_limit is not None:
        fig.add_hline(y=E_limit, line_dash="dash", line_color="red")
    fig.update_yaxes(title_text='Effect')
    fig.update_xaxes(title_text='Concentration')
    fig.update_layout(title='PD simulation')
    st.plotly_chart(fig)


# Page setup 
st.set_page_config(page_title='Variability PD Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("PD Simulation")
st.write("""This page helps to visualize the PD profile of drug, using Emax_hill model.

It takes into account Emax, EC50, Ebaseline, and hill to characterize the PD profile. 

The hill can be set to 1 to obtain the Emax model.
   
It also take the omega arguments as the unexplained interindividual variability.""")

col1, col2 = st.columns(2)
with col1: 
    Emax = st.number_input("Population Emax", value=6.43,format="%.3f")
    EC50 = st.number_input("Population EC50", value=5.38,format="%.3f")
    Ebaseline = st.number_input("Population Ebaseline", value=1.00,format="%.3f")
    hill = st.number_input("Population Hill Coefficient", value=1.00,format="%.3f")
with col2:
    omegaEmax = st.number_input("Omega Emax", value=0.00,format="%.3f")
    omegaEC50 = st.number_input("Omega EC50", value=0.00,format="%.3f")
    omegaEbaseline = st.number_input("Omega Ebaseline", value=0.00,format="%.3f")
    omegahill = st.number_input("Omega Hill", value=0.00,format="%.3f")
n_patients = st.number_input("Number of Patients", value=1)
E_limit = st.number_input("E Limit", value=None,format="%.3f")
sampling_conc = st.number_input("Concentrations Range", value=100)

if st.button("Run Simulation"):
    pd_simulation(Emax, EC50, Ebaseline, hill, n_patients, omegaEmax, omegaEC50, omegaEbaseline, omegahill, E_limit, sampling_conc)
