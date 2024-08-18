import streamlit as st
import pandas as pd 
import numpy as np
from thefuzz import process


def data_preprocessing(df):
    '''This function helps to change the columns' names of the initial dataframe to the unified name that used during the simulation and analysis.
    
    Parameters:
        df (PandasDataFrame): the initial dataset.

    Returns: 
        extract_df (PandasDataFrame): the manipulated dataset, with the unified columns' name.
    '''
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
        st.write('**Compulsory Information**')
        ID_col = st.selectbox('Select a column that represent ID', df.columns, index=default_id_index)
        Time_col = st.selectbox('Select a column that represent Time', df.columns, index=default_time_index)
        Concentration_col = st.selectbox('Select a column that represent Concentration', df.columns, index=default_conc_index)
        Dose_col = st.selectbox('Select a column that represent Dose', df.columns, index=default_dose_index)
    with col2:
        st.write('**Additional Information**')
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

    return extract_df