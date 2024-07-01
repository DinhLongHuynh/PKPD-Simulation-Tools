# Import modules/packages
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm


# Define function for the simulation
def pd_simulation(parameters):
    Ebaseline_CV = norm.rvs(loc=0, scale=parameters['Omega Ebaseline'], size=parameters['Number of Patients'])
    Emax_CV = norm.rvs(loc=0, scale=parameters['Omega Emax'], size=parameters['Number of Patients'])
    EC50_CV = norm.rvs(loc=0, scale=parameters['Omega EC50'], size=parameters['Number of Patients'])
    hill_CV = norm.rvs(loc=0, scale=parameters['Omega Hill'], size=parameters['Number of Patients'])
    resid_CV = norm.rvs(loc=0, scale=parameters['Sigma Residual'], size=parameters['Number of Patients'])
    
    Ebaseline_var = (parameters['Population Ebaseline'] * np.exp(Ebaseline_CV)).reshape(parameters['Number of Patients'], 1)
    Emax_var = (parameters['Population Emax'] * np.exp(Emax_CV)).reshape(parameters['Number of Patients'], 1)
    EC50_var = (parameters['Population EC50'] * np.exp(EC50_CV)).reshape(parameters['Number of Patients'], 1)
    hill_var = (parameters['Population Hill'] * np.exp(hill_CV)).reshape(parameters['Number of Patients'], 1)
    resid_var = np.array(resid_CV).reshape(parameters['Number of Patients'], 1)
    
    sampling_conc = np.linspace(0, parameters['Sampling Conc'], 1000)
    conc_list = np.array(sampling_conc).reshape(1, len(sampling_conc))
    E_array = (Ebaseline_var + Emax_var * (conc_list ** hill_var) / (EC50_var + conc_list)) + resid_var
    global E_df
    E_df = pd.DataFrame(E_array, columns=np.round(sampling_conc,1))
    
    fig = go.Figure()
    for i in range(parameters['Number of Patients']):
        pd_data = E_df.iloc[i, :]
        fig.add_trace(go.Scatter(x=sampling_conc, y=pd_data, mode='lines', showlegend=False))
    if parameters['E Limit'] is not None:
        fig.add_hline(y=parameters['E Limit'], line_dash="dash", line_color="red")
    fig.update_yaxes(title_text='Effect')
    fig.update_xaxes(title_text='Concentration')
    fig.update_layout(title='PD simulation')

    config = {
        'toImageButtonOptions': {
            'format': 'png', 
            'filename': 'PD_simulation',
            'height': None,
            'width': None,
            'scale': 5
        }}
    st.plotly_chart(fig, config=config)


# Page setup 
st.set_page_config(page_title='Variability PD Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 PD Simulation")
st.write("""This page helps to visualize the PD profile of the drug, using the Emax-hill model.

It takes into account Emax, EC50, Ebaseline, and Hill to characterize the PD profile. 

The hill can be set to 1 to obtain the Emax model.
   
It also takes the omega arguments as the standard deviation of population distribution, representing unexplained interindividual variability.""")

# Take the information of PD profile 
col1, col2 = st.columns(2)
with col1: 
    Emax = st.number_input("Population Emax", value=6.00, format="%.3f")
    EC50 = st.number_input("Population EC50", value=5.00, format="%.3f")
    Ebaseline = st.number_input("Population Ebaseline", value=1.00, format="%.3f")
    hill = st.number_input("Population Hill Coefficient", value=1.00, format="%.3f")
with col2:
    omegaEmax = st.number_input("Omega Emax", value=0.00, format="%.3f")
    omegaEC50 = st.number_input("Omega EC50", value=0.00, format="%.3f")
    omegaEbaseline = st.number_input("Omega Ebaseline", value=0.00, format="%.3f")
    omegahill = st.number_input("Omega Hill", value=0.00, format="%.3f")

sig_resid = st.number_input("Sigma Residual", value=0.00, format="%.3f")
n_patients = st.number_input("Number of Patients", value=1)
E_limit = st.number_input("E Limit", value=None, format="%.3f")
sampling_conc = st.number_input("Concentrations Range", value=100)

# Summary of all parameters
parameters = {'Population Emax': Emax,
              'Population EC50': EC50,
              'Population Ebaseline': Ebaseline,
              'Population Hill': hill,
              'Omega Emax': omegaEmax,
              'Omega EC50': omegaEC50,
              'Omega Ebaseline': omegaEbaseline,
              'Omega Hill': omegahill,
              'Sigma Residual': sig_resid,
              'Number of Patients': n_patients,
              'E Limit': E_limit,
              'Sampling Conc': sampling_conc}

# Simulate the PD profile 
warning_values = []
if st.button("Run Simulation"):
    for name, value in parameters.items():
        if value is None: 
            continue
        elif value < 0: 
            warning_values.append(name)
    
    if len(warning_values) == 0:
        pd_simulation(parameters)
        st.subheader('Simulation Data')
        st.data_editor(E_df)
    else: 
        st.error(f'**Parameter Mismatch:** {", ".join(warning_values)} is/are below 0. All defined parameters must be higher than 0.')
    
