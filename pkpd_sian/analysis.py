import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from scipy.optimize import curve_fit
from scipy.integrate import quad



def non_compartmental_analysis(df):
    '''This function helps to analysis the clinical trials results using non-comparmental analysis.
    
    Parameters: 
        df (PandasDataFrame): A data frame that stores information of the clinical trials. The columns should be renamed as "ID","Dose","Time", and "Conc".
        The additional columns is acceptable. 
        
    Returns: 
        df_analysis (PandasDataFrame): A data frame that stores the analysis results, including: 
            - ID
            - Dose
            - Slope
            - Number of Lambda Points
            - R2 Values
            - AUC_0-last
            - AUC_last-inf
            - AUC _0-inf
            - Apparent Clearance
        
        unqualified_id (list): A list of unqualified individuals that cannot do the analysis.'''
    
    # Initialize output dataframe
    data = {
        'ID': [],
        'Dose': [],
        'Slope': [],
        'Number of Lambda Points': [],
        'R2 Values': [],
        'AUC_0-last': [],
        'AUC_last-inf': [],
        'AUC_0-inf': [],
        'Half Life': [],
        'Apparent Clearance': []
    }
    
    # Initialize unqualified id list
    unqualified_id = []
    
    # Extract each id data to handle
    for id in df['ID'].unique():
        df_id = df[df['ID'] == id].dropna()
        
        # Skip if is has less than 3 points 
        if df_id.shape[0] < 3:
            unqualified_id.append(id)
            continue  
        
        # Calculate AUC 0-last
        auc_0_last = np.trapz(y=df_id['Conc'], x=df_id['Time'])
        
        # Find optimal number of lambda points
        r2_list = []
        slope_list = []
        
        # Try different number of lamdapoints
        for n_points in range(3, df_id.shape[0] + 1):
            # Extract df
            df_id_point = df_id.iloc[-n_points:, :] 
            
            # Run regression
            X_points = df_id_point[['Time']]
            Y_points = np.log(df_id_point['Conc'] + 0.00001).values.reshape(-1, 1)
            
            
            model = LinearRegression()
            model.fit(X_points, Y_points)
            
            # Evaluate regression
            prediction = model.predict(X_points)
            r2 = r2_score(y_true=Y_points, y_pred=prediction)
            r2_list.append(r2)
            slope_list.append(model.coef_.item())
        
        # Skip if r2_list is empty
        if not r2_list:
            unqualified_id.append(id)
            continue  
        
        # Select optimal lambda points and the corresponding slopes
        r2_max_index = np.argmax(r2_list)
        slope = slope_list[r2_max_index]
        
        # Determine PK parameters
        auc_last_inf = -df_id['Conc'].iloc[-1] / slope
        dose = df_id['Dose'].unique()[0]
        auc_0_inf = auc_0_last + auc_last_inf
        apparent_CL = dose / auc_0_inf
        half_life = -np.log(2) / slope
        
        # Add to initial dataframe
        data['ID'].append(id)
        data['Dose'].append(dose)
        data['Slope'].append(-slope)
        data['Number of Lambda Points'].append(r2_max_index + 3)
        data['R2 Values'].append(r2_list[r2_max_index])
        data['AUC_0-last'].append(auc_0_last)
        data['AUC_last-inf'].append(auc_last_inf)
        data['AUC_0-inf'].append(auc_0_inf)
        data['Half Life'].append(half_life)
        data['Apparent Clearance'].append(apparent_CL)

    # Create DataFrame
    df_analysis = pd.DataFrame(data)
    return df_analysis, unqualified_id


