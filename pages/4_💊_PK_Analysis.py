import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from thefuzz import process

st.set_page_config(page_title='PK Analysis', page_icon='💊', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title("💊 PK Analysis Tools")
introduction, file_characteristic, visualization, non_compartment, one_compartment = st.tabs(["Introduction",'File Characteristic','Data Visulization',"Non-compartmental Model", "One-compartmental Model"])



with introduction:
    st.write('''This page helps users to analyse the clinical trial data. There are two approach in the analysis: 
         
1) Non-compartmental Analysis: the analysis will base on the discrete data point on the PK profile. Base on that to directly draw the conclusion of several PK parameters.
2) One-compartmental Analysis: the analysis will fit the observed data to the predefined model and then derived Pk parameters from the model. ''')

    st.subheader('Input data')
    file = st.file_uploader('Import your csv dataset here')
    df = None
    if file is not None:
        df = pd.read_csv(file)
        st.caption('Next step is characterising the data with File Characteristic tab.')
       

   
       
    


with file_characteristic:
    if df is not None:
        st.subheader("File Characteristic")
        st.caption('Select the column in your file that corresponding to these descriptions')


        # Use the similarity check to pre-assign columns
        default_id_col = process.extract('ID',df.columns,limit=1)[0][0]
        default_time_col = process.extract('Time',df.columns,limit=1)[0][0]
        default_conc_col = process.extract('Concentration',df.columns,limit=1)[0][0]
        default_dose_col = process.extract('Dose',df.columns,limit=1)[0][0]
        
        default_id_index = df.columns.get_loc(default_id_col)
        default_time_index = df.columns.get_loc(default_time_col)
        default_conc_index = df.columns.get_loc(default_conc_col)
        default_dose_index = df.columns.get_loc(default_dose_col)


       
        # Let user define the columns
        col1, col2 = st.columns(2)
        with col1: 
            st.write('Fundamental Information')
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
    st.error('The page is still in progress')
    st.header('Coming Soon')





with one_compartment:
    st.error('The page is still in progress')
    st.header('Coming Soon')