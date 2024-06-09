import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from thefuzz import process
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

st.set_page_config(page_title='PK Analysis', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 PK Analysis Tools")
introduction, file_characteristic, visualization, non_compartment, one_compartment = st.tabs(["Introduction",'File Characteristic','Data Visualization',"Non-compartmental Analysis", "One-compartmental Analysis"])



with introduction:
    st.write('''This page helps users to analyse the clinical trial data. There are two approach in the analysis: 
         
1) Non-compartmental Analysis: the analysis will base on the discrete data points on the PK profile. Base on that to directly draw the conclusion of several PK parameters.
2) One-compartmental Analysis: the analysis will fit the observed data to the predefined model and then derived PK parameters from the model. ''')

    st.subheader('Input data')
    file = st.file_uploader('Import your csv dataset here')
    df = None
    if file is not None:
        df = pd.read_csv(file)
        st.caption('Next step is characterising the data with File Characteristic tab.')
       
    
    


with file_characteristic:
    st.header("File Characteristic")
    st.caption('Select the column in your file that corresponding to these descriptions')
    
    if df is not None:
        # Use the similarity check to pre-assign columns
        default_id_col = process.extract('ID',df.columns,limit=1)[0][0]
        default_time_col = process.extract('Time',df.columns,limit=1)[0][0]
        default_conc_col = process.extract('Conc',df.columns,limit=1)[0][0]
        default_dose_col = process.extract('Dose',df.columns,limit=1)[0][0]
        
        default_id_index = df.columns.get_loc(default_id_col)
        default_time_index = df.columns.get_loc(default_time_col)
        default_conc_index = df.columns.get_loc(default_conc_col)
        default_dose_index = df.columns.get_loc(default_dose_col)


       
        # Let user define the columns
        col1, col2 = st.columns(2)
        with col1: 
            st.write('Compulsory Information')
            ID_col = st.selectbox('Select a column that represent ID',df.columns,index = default_id_index)
            Time_col = st.selectbox('Select a column that represent Time',df.columns,index = default_time_index)
            Concentration_col = st.selectbox('Select a column that represent Concentration',df.columns, index = default_conc_index)
            Dose_col = st.selectbox('Select a column that represent Dose',df.columns,index = default_dose_index)
        with col2: 
            st.write('Additional Information')
            Age_col = st.selectbox('Select a column that represent Age',df.columns,index=None)
            Weight_col = st.selectbox('Select a column that represent Body Weight',df.columns,index=None)
            Gender_col = st.selectbox('Select a column that represent Gender',df.columns,index=None)
            CLCR_col = st.selectbox('Select a column that represent Clearance Creatinine',df.columns,index=None)

        # Extract column from df
        col_list = [ID_col,Time_col,Concentration_col,Dose_col,Age_col,Weight_col,Gender_col,CLCR_col]
        col_name = ['ID','Time','Conc','Dose','Age','Weight','Gender','CLCR']
        extracted_col = []
        extracted_col_name = []
        for column, column_name in zip(col_list,col_name):
            if column is not None: 
                extracted_col.append(column)
                extracted_col_name.append(column_name)
                
       
        extract_df = df[extracted_col]
        extract_df.columns = extracted_col_name

        # Allow the edit from user on the dataframe
        st.subheader('Data Frame')
        st.caption('Double check your data. You can manipulate data directly on the displayed table.')
        edited_extract_df = st.data_editor(extract_df,num_rows="dynamic")

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
          if Age_col is not None: 
              st.subheader('Age Distribution')
              nbins_age = st.slider('Edit the number of bins for Age distribution:',value = 20)
              fig = px.histogram(edited_extract_df, x='Age',nbins=nbins_age)
              fig.update_layout(title='Age Distribution', xaxis_title='Age', yaxis_title='Freq.')
              plot = st.plotly_chart(fig, use_container_width=True)
        
      col3, col4 = st.columns(2)
      with col3: 
          if Weight_col is not None: 
            st.subheader('Weight Distribution')
            nbins_weight = st.slider('Edit the number of bins for Weight distribution:',value = 20)
            fig = px.histogram(edited_extract_df, x='Weight',nbins=nbins_weight)
            fig.update_layout(title='Weight Distribution', xaxis_title='Weight', yaxis_title='Freq.')
            plot = st.plotly_chart(fig, use_container_width=True)
      
      
      with col4:
          if CLCR_col is not None: 
            st.subheader('Creatinine Cleareance Distribution')
            nbins_CLCR = st.slider('Edit the number of bins for CRCL distribution:',value = 20)
            fig = px.histogram(edited_extract_df, x='CLCR',nbins=nbins_CLCR)
            fig.update_layout(title='CLCR Distribution', xaxis_title='Creatinine Clearance', yaxis_title='Freq.')
            plot = st.plotly_chart(fig, use_container_width=True)    



      # Display the Pk profile
      dose_profile = st.toggle('Display PK profile by Dose', value = False)
      if dose_profile:
        st.title('PK Profile by Dose')
        col1, col2 = st.columns(2)
      
        unique_doses = edited_extract_df['Dose'].unique()
      
        for i, dose in enumerate(unique_doses):
            dose_specific_df = edited_extract_df[edited_extract_df['Dose']==dose]
            fig = px.scatter(dose_specific_df, x='Time', y='Conc', title=f'Dose: {dose}')
            if i % 2 == 0:
                with col1:
                    st.plotly_chart(fig)
            else:
                with col2:
                    st.plotly_chart(fig)
    
    
    else:
        st.info('You should upload the file first')







with non_compartment:
    
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
        
        for id in df['ID'].unique():
            df_id = df[df['ID'] == id].dropna()
            
            # Skip if less than 3 points 
            if df_id.shape[0] < 3:
                st.error(f'ID "{id}" has less than 3 data points. Double check the input data')
                continue  

            else:
                # Calculate AUC 0-last
                auc_0_last = np.trapz(y=df_id['Conc'], x=df_id['Time'])
            
                # Find optimal number of lamda points
                r2_list = []
                slope_list = []
                X = df_id[['Time']]
            
                for n_points in range(3, df_id.shape[0] + 1):
                    df_id_point = df_id.iloc[-n_points:, :]
                    X_points = df_id_point[['Time']]
                    Y_points = np.log(df_id_point['Conc'] + 0.00001).values.reshape(-1, 1)
                    model = LinearRegression()
                    model.fit(X_points, Y_points)
                    prediction = model.predict(X_points)
                    r2 = r2_score(y_true=Y_points, y_pred=prediction)
                    r2_list.append(r2)
                    slope_list.append(model.coef_[0][0])

            # Skip if r2_list is empty
                if not r2_list:
                    continue  
            
                else:
                    r2_max_index = np.argmax(r2_list)
                    slope = slope_list[r2_max_index]
                    auc_last_inf = -df_id['Conc'].iloc[-1] / slope
                    dose = df_id['Dose'].unique()[0]
                    auc_0_inf = auc_0_last + auc_last_inf
                    apparent_CL = dose / auc_0_inf
                    half_life = -np.log(2)/slope

                # Add to data dictionary
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
        return df_analysis

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

    st.header('Non-Compartmental Analysis')
    st.write("Non-compartmental analysis (NCA) is a method used in pharmacokinetics to analyze and interpret drug concentration data without assuming a specific compartmental model for the body's drug distribution and elimination processes. Instead of relying on a predetermined biological model, NCA calculates pharmacokinetic (PK) parameters directly from the observed concentration-time data.")
    st.write("\n")
    st.write("One of the most important parameters estimated from NCA is the **terminal slope**, also known as the terminal rate constant. To estimate this parameter, the algorithm considers a certain number of last data points, referred to as lambda points. The consideration starts with 3 points, then gradually increase overtime. During that process, a linear regression is performed between the logarithm concentration and time of these points. Subsequently, the optimal number of lambda points is selected, and the corresponding slope is identified as the terminal rate constant.")
    st.write("\n")
    st.write("*However, it is important to note that the terminal slope can be either ka or ke, depending on the PK scenario. The further methods to estimate other PK parameters are decribed in the❓Helps page.*")
    st.write("\n")
    st.write("\n")



    st.subheader('Analysis Results')
    
    if edited_extract_df is not None:
        
        non_compartment_df = non_compartmental_analysis(edited_extract_df)
        if not non_compartment_df.empty:
            covariate_df = edited_extract_df.drop(['Time','Conc','Dose'],axis = 1).drop_duplicates(subset='ID')
            analysis_covariate_df = non_compartment_df.merge(covariate_df, on = 'ID')
            non_compartment_df_final = st.data_editor(analysis_covariate_df, num_rows="dynamic")
            
            #Display the selection profile:
            plots = st.toggle('Display the individual profiles')
            counts = non_compartment_df_final['ID'].nunique()
            if plots:
                col1, col2 = st.columns(2)
                for id, lambda_points, count in zip(non_compartment_df_final['ID'],non_compartment_df_final['Number of Lambda Points'],range(counts)):
                    df_whole_profile = edited_extract_df[edited_extract_df['ID']==id].dropna()
                    df_lambda_profile = df_whole_profile.iloc[-lambda_points:,:].dropna()

                    df_whole_profile['log_conc'] = np.log(df_whole_profile['Conc'])
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
    st.title('One-Compartmental Analysis')
    st.write('write some introduction here')