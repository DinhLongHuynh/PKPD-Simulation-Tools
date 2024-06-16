import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Define function for the single dose simulation
def pk_iv_dose(dose, time, ke, Vd):
    concentration = (dose/Vd) * (np.exp(-ke * time))
    return concentration

def pk_prolonged_iv_dose(dose, time, ke, Vd, infusion_duration):
    concentration = []
    for time_point in time:
        if time_point <= infusion_duration:
            # During infusion
            concentration.append((dose / (Vd * infusion_duration * ke)) * (1 - np.exp(-ke * time_point)))
        else:
            # After infusion
            concentration.append((dose / (Vd * infusion_duration * ke)) * (1 - np.exp(-ke * infusion_duration)) * np.exp(-ke * (time_point - infusion_duration)))
    return np.array(concentration)

def pk_non_iv_dose(dose, F, time, ke, ka, Vd):
    concentration = ((dose * F*ka)/(Vd*(ka-ke)))*(np.exp(-ke*time)-np.exp(-ka*time))
    return concentration


# Page setup
st.set_page_config(page_title='Multiple Dose PK', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 Multiple Dose PK Simulation")
st.write("""This page helps to visualize the drug's PK profile of the multiple-dosing regimen, using the one-compartmental model.

It takes the PK parameters, including ka, ke, and Vd to characterize the PK profile.

It also enables the define different dosing regimens by the buttons "Add IV Drug" or "Add Non-IV Drug. Each dose is characterized by the Dose Amount and the Starting Time Point. There are two types of dose:

- **IV drug:** the infusion duration can be used for the prolonged IV dose. If the normal IV dose is used, infusion duration should remain None.
- **Non-IV drug:** the total bioavailability is set equal to 1.0 by default. It can be changed when you have information.

""")

# Input the PK parameters
st.subheader('PK parameters')
col1, col2 = st.columns(2)
with col1:   
    ka = st.number_input("Absorption Rate Constant (h-1)", value=None,format="%.3f")
    ke = st.number_input("Elimination Rate Constant (h-1)", value=0.2,format="%.3f")
with col2:
    Vd = st.number_input("Volume of Distribution (L)", value=33.2,format="%.3f")
    simulation_range = st.number_input('Simulation Range (h)',value = 100.0, format="%.1f")

st.write('\n')
st.write('\n')

# Input the dosing regimen
st.subheader('Dose Regimen')
if 'dose_times' not in st.session_state:
    st.session_state.dose_times = []


col1, col2,col3 = st.columns(3)
with col1: 
    add_iv_dose = st.button("Add IV Dose")
with col2: 
    add_non_iv_dose = st.button("Add Non-IV Dose")


if add_iv_dose:
    st.session_state.dose_times.append({"time": 0, "dose": 0,"infusion_duration":None,"label":'iv'})
elif add_non_iv_dose:
    st.session_state.dose_times.append({"time": 0, "dose": 0,'F':0,"label":'non_iv'})


cols = st.columns(3)
for i, dose_time in enumerate(st.session_state.dose_times):
    with cols[i % 3]:
        if st.session_state.dose_times[i]["label"] == 'iv':
            st.write(f'**Dose {i+1} - IV Dose**')
            st.session_state.dose_times[i]["time"] = st.number_input(f"Start time (h)", value=0.0, key=f"time_{i}",format="%.1f")
            st.session_state.dose_times[i]["dose"] = st.number_input(f"Dose Amount (mg)", value=0.000, key=f"dose_{i}",format="%.3f")
            st.session_state.dose_times[i]["infusion_duration"] = st.number_input(f"Infusion Duration", value=None, key=f"infusion_duration_{i}",format="%.3f")
            st.write('\n')
            st.write('\n')
            st.write('\n')
        elif st.session_state.dose_times[i]["label"] == 'non_iv':
            st.write(f'**Dose {i+1} - Non-IV Dose**')
            st.session_state.dose_times[i]["time"] = st.number_input(f"Start time (h)", value=0.0, key=f"time_{i}",format="%.1f")
            st.session_state.dose_times[i]["dose"] = st.number_input(f"Dose Amount (mg)", value=0.000, key=f"dose_{i}",format="%.3f")
            st.session_state.dose_times[i]["F"] = st.number_input('Biovailability', value = 1.00, format="%.3f", key=f"F_{i}")
            st.write('\n')
            st.write('\n')
            st.write('\n')

# Simulation option
col1, col2, col3 = st.columns(3)
with col1:
    combine_profile = st.toggle('Combined PK Profiles',value=True)
with col2:
    each_dose_pk_profile = st.toggle('Each dose PK Profile',value=False)
with col3:
    run_simulation = st.button("Run Simulation")

# Run the simulation
if run_simulation:
    conc = {}
    add_conc = {}
    conc_each_dose = {}
    
    for i,dose_regimen in enumerate(st.session_state.dose_times):
        dose = dose_regimen['dose']
        start_time = dose_regimen['time']
        if dose_regimen['label'] == 'iv':
            if dose_regimen['infusion_duration'] == None:
                conc[i] = pk_iv_dose(dose=dose, time = np.arange(0,simulation_range-start_time+0.1, 0.1), ke=ke, Vd=Vd)
            elif dose_regimen['infusion_duration'] is not None:
                conc[i] = pk_prolonged_iv_dose(dose=dose, time = np.arange(0,simulation_range-start_time+0.1, 0.1), ke=ke, Vd=Vd,infusion_duration=dose_regimen['infusion_duration'])
            
        elif dose_regimen['label'] == 'non_iv':
            if ka is not None:
                conc[i] = pk_non_iv_dose(dose=dose, F=dose_regimen['F'], time = np.arange(0,simulation_range-start_time+0.1, 0.1), ke=ke, Vd=Vd,ka=ka)
            else:
                conc[i] = np.zeros((np.arange(0,simulation_range-start_time+0.1, 0.1).shape))
                st.error('You need to define ka for the simulation of Non-IV Drug.')
                break
        
        add_conc[i] = np.zeros((int(start_time/0.1)))
        conc_each_dose[i] = np.concatenate((add_conc[i],conc[i]),axis=0)
    
    simulate_conc = np.zeros((np.arange(0,simulation_range+0.1, 0.1).shape))
    for key, conc in conc_each_dose.items():
        simulate_conc += conc

    fig = go.Figure()
    if each_dose_pk_profile: 
        for i, conc_array in conc_each_dose.items():
            fig.add_trace(go.Scatter(x=np.arange(0, simulation_range+0.1, 0.1), y=conc_array, mode='lines', name=f'Dose {i+1}'))
    if combine_profile:
        fig.add_trace(go.Scatter(x=np.arange(0,simulation_range+0.1, 0.1), y=simulate_conc, mode='lines',name='Combine Profile'))
    fig.update_yaxes(title_text='Concentration] (mg/L)')
    fig.update_xaxes(title_text='Time (h)')
    fig.update_layout(title='PK simulation')
    st.plotly_chart(fig)
        
        

        
