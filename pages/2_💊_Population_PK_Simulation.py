# Import modules/packages
import streamlit as st
from pkpd_sian.simulation import population_pk_simulation


#Page setup
st.set_page_config(page_title='Population PK Simulation', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 Population PK Simulation")

st.write("""This page helps to visualize the PK profile of the drug, using the one-compartment model.

It takes into account dose, ka, ke, F, V, and CL to characterize the PK profile.

It can used for modeling both IV and oral drugs.

It also takes the omega arguments as the standard deviation of the population distribution, representing unexplained interindividual variability.""")

# Take the information of PK profile 
col1, col2 = st.columns(2)
with col1:
    dose = st.number_input("Dose (mg)", value=100.0,format="%.3f")
    CL_pop = st.number_input("Population Clearance (L/h)", value=2.00,format="%.3f")
    V_pop = st.number_input("Population Volume of Distribution (L)", value=50.00,format="%.3f")
    ka_pop = st.number_input("Population absorption constant (h-1)", value=None,format="%.3f")
    F_pop = st.number_input("Population Bioavailability", value=1.00,format="%.3f")
with col2:
    n_patients = st.number_input("Number of Patients", value=1)
    omegaCL = st.number_input("Omega CL", value=0.00,format="%.3f")
    omegaV = st.number_input("Omega V", value=0.00,format="%.3f")
    omegaka = st.number_input("Omega ka", value=0.00,format="%.3f")
    omegaF = st.number_input("Omega F", value=0.00,format="%.3f")

sig_resid = st.number_input("Sigma Residual", value=0.0,format="%.3f")
C_limit = st.number_input("C Limit (mg/L)", value=None,format="%.3f")
sampling_points = st.number_input("Simulation range (h)", value=24, format = '%.1f')
logit = st.toggle("Log Transformation", value=False)

parameters = {'Dose': dose,
              'Population Clearance': CL_pop,
              'Population Volume of Distribution': V_pop,
              'Population ka': ka_pop,
              'Population Bioavailability': F_pop,
              'Number of Patients': n_patients,
              'Omega CL': omegaCL,
              'Omega V': omegaV,
              'Omega ka': omegaka,
              'Omega F': omegaF,
              'Sigma Residual': sig_resid,
              'C Limit':C_limit,
              'sampling_points': sampling_points,
              'logit':logit}

# Simulate the PK profile 
warning_values = []
if st.button("Run Simulation",key='One Compartment Simulation'):
    for name, value in parameters.items():
        if value is None: 
            continue
        elif value < 0: 
            warning_values.append(name)
    
    if len(warning_values) == 0:
        df_C, df_C_ln = population_pk_simulation(parameters)
        st.subheader('Simulation Data')
        if parameters['logit']:
            st.data_editor(df_C_ln)
        else:
            st.data_editor(df_C)
    else: 
        st.error(f'**Parameter Mismatch:** {", ".join(warning_values)} is/are below 0. All defined parameters must be higher than 0.')



    