def non_compartmental_plots(df_whole_profile,df_lambda_profile):
    '''This function helps to visualized the choice of lambda points and the regression line on individual profile.
    
    Parameters:
        df_whole_profile (PandasDataFrame): A dataframe containing whole profile of individuals.
        df_lambda_profile (Pandas DataFrame): A dataframe containing only lambda points of individuals profiles.'''
    
    # Create base figure with whole profile
    fig = px.scatter(df_whole_profile, x='Time', y='log_conc')
    
    # Create scatter plot with trendline for lambda points
    trend_fig = px.scatter(df_lambda_profile, x='Time', y='log_conc', trendline='ols')
    
    # Extract the trendline data
    trendline_data = trend_fig.data[1]  # The trendline is the second trace in the figure
    
    # Add lambda profile to the main figure
    fig.add_trace(go.Scatter(x=df_lambda_profile['Time'], y=df_lambda_profile['log_conc'], mode='markers', marker=dict(color='red'), name='Lambda Points',showlegend=False))
    
    # Add the trendline to the main figure
    fig.add_trace(trendline_data)

    # Modify the axis label
    fig.update_layout(title=f"ID {df_whole_profile['ID'].unique()}", xaxis_title='Time', yaxis_title='Log Concentration')
    
    # Display the figure
    config_nca = {
        'toImageButtonOptions': {
        'format': 'png', 
        'filename': 'nca_analysis',
        'height': None,
        'width': None,
        'scale': 5 }}
    st.plotly_chart(fig,config = config_nca)


def one_compartmental_iv_analysis(df):
    '''This function helps to analysis the clinical trials results for iv drug using one-compartmental model.
    The analysis is conducted using linear regression of the function: ln(C) = ln(C0) - ke*t.
    
    Parameters: 
        df (PandasDataFrame): A data frame that stores information of the clinical trials. The columns should be renamed as "ID","Dose","Time", and "Conc".
        The additional columns is acceptable. 
        
    Returns: 
        df_analysis (PandasDataFrame): A data frame that stores the analysis results, including: 
            - ID
            - Dose
            - C0
            - ke
            - R2
            - RMSE
            - AUC _0-inf
            - Half life
            - Apparent CL
            - Apparent Vd
        
        unqualified_id (list): A list of unqualified individuals that cannot do the analysis.'''
    
    # Initialize output dataframe
    iv_analysis_results = {'ID': [],
                               'Dose':[],
                               'C0': [],
                               'ke':[],
                               'R2':[],
                               'RMSE':[],
                               'AUC_0-inf':[],
                               'Half life': [],
                               'Apparent CL':[],
                               'Apparent Vd':[]}
    # Initialize unqualified id list
    unqualified_id = []

    # Extract each id data to handle
    for id in df['ID'].unique():
        df_id = df[df['ID']==id].dropna()

        # Skip if id has less than 3 datapoints   
        if df_id.shape[0] < 3:
            unqualified_id.append(id)
            continue 
        
        # Linear Regression 
        else:
            Y = np.log(df_id['Conc']+0.00001).values.reshape(-1, 1)
            X = df_id['Time'].values.reshape(-1, 1)
            model = LinearRegression()
            model.fit(X,Y)
            prediction = model.predict(X)

            # Store the primary data
            iv_analysis_results['ID'].append(id)
            iv_analysis_results['R2'].append(r2_score(y_true=np.exp(Y), y_pred=np.exp(prediction)))
            iv_analysis_results['RMSE'].append(mean_squared_error(y_true=np.exp(Y), y_pred=np.exp(prediction), squared=False))
            iv_analysis_results['ke'].append(-model.coef_.item())
            iv_analysis_results['C0'].append(np.exp(model.intercept_.item()))
            iv_analysis_results['Dose'].append(df_id['Dose'].unique()[0])
            iv_analysis_results['Apparent Vd'].append(df_id['Dose'].unique()[0]/np.exp(model.intercept_.item()))
            iv_analysis_results['Apparent CL'].append(-model.coef_.item()*df_id['Dose'].unique()[0]/np.exp(model.intercept_.item()))
            iv_analysis_results['AUC_0-inf'].append(np.exp(model.intercept_.item())/-model.coef_.item())
            iv_analysis_results['Half life'].append(np.log(2)/-model.coef_.item())

                
        
    iv_analysis_df = pd.DataFrame(iv_analysis_results)
        
    return iv_analysis_df, unqualified_id


