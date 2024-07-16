import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pkpd_sian.simulation import pk_iv_dose, pk_prolonged_iv_dose, pk_non_iv_dose,multiple_compartment_simulation


# Page setup
st.set_page_config(page_title='Multiple Dose PK Simulation', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 PK Simulation")
one_compartment, multiple_compartment, physiology_compartment = st.tabs(['One Compartmental Simulation','Multiple Compartmental Simulation','Physiology-based Simulation'])

with one_compartment:   
    st.write("""This page helps to visualize the drug's PK profile of the multiple-dosing regimen, using the one-compartmental model.

It takes the PK parameters, including ka, ke, and Vd to characterize the PK profile.

It also enables the define different dosing regimens by the buttons "Add IV Drug" or "Add Non-IV Drug. Each dose is characterized by the Dose Amount and the Starting Time Point. There are two types of dose:

- **IV drug:** the infusion duration can be used for the prolonged IV dose. If the normal IV dose is used, infusion duration should remain None.
- **Non-IV drug:** the total bioavailability is set equal to 1.0 by default. It can be changed when you have information.

""")

    # Input the PK parameters
    col1, col2 = st.columns(2)
    with col1:   
        ka = st.number_input("Absorption Rate Constant (h-1)", value=None,format="%.3f")
        ke = st.number_input("Elimination Rate Constant (h-1)", value=0.2,format="%.3f")
    with col2:
        Vd = st.number_input("Volume of Distribution (L)", value=33.2,format="%.3f")
        simulation_range = st.number_input('Simulation Range (h)',value = 100.0, format="%.1f")

    st.write("\n\n\n")

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
                st.write("\n\n\n")

            elif st.session_state.dose_times[i]["label"] == 'non_iv':
                st.write(f'**Dose {i+1} - Non-IV Dose**')
                st.session_state.dose_times[i]["time"] = st.number_input(f"Start time (h)", value=0.0, key=f"time_{i}",format="%.1f")
                st.session_state.dose_times[i]["dose"] = st.number_input(f"Dose Amount (mg)", value=0.000, key=f"dose_{i}",format="%.3f")
                st.session_state.dose_times[i]["F"] = st.number_input('Biovailability', value = 1.00, format="%.3f", key=f"F_{i}")
                st.write("\n\n\n")

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
                    st.error('**Parameter Mismatch:** You need to define ka for the simulation of Non-IV Drug.')
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
            fig.add_trace(go.Scatter(x=np.arange(0,simulation_range+0.1, 0.1), y=simulate_conc, mode='lines',name='Combined Profile'))
        fig.update_yaxes(title_text='Concentration (mg/L)')
        fig.update_xaxes(title_text='Time (h)')
        fig.update_layout(title='PK simulation')

        # Characterize the downloaded image 
        config = {
        'toImageButtonOptions': {
        'format': 'png', 
        'filename': 'Multiple_PK_simulation',
        'height': None,
        'width': None,
        'scale': 5
    }}

        st.plotly_chart(fig, config = config)
    
with multiple_compartment:
    st.write('''This page helps to simulate PK profile using a multiple compartmental model. The graphical representation of the model is described by the figure below.
             
The model includes one central compartment responsible for drug absorption and elimination. Various parameters for this compartment include Absorption Rate Constant, Elimination Rate Constant, and Volume of Distribution.

The model also includes one or more peripheral compartments directly connected to the central one. Each peripheral compartment is characterized by its Initial Drug Concentration, k_in, and k_out.

It also enables the define different dosing regimens by the buttons "Add IV Drug" or "Add Non-IV Drug. Each dose is characterized by the Dose Amount and the Starting Time Point. There are two types of dose:

- **IV drug:**  The drug that is immediately absorped into plasma compartment.
- **Non-IV drug:** The drug that need time to be absorped into plasma compartment.''')
    
    st.image('/mount/src/pkpd-simulation-tools/images/Multiple_Compartmental_Model.png')
    st.write("\n\n\n")
    
    # Initialize session states to store information
    if 'parameters' not in st.session_state:
        st.session_state.parameters = {}
    if 'compartment_count' not in st.session_state:
        st.session_state.compartment_count = 2  # Start from Compartment 2
    if 'dose_regimens' not in st.session_state:
        st.session_state.dose_regimens = []

    # Input for central compartment parameters
    st.subheader('Central Compartment Parameters')
    col1, col2 = st.columns(2)
    with col1: 
        simulation_range = st.number_input('Simulation Range (h)', value=24.0, format="%.3f", key='Multiple Simulation range')
        F = st.number_input('Bioavailability', value=1.0, format="%.3f", key='Multiple Simulation Bioavailability')
        conc_limit = st.number_input('C Limit (mg/L)', value=None, format='%.3f', key='Multiple Simulation')
        
    with col2:
        ka = st.number_input("Absorption Rate Constant (h-1)", value=None, format="%.3f", key='Multiple Simulation ka')
        ke = st.number_input("Elimination Rate Constant (h-1)", value=0.2, format="%.3f", key='Multiple Simulation ke')
        V_central = st.number_input("Volume of Distribution (L)", value=33.0, format="%.3f", key='Multiple Simulation Vd')
    
    time = np.arange(0, simulation_range + 0.1, 0.1)
    
    # Initialize parameters
    st.session_state.parameters['Compartment 0'] = {'C0': 0, 'k_in': None, 'k_out': ka, 'V': V_central}
    st.session_state.parameters['Compartment 1'] = {'C0': 0, 'k_in': ka, 'k_out': ke, 'V': V_central}
    st.write("\n\n\n")

    # Input for peripheral compartments parameters
    st.subheader('Peripheral Compartment Parameters')
    add_peripheral = st.button("Add Peripheral Compartment")
    
    if add_peripheral: 
        new_compartment_key = f'Compartment {st.session_state.compartment_count}'
        st.session_state.parameters[new_compartment_key] = {'C0': 0.0, 'k_in': 0.0, 'k_out': 0.0, 'V': V_central}
        st.session_state.compartment_count += 1 

    cols = st.columns(3)
    for i in range(len(st.session_state.parameters) - 2):
        with cols[i % 3]:
            st.write(f'**Peripheral {i + 2}**')
            st.session_state.parameters[f'Compartment {i + 2}']["C0"] = st.number_input(f"Initial Drug Concentration (mg/L)", value=0.0, key=f"Do_{i + 2}", format="%.3f")
            st.session_state.parameters[f'Compartment {i + 2}']["k_in"] = st.number_input(f"k_in (h-1)", value=0.0, key=f"kin_{i + 2}", format="%.3f")
            st.session_state.parameters[f'Compartment {i + 2}']["k_out"] = st.number_input(f"k_out (h-1)", value=0.0, key=f"kout_{i + 2}", format="%.3f")
            st.write("\n\n\n")
    
    # Input for Dose Regimen
    st.subheader('Dose Regimen')

    col1, col2, col3 = st.columns(3)
    with col1: 
        add_iv_dose = st.button("Add IV Dose", key='Multiple Compartment IV Dose')
    with col2: 
        add_non_iv_dose = st.button("Add Non-IV Dose", key='Multiple Compartment Non-IV Dose')

    if add_iv_dose:
        st.session_state.dose_regimens.append({"time": 0, "dose": 0, "label": 'iv'})
    elif add_non_iv_dose:
        st.session_state.dose_regimens.append({"time": 0, "dose": 0, "label": 'non_iv'})

    cols = st.columns(3)
    for i, dose_time in enumerate(st.session_state.dose_regimens):
        with cols[i % 3]:
            if st.session_state.dose_regimens[i]["label"] == 'iv':
                st.write(f'**Dose {i + 1} - IV Dose**')
                st.session_state.dose_regimens[i]["time"] = st.number_input(f"Start Time (h)", value=0.0, key=f"multicompart_time_{i}", format="%.1f")
                st.session_state.dose_regimens[i]["dose"] = st.number_input(f"Dose Amount (mg)", value=0.000, key=f"multicompart_dose_{i}", format="%.3f")
                st.write('\n\n\n')
            elif st.session_state.dose_regimens[i]["label"] == 'non_iv':
                st.write(f'**Dose {i + 1} - Non-IV Dose**')
                st.session_state.dose_regimens[i]["time"] = st.number_input(f"Start Time (h)", value=0.0, key=f"multicompart_time_{i}", format="%.1f")
                st.session_state.dose_regimens[i]["dose"] = st.number_input(f"Dose Amount (mg)", value=0.000, key=f"multicompart_dose_{i}", format="%.3f")
                st.write('\n\n\n')

    
    # Run the simulation
    if st.button("Run Simulation", key='Multiple_Simulation'):
        conc = {}
        conc_each_dose = {}
        total_concentration = {f'C{i}': np.zeros_like(time) for i in range(len(st.session_state.parameters))}

        # Simulate each dose
        for i, dose_regimen in enumerate(st.session_state.dose_regimens):
            dose = dose_regimen['dose']
            start_time = dose_regimen['time']
            if dose_regimen['label'] == 'iv':
                conc[f'regimen{i}'] = multiple_compartment_simulation(st.session_state.parameters, time, dose, F, iv=True) 
            elif dose_regimen['label'] == 'non_iv':
                if ka is not None:
                    conc[f'regimen{i}'] = multiple_compartment_simulation(st.session_state.parameters, time, dose, F, iv=False)
                else:
                    conc[f'regimen{i}'] = {f'C{comp}': np.zeros_like(time) for comp in range(len(st.session_state.parameters))}
                    st.error('**Parameter Mismatch:** You need to define ka for the simulation of Non-IV Drug.')
                    break
            
            # Store compartments concentration into each dose
            for compartment in range(len(st.session_state.parameters)):
                if f'regimen{i}' not in conc_each_dose:
                    conc_each_dose[f'regimen{i}'] = {}
                conc_each_dose[f'regimen{i}'][f'C{compartment}'] = np.zeros_like(time)
                conc_each_dose[f'regimen{i}'][f'C{compartment}'][int(start_time / 0.1):] = conc[f'regimen{i}'][f'C{compartment}'][:len(time) - int(start_time / 0.1)]

        # Calculate concentration for each compartment during the whole regimen
        for dose_regimen in conc_each_dose.values():
            for compartment, values in dose_regimen.items():
                total_concentration[compartment] += values[:len(time)]

        # Visualize the results
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time,
            y=total_concentration['C1'],
            mode='lines',
            name='Central Compartment'
        ))

        for i in range(2, len(st.session_state.parameters)):
            fig.add_trace(go.Scatter(
                x=time,
                y=total_concentration[f'C{i}'],
                mode='lines',
                name=f'Compartment {i}',
                line=dict(dash='dash')
            ))
    
        if conc_limit is not None:
            fig.add_hline(y=conc_limit, line_dash="dash", line_color="red")

        fig.update_layout(
            title='Multiple Compartmental Pharmacokinetic Simulation',
            xaxis_title='Time (hours)',
            yaxis_title='Concentration (mg/L)',
        )

        config = {
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'PK_simulation',
                'height': None,
                'width': None,
                'scale': 5
            }
        }
        st.plotly_chart(fig, config=config)

        # Simulation data
        total_concentration['C0'] = time
        simulation_data = pd.DataFrame(total_concentration)
        simulation_data.rename(columns={'C0': 'Time'}, inplace=True)

        st.subheader('Simulation Data')
        simulation_data_display = st.data_editor(simulation_data)




with physiology_compartment:
    st.info("This page is on the way to development. Please come back later.")




        



        
