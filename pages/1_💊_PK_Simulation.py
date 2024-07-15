# Import modules/packages
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from pkpd_sian.simulation import one_compartment_simulation, multiple_compartment_simulation


#Page setup
st.set_page_config(page_title='PK Simulation Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 PK Simulation")
one_compartment, multiple_compartment, physiology_compartment = st.tabs(['One Compartmental Simulation','Multiple Compartmental Simulation','Physiology-based Simulation'])

with one_compartment:
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
    sampling_points = st.number_input("Time range (h)", value=24)
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
            df_C, df_C_ln = one_compartment_simulation(parameters)
            st.subheader('Simulation Data')
            if parameters['logit']:
                st.data_editor(df_C_ln)
            else:
                st.data_editor(df_C)
        else: 
            st.error(f'**Parameter Mismatch:** {", ".join(warning_values)} is/are below 0. All defined parameters must be higher than 0.')



with multiple_compartment: 
    # Tab information
    st.write('''This page helps to simulate PK profile of a single dose using multiple compartmental model. The graphical representation of the model is describes by the figure below.
             
The model includes one central compartment responsible for drug absorption and elimination. Various parameters for this compartment include Absorption Rate Constant, Elimination Rate Constant, and Volume of Distribution.

The model also includes one or more peripheral compartments directly connect to the central one. Each peripheral compartment is characterized by its Initial Drug Concentration, k_in, and k_out.''')
    
    st.image('/Users/lod/Desktop/Projects/PKPD_Simulation_App/images/Multiple_Compartmental_Model.png')
    
    # Initialize session state
    if 'parameters' not in st.session_state:
        st.session_state.parameters = {}
    if 'compartment_count' not in st.session_state:
        st.session_state.compartment_count = 2  # Start from Compartment 2

    # Input for central Compartment
    st.subheader('Central Compartment')
    col1, col2 = st.columns(2)
    with col1: 
        Dose = st.number_input("Dose Amount (mg)", value=100.0,format="%.3f")
        conc_limit = st.number_input('C Limit (mg/L)',value=None, format='%.3f',key='Multiple Simulation')
        simulation_range = st.number_input('Simulation Range (h)',value=24.0, format="%.3f")
    
    with col2:
        ka = st.number_input("Absorption Rate Constant (h-1)", value=None,format="%.3f")
        ke = st.number_input("Elimination Rate Constant(h-1)",value = 0.2,format="%.3f")
        V_central = st.number_input("Volume of Distribution (L)",value = 33.0,format="%.3f")
    
    time = np.arange(0,simulation_range+0.1,0.1)
    st.session_state.parameters['Compartment 0'] = {'C0': Dose/V_central, 'k_in': None, 'k_out': ka, 'V': V_central}
    st.session_state.parameters['Compartment 1'] = {'C0': 0, 'k_in': ka, 'k_out': ke, 'V': V_central}
    st.write("\n")
    st.write("\n")
    st.write("\n")

    # Input for Peripheral Compartment
    st.subheader('Peripheral Compartments')
    add_peripheral = st.button("Add peripheral compartment")
        
    # Take input from users
    if add_peripheral: 
        new_compartment_key = f'Compartment {st.session_state.compartment_count}'
        st.session_state.parameters[new_compartment_key] = {'D0': 0.0, 'k_in': 0.0, 'k_out': 0.0, 'V': V_central}
        st.session_state.compartment_count += 1 

    cols = st.columns(3)
    for i in range(len(st.session_state.parameters)-2):
        with cols[i % 3]:
            st.write(f'**Peripheral {i+2}**')
            st.session_state.parameters['Compartment '+str(i+2)]["C0"] = st.number_input(f"Inital Drug Concentration (mg/L)", value=0.0, key=f"Do_{i+2}",format="%.3f")
            st.session_state.parameters['Compartment '+str(i+2)]["k_in"] = st.number_input(f"k_in (h-1)", value=0.0, key=f"kin_{i+2}",format="%.3f")
            st.session_state.parameters['Compartment '+str(i+2)]["k_out"] = st.number_input(f"k_out (h-1)", value=0.0, key=f"kout_{i+2}",format="%.3f")
            st.write("\n")
            st.write("\n")
            st.write("\n")

        
    #Run the simulation
    if st.button("Run Simulation",key='Multiple_Simulation'):
        if ka is not None:
            results = multiple_compartment_simulation(st.session_state.parameters,time,Dose,conc_limit,iv=False)      

        else: 
            results = multiple_compartment_simulation(st.session_state.parameters,time,Dose,conc_limit,iv=True)

        # Simulation data 
        results['C0'] = time
        simulation_data = pd.DataFrame(results)
        simulation_data.rename(columns={'C0': 'Time'}, inplace=True)

        st.subheader('Simulation Data')
        simulation_data_display = st.data_editor(simulation_data)



with physiology_compartment:
    st.info("This page is on the way to development. Please come back later.")




        


