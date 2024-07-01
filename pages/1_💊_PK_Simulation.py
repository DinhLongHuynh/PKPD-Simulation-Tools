# Import modules/packages
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

# Define function for the simulation
def pk_simulation(parameters): 
    sampling_points = np.arange(0,parameters['sampling_points']+0.1,0.1)
    time = np.array(sampling_points).reshape(1, len(sampling_points))
    CV_V = norm.rvs(loc=0, scale=parameters['Omega V'], size=parameters['Number of Patients'])
    V_variability = parameters['Population Volume of Distribution'] * np.exp(CV_V)
    V_var = V_variability.reshape(parameters['Number of Patients'], 1)
    CV_CL = norm.rvs(loc=0, scale=parameters['Omega CL'], size=parameters['Number of Patients'])
    CL_variability = parameters['Population Clearance'] * np.exp(CV_CL)
    CL_var = CL_variability.reshape(parameters['Number of Patients'], 1)
    CV_F = norm.rvs(loc=0, scale=parameters['Omega F'], size=parameters['Number of Patients'])
    F_variability = parameters['Population Bioavailability'] * np.exp(CV_F)
    F_var = F_variability.reshape(parameters['Number of Patients'], 1)
    ke_var = CL_var / V_var
    CV_resid = norm.rvs(loc=0, scale=parameters['Sigma Residual'], size=parameters['Number of Patients'])
    resid_var = np.array(CV_resid).reshape(parameters['Number of Patients'], 1)


    if ka_pop is None:
        concentration = ((parameters['Dose'] * F_var / V_var) * np.exp(np.dot(-ke_var, time)))+resid_var
    else:
        CV_ka = norm.rvs(loc=0, scale=omegaka, size=parameters['Number of Patients'])
        ka_variability = parameters['Population ka'] * np.exp(CV_ka)
        ka_var = ka_variability.reshape(parameters['Number of Patients'], 1)
        concentration = ((parameters['Dose'] * F_var * ka_var) / (V_var * (ka_var - ke_var)) * (np.exp(np.dot(-ke_var, time)) - np.exp(np.dot(-ka_var, time))))+resid_var

    global df_C, df_C_ln
    df_C = pd.DataFrame(concentration, columns=np.round(sampling_points,1))
    df_C.replace([np.inf, -np.inf], np.nan, inplace=True)
    concentration_ln = np.log(concentration)
    df_C_ln = pd.DataFrame(concentration_ln, columns=np.round(sampling_points,1))
    df_C_ln.replace([np.inf, -np.inf], np.nan, inplace=True)
    


    fig = go.Figure()
    for i in range(parameters['Number of Patients']):
        if parameters['logit']:
            pk_data = df_C_ln.iloc[i, :]
            fig.add_trace(go.Scatter(x=sampling_points, y=pk_data, mode='lines',showlegend=False))
            fig.update_yaxes(title_text='Log[Concentration] (mg/L)')
            if C_limit is not None:
                fig.add_hline(y=np.log(C_limit), line_dash="dash", line_color="red")
        else:
            pk_data = df_C.iloc[i, :]
            fig.add_trace(go.Scatter(x=sampling_points, y=pk_data, mode='lines',showlegend=False))
            fig.update_yaxes(title_text='Concentration (mg/L)')
            if parameters['C Limit'] is not None:
                fig.add_hline(y=C_limit, line_dash="dash", line_color="red")
    fig.update_xaxes(title_text='Time (h)')
    fig.update_layout(title='PK simulation')

    config = {
    'toImageButtonOptions': {
        'format': 'png', 
        'filename': 'PK_simulation',
        'height': None,
        'width': None,
        'scale': 5
    }}
    st.plotly_chart(fig,config=config)

#Page setup
st.set_page_config(page_title='Variability PK Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 PK Simulation")
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
if st.button("Run Simulation"):
    for name, value in parameters.items():
        if value is None: 
            continue
        elif value < 0: 
            warning_values.append(name)
    
    if len(warning_values) == 0:
        pk_simulation(parameters)
        st.subheader('Simulation Data')
        if parameters['logit']:
            st.data_editor(df_C_ln)
        else:
            st.data_editor(df_C)
    else: 
        st.error(f'**Parameter Mismatch:** {", ".join(warning_values)} is/are below 0. All defined parameters must be higher than 0.')
    