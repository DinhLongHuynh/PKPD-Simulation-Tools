import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from scipy.stats import norm


def _sample_lognormal(pop_value, omega, size):
    """Draw log-normally distributed samples shaped for broadcasting."""
    draws = norm.rvs(loc=0, scale=omega, size=size)
    return (pop_value * np.exp(draws)).reshape(size, 1)


def _sample_normal(scale, size):
    """Draw normally distributed residuals shaped for broadcasting."""
    draws = norm.rvs(loc=0, scale=scale, size=size)
    return np.array(draws).reshape(size, 1)


def _ordered_compartments(parameters):
    """Return compartment definitions sorted by numeric suffix."""
    sorted_keys = sorted(parameters.keys(), key=lambda key: int(key.split()[1]))
    return [parameters[key].copy() for key in sorted_keys]


def _initial_concentrations(compartments, dose, F, iv):
    """Set compartment C0 values based on route of administration."""
    if iv:
        compartments[0]['C0'] = 0
        compartments[1]['C0'] = dose / compartments[0]['V']
    else:
        compartments[0]['C0'] = F * dose / compartments[0]['V']
        compartments[1]['C0'] = 0
    return [comp['C0'] for comp in compartments]


def _peripheral_exchange(compartments, concentrations):
    """Aggregate exchange between central and peripheral compartments."""
    flux = 0.0
    for idx in range(2, len(compartments)):
        comp = compartments[idx]
        flux += comp['k_out'] * concentrations[idx] - comp['k_in'] * concentrations[1]
    return flux

def population_pk_simulation(parameters):
    '''This function helps to visulaized the PK profile of single dose using one-compartmental model.
    
    Parameters: 
        Parameters (dict): A dictionary that contain all the information for simulation.
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
                'C Limit': C_limit,
                'sampling_points': sampling_points,
                'logit':logit}
    Returns: 
        df_C (PandasDataFrame): Concentration by Time Profile.
        df_C_ln (PandasDataFrame): Logarithm of Concentration by Time Profile.
        '''

    n_patients = parameters['Number of Patients']

    # Defined time scale for the simulation
    sampling_points = np.arange(0, parameters['sampling_points'] + 0.1, 0.1)
    time = np.array(sampling_points).reshape(1, len(sampling_points))

    # Sampling variability of PK parameters
    V_var = _sample_lognormal(parameters['Population Volume of Distribution'], parameters['Omega V'], n_patients)
    CL_var = _sample_lognormal(parameters['Population Clearance'], parameters['Omega CL'], n_patients)
    F_var = _sample_lognormal(parameters['Population Bioavailability'], parameters['Omega F'], n_patients)

    ke_var = CL_var / V_var

    # Sampling variability of residual error
    resid_var = _sample_normal(parameters['Sigma Residual'], n_patients)

    dose = parameters['Dose']
    population_ka = parameters['Population ka']
    if population_ka is None:
        concentration = (dose * F_var / V_var) * np.exp(np.dot(-ke_var, time)) + resid_var
    else:
        ka_var = _sample_lognormal(population_ka, parameters['Omega ka'], n_patients)
        concentration = (
            (dose * F_var * ka_var) / (V_var * (ka_var - ke_var))
            * (np.exp(np.dot(-ke_var, time)) - np.exp(np.dot(-ka_var, time)))
            + resid_var
        )

    # Generate the dataframe of the PK profile
    rounded_sampling = np.round(sampling_points, 1)
    df_C = pd.DataFrame(concentration, columns=rounded_sampling)
    df_C.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_C_ln = pd.DataFrame(np.log(concentration), columns=rounded_sampling)
    df_C_ln.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Visualized Profile
    fig = go.Figure()
    plot_log = parameters['logit']
    frame_to_plot = df_C_ln if plot_log else df_C
    for i in range(n_patients):
        fig.add_trace(
            go.Scatter(x=sampling_points, y=frame_to_plot.iloc[i, :], mode='lines', showlegend=False)
        )
    fig.update_yaxes(
        title_text='Log[Concentration] (mg/L)' if plot_log else 'Concentration (mg/L)'
    )
    if parameters['C Limit'] is not None:
        limit_value = np.log(parameters['C Limit']) if plot_log else parameters['C Limit']
        fig.add_hline(y=limit_value, line_dash="dash", line_color="red")
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
    st.plotly_chart(fig, config=config)

    return df_C, df_C_ln


