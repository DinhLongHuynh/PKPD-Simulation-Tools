import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def distribution_plots(data,x,xlabel,ylabel,title):
    '''This function helps to draw the histogram of feature X in the dataframe
    Parameters:
        data (PandasDataFrame): Data Frame that contain feature X.
        X (str): Column name of feature X.
        xlabel (str): label for x axis.
        ylabel (str): label for y axis
        title (str): title for the whole plot.
    '''

    st.subheader(title)
    nbins = st.slider(f'Edit the number of bins for {x} distribution:',value = 20)
    fig = px.histogram(data, x=x,nbins=nbins)
    fig.update_traces(marker_line_color='black', marker_line_width=1)
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    config_dis = {
        'toImageButtonOptions': {
        'format': 'png', 
        'filename': f'{x}_distribution',
        'height': None,
        'width': None,
        'scale': 5 }}
    plot = st.plotly_chart(fig, use_container_width=True, config = config_dis)


def id_count_by_dose(df,gender):
    '''This function helps to visualize the ID counts by dose (and gender).
    Parameters:
        df (PandasDataFrame): the preprocessed dataframe by pkpd_sian.preprocessing.data_preprocessing function.
        gender (boolean): indicate if gender information available.
    '''

    if gender: 
        # Hanlding data
        st.subheader('Number of ID by Dose and Gender')
        id_count_df = df.groupby(['Dose','Gender'])['ID'].nunique().reset_index(name='ID_count')
        id_count_df['Dose'] = id_count_df['Dose'].astype(str)+'mg' # Turn dose into category for better visualization
        id_count_df['Gender'] = id_count_df['Gender'].astype(str)

        # Draw the plot
        default_plot_title = 'Number of ID by Dose and Gender'
        default_xlabel = 'ID Counts'
        default_ylabel = 'Dose'
        fig = px.bar( id_count_df, x='ID_count', y='Dose', color='Gender', orientation='h',title = default_plot_title)
        fig.update_layout(xaxis_title=default_xlabel, yaxis_title=default_ylabel, legend_title_text='Gender')
        config = {
            'toImageButtonOptions': {
            'format': 'png', 
            'filename': 'ID_counts_by_Dose_Gender',
            'height': None,
            'width': None,
            'scale': 5  }}
        plot = st.plotly_chart(fig, use_container_width=True)

            # Plot characteristic
        plot_title = st.text_input('Edit plot title:',value = 'Number of ID by Dose and Gender')
            
        col3, col4 = st.columns(2)
        with col3:
            xlabel = st.text_input('Edit x label:',value = 'ID Counts')
        with col4:
            ylabel = st.text_input('Edit y label:',value = 'Dose')
            
        fig.update_layout(title=plot_title, xaxis_title=xlabel, yaxis_title=ylabel)
        plot.plotly_chart(fig, use_container_width=True,config=config)
        
    else:
        # Handling data: 
        st.subheader('Number of ID by Dose')
        id_count_df = df.groupby('Dose')['ID'].nunique().reset_index(name='ID_count')
        id_count_df['Dose'] = 'Dose ' + id_count_df['Dose'].astype(str) # Turn dose into category for better visualization

        # Draw plot
        default_plot_title = 'Number of ID by Dose'
        default_xlabel = 'ID Counts'
        default_ylabel = 'Dose'
        fig = px.bar(id_count_df, x='ID_count', y='Dose', orientation='h',color = 'Dose', title = default_plot_title ,color_discrete_sequence=px.colors.qualitative.Safe)
        fig.update_layout(xaxis_title=default_xlabel, yaxis_title=default_ylabel)
        config = {
            'toImageButtonOptions': {
            'format': 'png', 
            'filename': 'ID_counts_by_Dose',
            'height': None,
            'width': None,
            'scale': 5  }}
        plot = st.plotly_chart(fig, use_container_width=True,config=config)

        # Plot characteristic
        plot_title = st.text_input('Edit plot title:',value = 'Number of ID by Dose')
            
        col3, col4 = st.columns(2)
        with col3:
            xlabel = st.text_input('Edit x label:',value = 'ID Counts')
        with col4:
            ylabel = st.text_input('Edit y label:',value = 'Dose')
            
        fig.update_layout(title=plot_title, xaxis_title=xlabel, yaxis_title=ylabel)

        plot.plotly_chart(fig, use_container_width=True,config = config)


def pk_profile_by_dose(df):
    '''This function helps to visualize the pharmacokinetic profile of each dose.
    Parameters:
        df (PandasDataFrame): the preprocessed dataframe by pkpd_sian.preprocessing.data_preprocessing function.
    '''

    st.title('PK Profile by Dose')
    col1, col2 = st.columns(2)
    unique_doses = df['Dose'].unique()
    for i, dose in enumerate(unique_doses):
        dose_specific_df = df[df['Dose']==dose]
        fig = px.scatter(dose_specific_df, x='Time', y='Conc', title=f'Dose: {dose}')
        config_dose_profile = {
            'toImageButtonOptions': {
            'format': 'png', 
            'filename': f'PK_dose_{dose}',
            'height': None,
            'width': None,
            'scale': 5 }}
            # Plot on 2-column page layout
        if i % 2 == 0:
            with col1:
                st.plotly_chart(fig,config = config_dose_profile)
        else:
            with col2:
                st.plotly_chart(fig,config = config_dose_profile)
        