def one_compartmental_im_analysis(df, predefined_F, initial_ka, initial_ke, initial_Vd):
    '''This function helps to analysis the clinical trials results for non-iv drug using one-compartmental model.
    The analysis is conducted using non-linear regression, therefore, it requires the initial guess of parameters.
    
    Parameters: 
        df (PandasDataFrame): A data frame that stores information of the clinical trials. The columns should be renamed as "ID","Dose","Time", and "Conc".
        The additional columns is acceptable. 

        predefined_F (float): Initial guess of bioavailability.
        predefined_ka (float): Initial guess of ka.
        predefined_ke (float): Initial guess of ke.
        predefined_Vd (float): Initial guess of Vd.
        
    Returns: 
        df_analysis (PandasDataFrame): A data frame that stores the analysis results, including: 
            - ID
            - Dose
            - ka
            - ke
            - Vd
            - RMSE
            - Tmax
            - Cmax
            - Half life
            - AUC _0-inf
            - Clearance

        
        unqualified_id (list): A list of unqualified individuals that cannot do the analysis.'''
    
    # Initialize output dataframe
    im_analysis_results = {'ID': [],
                               'Dose':[],
                               'ka': [],
                               'ke':[],
                               'Vd':[],
                               'RMSE':[],
                               'Tmax':[],
                               'Cmax': [],
                               'Half life':[],
                               'AUC_0-inf':[],
                               'Clearance':[]}
        
    # Initialized unqualified id list
    unqualified_id = []

    # Extract each id data to handle
    for id in df['ID'].unique():
        df_id = df[df['ID']==id].dropna()
            
        # Skip if id has less than 3 datapoints
        if df_id.shape[0] < 3:
            unqualified_id.append(id)
            continue 

        # Non-linear regression
        else:
            def model(t, ka, ke, V):
                F = predefined_F
                Dose = df_id['Dose'].unique()[0]
                return (F * Dose * ka / (V * (ka - ke))) * (np.exp(-ke * t) - np.exp(-ka * t))

            initial_guesses = [initial_ka, initial_ke, initial_Vd]
            Y = df_id['Conc'].values
            X = df_id['Time'].values
            params, _ = curve_fit(model, X, Y, p0=initial_guesses)
            ka_est, ke_est, V_est = params
                
            prediction = model(X, ka_est, ke_est, V_est)
            RMSE = mean_squared_error(Y,prediction, squared=False)

            integral, _ = quad(model, 0, np.inf, args=(ka_est, ke_est, V_est))

            # Store the primary data
            im_analysis_results['ID'].append(id)
            im_analysis_results['Dose'].append(df_id['Dose'].unique()[0])
            im_analysis_results['ka'].append(ka_est)
            im_analysis_results['ke'].append(ke_est)
            im_analysis_results['Vd'].append(V_est)
            im_analysis_results['RMSE'].append(RMSE)
            im_analysis_results['Tmax'].append(np.log(ke_est/ka_est)/(ke_est-ka_est))
            im_analysis_results['Cmax'].append(model(t =np.log(ke_est/ka_est)/(ke_est-ka_est),ka=ka_est,ke=ke_est,V=V_est))
            im_analysis_results['AUC_0-inf'].append(integral)
            im_analysis_results['Clearance'].append(df_id['Dose'].unique()[0]/integral) 
            if ka_est > ke_est:
                im_analysis_results['Half life'].append(np.log(2)/ke_est)
            elif ka_est < ke_est:
                im_analysis_results['Half life'].append(np.log(2)/ka_est)


                
        
    im_analysis_df = pd.DataFrame(im_analysis_results)
        
    return im_analysis_df, unqualified_id