def multiple_compartment_simulation(parameters, time, dose, F, iv):
    '''This function helps to visualize pharmacokinetic profile of single dose using multiple-comparmental model.
    
    Parameters: 
        parameters (dict): A dictionary that contain information about different compartments. Each compartment contains information of its initial concentration,
        k_in, k_out, and V.
            Example: 
            parameters = {'Compartment 0': {'C0': Dose/V_central, 'k_in': None, 'k_out': ka, 'V': V_central},
                        'Compartment 1': {'C0': 0, 'k_in': ka, 'k_out': ke, 'V': V_central} }
        time (np.array): An array that contain time points used to generate the profile.
        dose (float): Dose Amount.
        conc_limit (float): A concentration limitation of the drug. 
        iv (boolean): indicate if the drug is iv or non-iv drug.

    Returns: 
        results (dict): A dictionary that contains the concentration by time profile for each compartment.
        '''
    

    compartments = _ordered_compartments(parameters)
    n_compartments = len(compartments)

    def general_model_iv(concentrations, _t):
        derivatives = [0.0] * n_compartments
        derivatives[0] = dose / compartments[0]['V']
        derivatives[1] = -compartments[1]['k_out'] * concentrations[1] + _peripheral_exchange(compartments, concentrations)
        for idx in range(2, n_compartments):
            comp = compartments[idx]
            derivatives[idx] = comp['k_in'] * concentrations[1] - comp['k_out'] * concentrations[idx]
        return derivatives
    
    def general_model_non_iv(concentrations, _t):
        derivatives = [0.0] * n_compartments
        derivatives[0] = -compartments[0]['k_out'] * concentrations[0]
        derivatives[1] = (
            compartments[0]['k_out'] * concentrations[0]
            - compartments[1]['k_out'] * concentrations[1]
            + _peripheral_exchange(compartments, concentrations)
        )
        for idx in range(2, n_compartments):
            comp = compartments[idx]
            derivatives[idx] = comp['k_in'] * concentrations[1] - comp['k_out'] * concentrations[idx]
        return derivatives

    concentrations_initial = _initial_concentrations(compartments, dose, F, iv)

    # Simulation PK profile
    if iv:
        solution = odeint(general_model_iv, concentrations_initial, time)
    else: 
        solution = odeint(general_model_non_iv, concentrations_initial, time)
    
    # Re-organized the results into dictionary.
    results = {f'C{i}': solution[:, i] for i in range(n_compartments)}

    return results


def population_pd_simulation(parameters):
    '''This function helps to visulaized the PD profile of single dose.
    
    Parameters: 
        Parameters (dict): A dictionary that contain all the information for simulation.
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

    Returns: 
        E_df (PandasDataFrame): Effect by Concentration Profile.
        '''
    
    n_patients = parameters['Number of Patients']
    Ebaseline_var = _sample_lognormal(parameters['Population Ebaseline'], parameters['Omega Ebaseline'], n_patients)
    Emax_var = _sample_lognormal(parameters['Population Emax'], parameters['Omega Emax'], n_patients)
    EC50_var = _sample_lognormal(parameters['Population EC50'], parameters['Omega EC50'], n_patients)
    hill_var = _sample_lognormal(parameters['Population Hill'], parameters['Omega Hill'], n_patients)
    resid_var = _sample_normal(parameters['Sigma Residual'], n_patients)
    
    sampling_conc = np.linspace(0, parameters['Sampling Conc'], 1000)
    conc_list = np.array(sampling_conc).reshape(1, len(sampling_conc))
    E_array = (Ebaseline_var + Emax_var * (conc_list ** hill_var) / (EC50_var + conc_list)) + resid_var
    E_df = pd.DataFrame(E_array, columns=np.round(sampling_conc,1))
    
    fig = go.Figure()
    for i in range(n_patients):
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

    return E_df


def pk_iv_dose(dose, time, ke, Vd):
    '''This function helps to visualize PK profile of a single iv dose using one-compartmental model.
    
    Parameters: 
        dose (float): Dose Amount.
        time (np.array): An array containing time points for the simulation.
        ke (float): the elimination constant of the drug.
        Vd (float): the volumns of distribution of the drug.
        
    Returns:
        concentration (np.array): A concentration by time profile.
    '''

    concentration = (dose/Vd) * (np.exp(-ke * time))
    return concentration


def pk_prolonged_iv_dose(dose, time, ke, Vd, infusion_duration):
    '''This function helps to visualize PK profile of a single prolonged iv dose using one-compartmental model.
    
    Parameters: 
        dose (float): Dose Amount.
        time (np.array): An array containing time points for the simulation.
        ke (float): the elimination constant of the drug.
        Vd (float): the volumns of distribution of the drug.
        infusion_duration (float): the time period for infusing the drug. 
        
    Returns:
        concentration (np.array): A concentration by time profile.
    '''

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
    '''This function helps to visualize PK profile of a single non-iv dose using one-compartmental model.
    
    Parameters: 
        dose (float): Dose Amount.
        F (float): Bioavailability of the drug.
        time (np.array): An array containing time points for the simulation.
        ke (float): the elimination constant of the drug.
        ka (float): the absorption constant of the drug.
        Vd (float): the volumns of distribution of the drug.
        
        
    Returns:
        concentration (np.array): A concentration by time profile.
    '''
    
    concentration = ((dose * F*ka)/(Vd*(ka-ke)))*(np.exp(-ke*time)-np.exp(-ka*time))
    return concentration
