# Import module/package
import streamlit as st
import pandas as pd 
import numpy as np
from pkpd_sian.visualization import distribution_plots, id_count_by_dose, pk_profile_by_dose
from pkpd_sian.analysis import non_compartmental_analysis, non_compartmental_plots, one_compartmental_iv_analysis, one_compartmental_im_analysis
from pkpd_sian.preprocessing import data_preprocessing

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
        file = '/mount/src/pkpd-simulation-tools/testdata/Phase_I_iv_drug.csv'
    elif im_drug_file:
        file = '/mount/src/pkpd-simulation-tools/testdata/Phase_I_im_drug.csv'

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

        extract_df = data_preprocessing(df)



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
    if edited_extract_df is not None:
      # Quick summary
      st.title('Quick Summary')
      col1, col2 = st.columns(2)
      with col1:
        # plot the summary of study arms by Dose
        if 'Gender' in edited_extract_df.columns:
            id_count_by_dose(edited_extract_df,gender=True)
        
        else: 
            id_count_by_dose(edited_extract_df,gender=False)
            
      
      with col2: 
          # plot the summary of Age
          if 'Age' in edited_extract_df.columns: 
              distribution_plots(data=edited_extract_df,x='Age',xlabel="Age",ylabel='Freq.',title='Age Distribution')
        
      col3, col4 = st.columns(2)
      with col3: 
          # plot the summary of Weight
          if 'Weight' in edited_extract_df.columns: 
            distribution_plots(data=edited_extract_df,x='Weight',xlabel="Weight",ylabel='Freq.',title='Weight Distribution')
      
      
      with col4:
          # plot the summary of CLCR
          if 'CLCR' in edited_extract_df.columns: 
            distribution_plots(data=edited_extract_df,x='CLCR',xlabel="Creatinine Clearance",ylabel='Freq.',title='CLCR Distribution')


      # Display the PK profile by Dose
      dose_profile = st.toggle('Display PK profile by Dose', value = False)
      
      if dose_profile:
        pk_profile_by_dose(edited_extract_df)
    
    else:
        st.info('You should upload the file first')




with non_compartment:
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
            st.error(f'**Insufficient data:** ID {", ".join(str(id) for id in unqualified_id)} have less than 3 data points, which is insufficient for fitting the model. Double check your data.')

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
                for id, lambda_points,count in zip(non_compartment_df_final['ID'],non_compartment_df_final['Number of Lambda Points'],range(counts)):
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
            st.error('**Insufficient Data:** For non-compartmental analysis, there should be at least 3 data points for each individuals. Double check your input data.')
    
    else:
        st.info('You should upload the file first')




with one_compartment:
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
            iv_analysis_final, unqualified_id = one_compartmental_iv_analysis(edited_extract_df)
            
            # Print warning for unqualified id
            if len(unqualified_id) > 0:
                st.error(f'**Insufficient data:** ID {", ".join(str(id) for id in unqualified_id)} have less than 3 data points, which is insufficient for fitting the model. Double check your data.')

            # Add the covariates to the dataframe
            if not iv_analysis_final.empty:
                covariate_df = edited_extract_df.drop(['Time','Conc','Dose'],axis = 1).drop_duplicates(subset='ID')
                iv_analysis_covariate_df = iv_analysis_final.merge(covariate_df, on = 'ID')
                iv_analysis_covariate_final = st.data_editor(iv_analysis_covariate_df)
            else:
                st.error('**Insufficient data:** For non-compartmental analysis, there should be at least 3 data points for each individuals. Double check your input data.')

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
                im_analysis_final, unqualified_id = one_compartmental_im_analysis(df=edited_extract_df, predefined_F=predefined_F, initial_ka=initial_ka, initial_ke=initial_ke, initial_Vd=initial_Vd)
                
                # Print warning for unqualified id
                if len(unqualified_id) > 0:
                    st.error(f'**Insufficient data:** ID {", ".join(str(id) for id in unqualified_id)} have less than 3 data points, which is insufficient for fitting the model. Double check your data.')

                # Add the covariates to the dataframe
                if not im_analysis_final.empty:
                    covariate_df = edited_extract_df.drop(['Time','Conc','Dose'],axis = 1).drop_duplicates(subset='ID')
                    im_analysis_covariate_df = im_analysis_final.merge(covariate_df, on = 'ID')
                    im_analysis_covariate_final = st.data_editor(im_analysis_covariate_df)
                else:
                    st.info('**Insufficient data:** For non-compartmental analysis, there should be at least 3 data points for each individuals. Double check your input data.')


                

    
    else:
        st.info('You should upload the file first')


