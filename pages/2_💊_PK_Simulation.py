import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

# Core code of the page
def pk_simulation(dose=100, CL_pop=2, V_pop=50, ka_pop=None, F_pop=1, n_patients=1, sig_resid = 0, omegaCL=0, omegaV=0, omegaka=0, omegaF=0, 
                  C_limit=None, sampling_points=24, logit=False):
    sampling_points = np.linspace(0,sampling_points,1000)
    time = np.array(sampling_points).reshape(1, len(sampling_points))
    CV_V = norm.rvs(loc=0, scale=omegaV, size=n_patients)
    V_variability = V_pop * np.exp(CV_V)
    V_var = V_variability.reshape(n_patients, 1)
    CV_CL = norm.rvs(loc=0, scale=omegaCL, size=n_patients)
    CL_variability = CL_pop * np.exp(CV_CL)
    CL_var = CL_variability.reshape(n_patients, 1)
    CV_F = norm.rvs(loc=0, scale=omegaF, size=n_patients)
    F_variability = F_pop * np.exp(CV_F)
    F_var = F_variability.reshape(n_patients, 1)
    ke_var = CL_var / V_var
    CV_resid = norm.rvs(loc=0, scale=sig_resid, size=n_patients)
    resid_var = np.array(CV_resid).reshape(n_patients, 1)


    if ka_pop is None:
        concentration = ((dose * F_var / V_var) * np.exp(np.dot(-ke_var, time)))+resid_var
    else:
        CV_ka = norm.rvs(loc=0, scale=omegaka, size=n_patients)
        ka_variability = ka_pop * np.exp(CV_ka)
        ka_var = ka_variability.reshape(n_patients, 1)
        concentration = ((dose * F_var * ka_var) / (V_var * (ka_var - ke_var)) * (np.exp(np.dot(-ke_var, time)) - np.exp(np.dot(-ka_var, time))))+resid_var

    df_C = pd.DataFrame(concentration, columns=sampling_points)
    df_C.replace([np.inf, -np.inf], np.nan, inplace=True)
    concentration_ln = np.log(concentration)
    df_C_ln = pd.DataFrame(concentration_ln, columns=sampling_points)
    df_C_ln.replace([np.inf, -np.inf], np.nan, inplace=True)

    fig = go.Figure()
    for i in range(n_patients):
        if logit:
            pk_data = df_C_ln.iloc[i, :]
            fig.add_trace(go.Scatter(x=sampling_points, y=pk_data, mode='lines',showlegend=False))
            fig.update_yaxes(title_text='Log[Concentration] (mg/L)')
            if C_limit is not None:
                fig.add_hline(y=np.log(C_limit), line_dash="dash", line_color="red")
        else:
            pk_data = df_C.iloc[i, :]
            fig.add_trace(go.Scatter(x=sampling_points, y=pk_data, mode='lines',showlegend=False))
            fig.update_yaxes(title_text='Concentration (mg/L)')
            if C_limit is not None:
                fig.add_hline(y=C_limit, line_dash="dash", line_color="red")
    fig.update_xaxes(title_text='Time (h)')
    fig.update_layout(title='PK simulation')
    st.plotly_chart(fig)

#Page Set up
st.set_page_config(page_title='Variability PK Tools', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 PK Simulation")
st.write("""This page helps to visualize the PK profile of drug, using one compartment model.
    
It takes into account dose, ka, ke, F, V, and CL to characterize the PK profile. 
    
It can used for modelling both IV and oral drug.
    
It also take the omega arguments as the standard deviation of the population distribution, represent unexplained interindividual variability.""")

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

if st.button("Run Simulation"):
    pk_simulation(dose, CL_pop, V_pop, ka_pop, F_pop, n_patients, sig_resid, omegaCL, omegaV, omegaka, omegaF, C_limit, sampling_points, logit)