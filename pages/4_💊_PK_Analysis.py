# Import module/package
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from thefuzz import process
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from scipy.optimize import curve_fit
from scipy.integrate import quad

# Page setup
st.set_page_config(page_title='PK Analysis', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 PK Analysis Tools")
introduction, file_characteristic, visualization, non_compartment, one_compartment = st.tabs(["Introduction",'File Characteristic','Data Visualization',"Non-compartmental Analysis", "One-compartmental Analysis"])



with introduction:  
# Introduction
    st.write(''' This page helps users to analyze the clinical trial data. There are two approaches to the analysis:

 - **Non-compartmental Analysis**: the analysis will be based on the discrete data points on the PK profile to conclude several PK parameters directly.
             
 - **One-compartmental Analysis**: the analysis will fit the observed data to the predefined model and then derive PK parameters from the model.''')

# File uploader
    uploaded_file = st.file_uploader('Import your CSV dataset here')

    st.caption('These two demo datasets could be used as application trial:')
    col1, col2 = st.columns(2)

# Initialize file to None
    file = None

# Initialize df to None
    if 'df' not in st.session_state:
        st.session_state.df = None

    with col1:
        iv_drug_file = st.button('IV Drug Data')
    with col2:
        im_drug_file = st.button('IM Drug Data')

    # Handling button clicks
    if uploaded_file is not None:
        file = uploaded_file
    elif iv_drug_file:
        file = '/../testdata/Phase_I_iv_drug.csv'
    elif im_drug_file:
        file = '/../testdata/Phase_I_im_drug.csv'

# Read and store the data in session state
    if file is not None:
        st.session_state.df = pd.read_csv(file)
        st.success('File importing success')
        st.caption('Next step is characterising the data with File Characteristic tab.')

with file_characteristic:
    if st.session_state.df is not None:
        df = st.session_state.df

        st.header("File Characteristic")
        st.caption('Select the column in your file that corresponds to these descriptions.')

    # Use the similarity check to pre-assign mandatory columns
        default_id_col = process.extract('ID', df.columns, limit=1)[0][0]
        default_time_col = process.extract('Time', df.columns, limit=1)[0][0]
        default_conc_col = process.extract('Conc', df.columns, limit=1)[0][0]
        default_dose_col = process.extract('Dose', df.columns, limit=1)[0][0]

        default_id_index = df.columns.get_loc(default_id_col)
        default_time_index = df.columns.get_loc(default_time_col)
        default_conc_index = df.columns.get_loc(default_conc_col)
        default_dose_index = df.columns.get_loc(default_dose_col)

    # Let user define the columns
        col1, col2 = st.columns(2)
        with col1:  # Use pre-assign columns as the default argument
            st.write('Compulsory Information')
            ID_col = st.selectbox('Select a column that represent ID', df.columns, index=default_id_index)
            Time_col = st.selectbox('Select a column that represent Time', df.columns, index=default_time_index)
            Concentration_col = st.selectbox('Select a column that represent Concentration', df.columns, index=default_conc_index)
            Dose_col = st.selectbox('Select a column that represent Dose', df.columns, index=default_dose_index)
        with col2:
            st.write('Additional Information')
            Age_col = st.selectbox('Select a column that represent Age', df.columns, index=None)
            Weight_col = st.selectbox('Select a column that represent Body Weight', df.columns, index=None)
            Gender_col = st.selectbox('Select a column that represent Gender', df.columns, index=None)
            CLCR_col = st.selectbox('Select a column that represent Clearance Creatinine', df.columns, index=None)

    # Define the extracted columns from df
        col_list = [ID_col, Time_col, Concentration_col, Dose_col, Age_col, Weight_col, Gender_col, CLCR_col]
        col_name = ['ID', 'Time', 'Conc', 'Dose', 'Age', 'Weight', 'Gender', 'CLCR']
        extracted_col = []
        extracted_col_name = []
        for column, column_name in zip(col_list, col_name):
            if column is not None:
                extracted_col.append(column)
                extracted_col_name.append(column_name)

    # Extract df and unify the columns' names
        extract_df = df[extracted_col]
        extract_df.columns = extracted_col_name

    # Allow the edit from user on the dataframe
        st.subheader('Data Frame')
        st.caption('Double-check your data. You can manipulate data directly on the displayed table.')
        edited_extract_df = st.data_editor(extract_df, num_rows="dynamic")

        # Update the session state with the edited dataframe
        st.session_state.edited_extract_df = edited_extract_df
    else:
        st.info('You should upload the file first')
        edited_extract_df = None





with visualization:
    # Define function used for the visualisation
    def distribution_plots(data,x,xaxis_title,y_axis_title,header):
        st.subheader(header)
        nbins = st.slider(f'Edit the number of bins for {x} distribution:',value = 20)
        fig = px.histogram(data, x=x,nbins=nbins)
        fig.update_layout(title=header, xaxis_title=xaxis_title, yaxis_title=y_axis_title)
        plot = st.plotly_chart(fig, use_container_width=True)

    # Body code
    if edited_extract_df is not None:
      # Quick summary
      st.title('Quick Summary')
      col1, col2 = st.columns(2)
      with col1:
        # plot the summary of study arms by Dose
        if Gender_col is None:
            # Handling data: 
            st.subheader('Number of ID by Dose')
            id_count_df = edited_extract_df.groupby('Dose')['ID'].nunique().reset_index(name='ID_count')
            id_count_df['Dose'] = id_count_df['Dose'].astype(str)+'mg' # Turn dose into category for better visualization

            # Draw plot
            default_plot_title = 'Number of ID by Dose'
            default_xlabel = 'ID Counts'
            default_ylabel = 'Dose'
            fig = px.bar(id_count_df, x='ID_count', y='Dose', orientation='h',color = 'Dose', title =default_plot_title ,color_discrete_sequence=px.colors.qualitative.Safe)
            fig.update_layout(xaxis_title=default_xlabel, yaxis_title=default_ylabel)
            plot = st.plotly_chart(fig, use_container_width=True)

            # Plot characteristic
            plot_title = st.text_input('Edit plot title:',value = 'Number of ID by Dose')
            
            col3, col4 = st.columns(2)
            with col3:
                xlabel = st.text_input('Edit x label:',value = 'ID Counts')
            with col4:
                ylabel = st.text_input('Edit y label:',value = 'Dose')
            
            fig.update_layout(title=plot_title, xaxis_title=xlabel, yaxis_title=ylabel)
            plot.plotly_chart(fig, use_container_width=True)
        
        # plot the summary of study arms by Dose and Gender
        else: 
            # Hanlding data
            st.subheader('Number of ID by Dose and Gender')
            id_count_df = edited_extract_df.groupby(['Dose','Gender'])['ID'].nunique().reset_index(name='ID_count')
            id_count_df['Dose'] = id_count_df['Dose'].astype(str)+'mg' # Turn dose into category for better visualization
            id_count_df['Gender'] = id_count_df['Gender'].astype(str)

             # Draw the plot
            default_plot_title = 'Number of ID by Dose and Gender'
            default_xlabel = 'ID Counts'
            default_ylabel = 'Dose'
            fig = px.bar( id_count_df, x='ID_count', y='Dose', color='Gender', orientation='h',title = default_plot_title)
            fig.update_layout(xaxis_title=default_xlabel, yaxis_title=default_ylabel, legend_title_text='Gender')
            plot = st.plotly_chart(fig, use_container_width=True)

            # Plot characteristic
            plot_title = st.text_input('Edit plot title:',value = 'Number of ID by Dose and Gender')
            
            col3, col4 = st.columns(2)
            with col3:
                xlabel = st.text_input('Edit x label:',value = 'ID Counts')
            with col4:
                ylabel = st.text_input('Edit y label:',value = 'Dose')
            
            fig.update_layout(title=plot_title, xaxis_title=xlabel, yaxis_title=ylabel)
            plot.plotly_chart(fig, use_container_width=True)
      
      with col2: 
          # plot the summary of Age
          if Age_col is not None: 
              distribution_plots(data=edited_extract_df,x='Age',xaxis_title="Age",y_axis_title='Freq.',header='Age Distribution')
        
      col3, col4 = st.columns(2)
      with col3: 
          # plot the summary of Weight
          if Weight_col is not None: 
            distribution_plots(data=edited_extract_df,x='Weight',xaxis_title="Weight",y_axis_title='Freq.',header='Weight Distribution')
      
      
      with col4:
          # plot the summary of CLCR
          if CLCR_col is not None: 
            distribution_plots(data=edited_extract_df,x='CLCR',xaxis_title="Creatinine Clearance",y_axis_title='Freq.',header='CLCR Distribution')


      # Display the PK profile by Dose
      dose_profile = st.toggle('Display PK profile by Dose', value = False)
      
      if dose_profile:
        st.title('PK Profile by Dose')
        
        col1, col2 = st.columns(2)
        unique_doses = edited_extract_df['Dose'].unique()
        for i, dose in enumerate(unique_doses):
            dose_specific_df = edited_extract_df[edited_extract_df['Dose']==dose]
            fig = px.scatter(dose_specific_df, x='Time', y='Conc', title=f'Dose: {dose}')
            # Plot on 2-column page layout
            if i % 2 == 0:
                with col1:
                    st.plotly_chart(fig)
            else:
                with col2:
                    st.plotly_chart(fig)
    
    else:
        st.info('You should upload the file first')





with non_compartment:
    # Define functions for the analysis
    def non_compartmental_analysis(df):
        # Initialize dataframe
        data = {
            'ID': [],
            'Dose':[],
            'Slope': [],
            'Number of Lambda Points': [],
            'R2 Values': [],
            'AUC_0-last': [],
            'AUC_last-inf': [],
            'AUC_0-inf': [],
            'Half Life': [],
            'Apparent Clearance': []
        }
        
        unqualified_id = []
        for id in df['ID'].unique():
            df_id = df[df['ID'] == id].dropna()
            
            # Skip if less than 3 points 
            if df_id.shape[0] < 3:
                unqualified_id.append(id)
                continue  

            else:
                # Calculate AUC 0-last
                auc_0_last = np.trapz(y=df_id['Conc'], x=df_id['Time'])
            
                # Find optimal number of lamda points
                r2_list = []
                slope_list = []
                X = df_id[['Time']]
            
                for n_points in range(3, df_id.shape[0] + 1):
                    # Extract df
                    df_id_point = df_id.iloc[-n_points:, :] 
                    
                    #Run regression
                    X_points = df_id_point[['Time']]
                    Y_points = np.log(df_id_point['Conc'] + 0.00001).values.reshape(-1, 1)
                    model = LinearRegression()
                    model.fit(X_points, Y_points) 
                    
                    #Evaluate regression
                    prediction = model.predict(X_points) 
                    r2 = r2_score(y_true=Y_points, y_pred=prediction)
                    r2_list.append(r2)
                    slope_list.append(model.coef_.item())

            # Skip if r2_list is empty
                if not r2_list:
                    continue  
            
                else:
                    # Select optimal lamda poitns and the corresponding slopes
                    r2_max_index = np.argmax(r2_list)
                    slope = slope_list[r2_max_index]
                    
                    # Determine PK parameters 
                    auc_last_inf = -df_id['Conc'].iloc[-1] / slope
                    dose = df_id['Dose'].unique()[0]
                    auc_0_inf = auc_0_last + auc_last_inf
                    apparent_CL = dose / auc_0_inf
                    half_life = -np.log(2)/slope

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
        fig.update_layout(title=f'ID {id}', xaxis_title='Time', yaxis_title='Log Concentration')
    
        # Display the figure
        st.plotly_chart(fig)

    # Tab information
    st.header('Non-Compartmental Analysis')
    st.write("Non-compartmental analysis (NCA) is a method used in pharmacokinetics to analyze and interpret drug concentration data without assuming a specific compartmental model for the body's drug distribution and elimination processes. Instead of relying on a predetermined biological model, NCA calculates pharmacokinetic (PK) parameters directly from the observed concentration-time data.")
    st.write("\n")
    st.write("One of the most important parameters estimated from NCA is the **terminal slope**, also known as the terminal rate constant. To estimate this parameter, the algorithm considers a certain number of last data points, referred to as lambda points. The consideration starts with 3 points, then gradually increases over time. During that process, a linear regression is performed between the logarithm concentration and time of these points. Subsequently, the optimal number of lambda points is selected, and the corresponding slope is identified as the terminal rate constant.")
    st.write("\n")
    st.write("*However, it is important to note that the terminal slope can be either ka or ke, depending on the PK scenario. The further methods to estimate other PK parameters are described in the❓Helps page.*")
    st.write("\n")
    st.write("\n")

    st.subheader('Analysis Results')
    
    if edited_extract_df is not None:
        # Export the analysis resutls
        non_compartment_df, unqualified_id = non_compartmental_analysis(edited_extract_df)
        
        # Print warning with the unqualified ID
        if len(unqualified_id) > 0:
            st.error(f'ID {", ".join(str(id) for id in unqualified_id)} have less than 3 data points, which is insufficient for fitting the model. Double check your data.')

        # Add covariates to the final results dataframe
        if not non_compartment_df.empty:
            covariate_df = edited_extract_df.drop(['Time','Conc','Dose'],axis = 1).drop_duplicates(subset='ID')
            analysis_covariate_df = non_compartment_df.merge(covariate_df, on = 'ID')
            non_compartment_df_final = st.data_editor(analysis_covariate_df)
            
            #Display the selection profile:
            plots = st.toggle('Display the individual profiles')
            counts = non_compartment_df_final['ID'].nunique()
            
            if plots:
                col1, col2 = st.columns(2)
                for id, lambda_points, count in zip(non_compartment_df_final['ID'],non_compartment_df_final['Number of Lambda Points'],range(counts)):
                    # Extract whole PK profile 
                    df_whole_profile = edited_extract_df[edited_extract_df['ID']==id].dropna()
                    df_whole_profile['log_conc'] = np.log(df_whole_profile['Conc'])
                    
                    # Extract PK profile with selected lambda points
                    df_lambda_profile = df_whole_profile.iloc[-lambda_points:,:].dropna()
                    df_lambda_profile['log_conc'] = np.log(df_lambda_profile['Conc'])

                    # Plot with the 2 columns layout
                    if count%2 == 0:
                        with col1:
                            non_compartmental_plots(df_whole_profile,df_lambda_profile)
                    else:
                        with col2:
                            non_compartmental_plots(df_whole_profile,df_lambda_profile)
    
        else:
            st.info('For non-compartmental analysis, there should be at least 3 data points for each individuals. Double check your input data.')
    
    else:
        st.info('You should upload the file first')




with one_compartment:
    
    # Define functions for the analysis
    def iv_analysis_function(df):
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
        unqualified_id = []
        for id in df['ID'].unique():
            df_id = df[df['ID']==id].dropna()
            
            if df_id.shape[0] < 3:
                unqualified_id.append(id)
                continue 
            
            else:
                Y = np.log(df_id['Conc']+0.00001).values.reshape(-1, 1)
                X = df_id['Time'].values.reshape(-1, 1)
                model = LinearRegression()
                model.fit(X,Y)
                prediction = model.predict(X)

                # Store the primary data
                iv_analysis_results['ID'].append(id)
                iv_analysis_results['R2'].append(r2_score(y_true=Y, y_pred=prediction))
                iv_analysis_results['RMSE'].append(mean_squared_error(y_true=Y, y_pred=prediction, squared=False))
                iv_analysis_results['ke'].append(-model.coef_.item())
                iv_analysis_results['C0'].append(np.exp(model.intercept_.item()))
                iv_analysis_results['Dose'].append(df_id['Dose'].unique()[0])
                iv_analysis_results['Apparent Vd'].append(df_id['Dose'].unique()[0]/np.exp(model.intercept_.item()))
                iv_analysis_results['Apparent CL'].append(-model.coef_.item()*df_id['Dose'].unique()[0]/np.exp(model.intercept_.item()))
                iv_analysis_results['AUC_0-inf'].append(np.exp(model.intercept_.item())/-model.coef_.item())
                iv_analysis_results['Half life'].append(np.log(2)/-model.coef_.item())

                
        
        iv_analysis_df = pd.DataFrame(iv_analysis_results)
        
        return iv_analysis_df, unqualified_id

    def im_analysis_function(df, predefined_F, initial_ka, initial_ke, initial_Vd):
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
        
        unqualified_id = []

        for id in df['ID'].unique():
            df_id = df[df['ID']==id].dropna()
            
            if df_id.shape[0] < 3:
                unqualified_id.append(id)
                continue 
            
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

                # Elimination limited rate 
                if ka_est > ke_est:
                    im_analysis_results['Half life'].append(np.log(2)/ke_est)
                elif ka_est < ke_est:
                    im_analysis_results['Half life'].append(np.log(2)/ka_est)


                
        
        im_analysis_df = pd.DataFrame(im_analysis_results)
        
        return im_analysis_df, unqualified_id

    # Page information
    st.header('One-Compartmental Analysis')
    st.write('One-compartmental analysis (OCA) is a method used in pharmacokinetics to analyze and interpret drug concentration data by assuming the body behaves as a single, homogeneous compartment. OCA is the model-based method, which uses the data to fit the predefined model or equations.')
    st.write("\n")
    st.write('The important assumption of this analysis is that drug absorption and elimination follow first-order kinetic. There are two scenarios used for analysis:')
    st.write('- **IV drug analysis**: This scenario can be used for drugs that are instantaneously absorbed into the central plasma compartment.')
    st.write('- **Non-IV drug analysis**: This scenario can be used for drugs that are gradually absorbed into the central plasma compartment.')
    st.write("\n")
    
    if edited_extract_df is not None:
        # Choose mode to fit the data
        st.subheader('Classify your drug')
        col1, col2 = st.columns(2)
        with col1:
            iv_analysis = st.toggle('IV Drug Analysis')
        with col2:
            im_analysis = st.toggle('Non-IV Drug Analysis')

        # IV drug analysis
        if iv_analysis:
            st.subheader("IV Drug Analysis")
            # Export the analysis resutls
            iv_analysis_final, unqualified_id = iv_analysis_function(edited_extract_df)
            
            # Print warning for unqualified id
            if len(unqualified_id) > 0:
                st.error(f'ID {", ".join(str(id) for id in unqualified_id)} have less than 3 data points, which is insufficient for fitting the model. Double check your data.')

            # Add the covariates to the dataframe
            if not iv_analysis_final.empty:
                covariate_df = edited_extract_df.drop(['Time','Conc','Dose'],axis = 1).drop_duplicates(subset='ID')
                iv_analysis_covariate_df = iv_analysis_final.merge(covariate_df, on = 'ID')
                iv_analysis_covariate_final = st.data_editor(iv_analysis_covariate_df)
            else:
                st.info('For non-compartmental analysis, there should be at least 3 data points for each individuals. Double check your input data.')

        st.write('\n')

        # Non-iv drug analysis
        if im_analysis:
            st.subheader("Non-IV Drug Analysis")
            st.caption("Each patient needs at least 3 data points for non-iv drug analysis to fit the non-linear model with 3 parameters, including ka, ke, and Vd. However, to obtain reliable results, each patient should have more than 30 data points.")
            st.caption("The non-linear model fitting process requires initial guesses for the parameters, which can be based on previous studies. If the initial guesses are significantly different from the actual values, alternative values should be considered.")
            
            # Take the initial guesses of ke, ka, and Vd
            col1, col2 = st.columns(2)
            with col1:
                predefined_F = st.number_input("Bioavailability:",value = 1.00,format="%.3f")
                initial_Vd = st.number_input('Initial guess of Volume of Distribution:',value=0.001,format="%.3f")
            with col2:
                initial_ke = st.number_input('Initial guess of ke:',value=0.001,format="%.3f")
                initial_ka = st.number_input('Initial guess of ka:',value=0.002,format="%.3f")
            
            start =  st.button('Run Analysis')

            if start: 
                # Export the analysis resutls
                im_analysis_final, unqualified_id = im_analysis_function(df=edited_extract_df, predefined_F=predefined_F, initial_ka=initial_ka, initial_ke=initial_ke, initial_Vd=initial_Vd)
                
                # Print warning for unqualified id
                if len(unqualified_id) > 0:
                    st.error(f'ID {", ".join(str(id) for id in unqualified_id)} have less than 3 data points, which is insufficient for fitting the model. Double check your data.')

                # Add the covariates to the dataframe
                if not im_analysis_final.empty:
                    covariate_df = edited_extract_df.drop(['Time','Conc','Dose'],axis = 1).drop_duplicates(subset='ID')
                    im_analysis_covariate_df = im_analysis_final.merge(covariate_df, on = 'ID')
                    im_analysis_covariate_final = st.data_editor(im_analysis_covariate_df)
                else:
                    st.info('For non-compartmental analysis, there should be at least 3 data points for each individuals. Double check your input data.')


                

    
    else:
        st.info('You should upload the file first')
