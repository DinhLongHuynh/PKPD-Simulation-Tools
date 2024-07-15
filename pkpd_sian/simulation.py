import numpy as np
from scipy.integrate import odeint
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from scipy.stats import norm

def one_compartment_simulation(parameters): 
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


    if parameters['Population ka'] is None:
        concentration = ((parameters['Dose'] * F_var / V_var) * np.exp(np.dot(-ke_var, time)))+resid_var
    else:
        CV_ka = norm.rvs(loc=0, scale=parameters['Omega ka'], size=parameters['Number of Patients'])
        ka_variability = parameters['Population ka'] * np.exp(CV_ka)
        ka_var = ka_variability.reshape(parameters['Number of Patients'], 1)
        concentration = ((parameters['Dose'] * F_var * ka_var) / (V_var * (ka_var - ke_var)) * (np.exp(np.dot(-ke_var, time)) - np.exp(np.dot(-ka_var, time))))+resid_var

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
            if parameters['C Limit'] is not None:
                fig.add_hline(y=np.log(parameters['C Limit']), line_dash="dash", line_color="red")
        else:
            pk_data = df_C.iloc[i, :]
            fig.add_trace(go.Scatter(x=sampling_points, y=pk_data, mode='lines',showlegend=False))
            fig.update_yaxes(title_text='Concentration (mg/L)')
            if parameters['C Limit'] is not None:
                fig.add_hline(y=parameters['C Limit'], line_dash="dash", line_color="red")
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

    return df_C, df_C_ln


def multiple_compartment_simulation(parameters, time, dose, conc_limit, iv=False):
    '''This function helps to visualize pharmacokinetic profile of single dose using multiple-comparmental model.
    
    Parameters: 
        parameters (dict): A dictionary that contain information about different compartments. Each compartment contains information of its initial concentration,
        k_in, k_out, and V.
            Example: 
            parameters = {'Compartment 0': {'C0': Dose/V_central, 'k_in': None, 'k_out': ka, 'V': V_central},
                            'Compartment 1': {'C0': 0, 'k_in': ka, 'k_out': ke, 'V': V_central}
                            }
        time (np.array): An array that contain time points used to generate the profile.
        dose (float): Dose Amount.
        conc_limit (float): A concentration limitation of the drug. 
        iv (boolean): indicate if the drug is iv or non-iv drug.

    Returns: 
        results (dict): A dictionary that contains the concentration by time profile for each compartment.
        '''
    def general_model(concentrations, t):
        dCdt_dict = {}
        if iv:
            # Compartment 0
            dCdt_dict['dC0dt'] = dose / parameters['Compartment 0']['V']
            # Compartment 1
            dCdt_dict['dC1dt'] = (- parameters['Compartment 1']['k_out'] * concentrations[1]
                          + sum(parameters['Compartment ' + str(i)]['k_out'] * concentrations[i] - parameters['Compartment ' + str(i)]['k_in'] * concentrations[1] for i in range(2, len(parameters))))
            # Other compartments
            for i in range(2, len(parameters)):
                dCdt_dict['dC' + str(i) + 'dt'] = (parameters['Compartment ' + str(i)]['k_in'] * concentrations[1]
                                       - parameters['Compartment ' + str(i)]['k_out'] * concentrations[i])
        else:
            # Compartment 0
            dCdt_dict['dC0dt'] = -parameters['Compartment 0']['k_out'] * concentrations[0]
            # Compartment 1
            dCdt_dict['dC1dt'] = (parameters['Compartment 0']['k_out'] * concentrations[0]
                          - parameters['Compartment 1']['k_out'] * concentrations[1]
                          + sum(parameters['Compartment ' + str(i)]['k_out'] * concentrations[i] - parameters['Compartment ' + str(i)]['k_in'] * concentrations[1] for i in range(2, len(parameters))))
            # Other compartments
            for i in range(2, len(parameters)):
                dCdt_dict['dC' + str(i) + 'dt'] = (parameters['Compartment ' + str(i)]['k_in'] * concentrations[1]
                                       - parameters['Compartment ' + str(i)]['k_out'] * concentrations[i])

        return [dCdt_dict['dC' + str(i) + 'dt'] for i in range(len(dCdt_dict))]

    # Initialize
    if iv:
        parameters['Compartment 1']['C0'] = dose / parameters['Compartment 0']['V']
    
    concentrations_initial = [param['C0'] for param in parameters.values()]

    # Solve
    solution = odeint(general_model, concentrations_initial, time)

    # Extract concentrations
    results = {f'C{i}': solution[:, i] for i in range(len(parameters))}

    # Draw the graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time,
        y=results['C1'],
        mode='lines',
        name='Central Compartment'))

    for i in range(2, len(parameters)):
        fig.add_trace(go.Scatter(
            x=time,
            y=results['C' + str(i)],
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

    return results


def pd_simulation(parameters):
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

    return E_df


def pk_iv_dose(dose, time, ke, Vd):
    '''This function helps to visualize PK profile of a single iv dose.
    
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
    '''This function helps to visualize PK profile of a single prolonged iv dose.
    
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
    '''This function helps to visualize PK profile of a single non-iv dose.
    
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

