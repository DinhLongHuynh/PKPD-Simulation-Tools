import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

# Define functions for simulation

def pk_combine_dose_regimen(dose_iv=500, infusion_duration=24, dose_im=1300, start_im=24, interval_dose_im=[0, 24, 48, 72, 96, 120], 
                            CL=7.5, Vd=33, ke=0.228, ka=0.028, F=1, time_range=170, IM_profile=False, IV_profile=False, combine_profile=True):
    ko = dose_iv / infusion_duration
    dose_im_F = dose_im * F

    time_points_mutual = np.arange(0, time_range, 1)
    time_point_infusion = time_points_mutual[0:(round(infusion_duration) + 1)]
    time_point_elim = time_points_mutual[(round(infusion_duration) + 1):]

    C_infusion = (ko / CL) * (1 - np.exp(-ke * time_point_infusion))
    C_elim = C_infusion[-1] * np.exp(-ke * (time_point_elim - time_point_infusion[-1]))

    concentrations_iv = np.concatenate((C_infusion, C_elim))

    time_points_im = time_points_mutual[start_im:] - start_im
    concentration_im = np.zeros(len(time_points_im))

    for dose_time in interval_dose_im:
        for i, t in enumerate(time_points_im):
            if t >= dose_time:
                concentration_im[i] += (dose_im_F / Vd) * (ka / (ka - ke)) * (np.exp(-ke * (t - dose_time)) - np.exp(-ka * (t - dose_time)))

    concentrations_im = np.concatenate((np.zeros(start_im), concentration_im))
    final_concentration = concentrations_iv + concentrations_im

    fig = go.Figure()
    if IM_profile:
        fig.add_trace(go.Scatter(x=time_points_mutual, y=concentrations_im, mode='lines', name='IM regimen'))
    if IV_profile:
        fig.add_trace(go.Scatter(x=time_points_mutual, y=concentrations_iv, mode='lines', name='IV regimen'))
    if combine_profile:
        fig.add_trace(go.Scatter(x=time_points_mutual, y=final_concentration, mode='lines', name='Combined regimen '))

    fig.update_layout(title='PK profile', xaxis_title='Time', yaxis_title='Concentration (mg/L)')
    st.plotly_chart(fig)


# Pages setup 
st.set_page_config(page_title='Combined Dose Regimen PK', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("PK Simulation of Combined Dosing Regimen IV and IM/Oral Drugs")
st.write("""This page helps to visualize the PK profile of the combined dosing regimen between:
             
- Prolonged infusion iv drugs: characterized by Dose IV and the Infusion Duration.
             
- IM or oral drugs: charaterized by Dose IM, Start IM, and Interval Dose IM.
             
    
Besides, the simulation also takes into account the PK parameters of the drugs, including CL, Vd, ke, ka, and F.
The time range of the simulation can be selected through Simulation Range.""")
    
col1, col2 = st.columns(2)
    
with col1:
    dose_iv = st.number_input("Dose IV (mg)", value=500.0,format="%.3f")
    infusion_duration = st.number_input("Infusion Duration (h)", value=24)
    dose_im = st.number_input("Dose IM (mg)", value=1300.0,format="%.3f")
    start_im = st.number_input("Start point IM (h)", value=0)
    interval_dose_im = st.text_input("Interval Dose IM (h)", "0, 24, 48, 72, 96, 120")
    interval_dose_im = [int(x) for x in interval_dose_im.split(",")]
with col2:
    CL = st.number_input("Clearance (L/h)", value=9.00,format="%.2f")
    Vd = st.number_input("Volume of Distribution (L)", value=50.00,format="%.2f")
    ke = st.number_input("Elimination Constant (h-1)", value=0.200,format="%.3f")
    ka = st.number_input("Absorption Constant (h-1)", value=0.020,format="%.3f")
    F = st.number_input("Bioavailability", value=1.00)
    
time_range = st.number_input("Simulation Range (h)", value=200)

col4, col5, col6 = st.columns(3)
with col4:
    IM_profile = st.toggle("Show IM Profile", value=False)
with col5:
    IV_profile = st.toggle("Show IV Profile", value=False)
with col6:
    combine_profile = st.toggle("Show Combined Profile", value=True)

if st.button("Run Simulation"):
    pk_combine_dose_regimen(dose_iv, infusion_duration, dose_im, start_im, interval_dose_im, CL, Vd, ke, ka, F, time_range, IM_profile, IV_profile, combine_profile)



