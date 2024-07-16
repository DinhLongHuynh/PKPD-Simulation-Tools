# Import modules/packages
import streamlit as st
from pkpd_sian.simulation import pd_simulation

# Page setup 
st.set_page_config(page_title='Population PD Simulation', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
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
        E_df = pd_simulation(parameters)
        st.subheader('Simulation Data')
        st.data_editor(E_df)
    else: 
        st.error(f'**Parameter Mismatch:** {", ".join(warning_values)} is/are below 0. All defined parameters must be higher than 0.')

