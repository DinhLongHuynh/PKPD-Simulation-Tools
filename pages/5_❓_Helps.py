import streamlit as st
import pandas as pd

st.set_page_config(page_title='Helps', page_icon='❓', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title('❓ Helps')
st.write('''This page contains further interpretation of the parameters and variables using in the different simulation applications.
         
The application provides the common standard units used in clinical trial, i.e. hour for time, mg for dose, mg/L for concentration.
However, the units can be flexible depends on users' case. In this scenario, users should keep in mind the units when import and interpret the simulation results.''')

st.header('Combine Dosing Reigmen Simulation PK')
st.caption('Further description of the parameters and variables used in the simulation:')
st.write('- **Dose IV (mg):** The data type is **float**. This is the dose of intravenous drug.')
st.write('- **Infusion Duration (h):** The data type is **integer**. This is the infusion time of the i.v. drugs. Because the scenario is prolonged infusion drugs, the value of Infusion Duration should be higher than 0 hour.')
st.write('- **Dose IM (mg):** The data type is **float**. This is the dose of intramuscular drug in mg. However, it can be used for oral drugs as well.')
st.write('- **Start point IM (h):** The data type is **integer**. This is the time point when the intramuscular drug is injected. If the starting point IM is set as 0 hour, that means we start the IM drug from the begining, at the same time with IV drug.')
st.write('- **Interval Dose IM (h):** The data type is a **list of integer**. The values are the relative time points when you want to inject the i.m. drug. Because time points are relative, the first i.m. dose always starts at 0 hour. For example, if you want to inject triple dose a day of an i.m drug, the input should be: 0,8,16 hour.')
st.write('- **Clearance (L/h):** The data type is **float**. This is the clearance.')
st.write('- **Volume of Distribution (L):** The data type is **float**. This is the Volume of Distribution.')
st.write('- **Absorption Constant (h-1):** The data type is **float**. This is the absorption rate constant, or ka.')
st.write('- **Bioavailability:** The data type is **float**. This is the total bioavailability of drugs in the scale from 0 to 1. For example, if the bioavailability is 85%, the input value should be 0.85.')
st.write('- **Simulation Range (h):** The data type is **integer**. This is the endpoint of the time range on the simulation plot. For example, if you input 100, the plot will show the simulation within the range between 0 and 100 hour.')


st.header('PK Simulation')
st.caption('Further description of the parameters and variables used in the simulation:')
st.write('- **Dose (mg):** The data type is **float**. This is the dosage used for simulation.')
st.write('- **Population Clearance (L/h):** The data type is **float**. This is the mean of clearance among the whole population.')
st.write('- **Population Volume of Distribution (L):** The data type is **float**. This is the mean of volume of distribution among the whole population.')
st.write('- **Population Absorption Constant (h-1):** The data type is **float**. This is the mean of ka among the whole population. In case you want to simulate an intravenous drug, the value of ka can be blank, which means ignoring the absorption process.')
st.write('- **Population Bioavailability:** The data type is **float**. This is the mean total bioavailability of drugs among the whole population. The value is scaled from 0 to 1. For example, if the bioavailability is 85%, the input value should be 0.85.')
st.write('- **Number of Patients:** The data type is **integer**. This is the number of patients that you want to simulate.')
st.write("- **C Limit (mg/L):** The data type is **float**. This is the concentration that you don't want the drug to exceed it. The value can be a blank or a float number.")
st.write('- **Time range (h)**: The data type is **integer**. This is the endpoint of the time range on the simulation plot. For example, if you input 100, the plot will show the simulation within the range between 0 and 100 hour.')
st.write("- **Omega:**: The data type is **float**. Each PK parameter has its corresponding omega, which represents the standard deviation of the normal distribution with a mean of 0. Then, a sample of a specific size, which is the number of patients, is picked from this distribution, and each value in the sample (denoted as ni) is used to estimate the variability of the parameters. The estimation follows this formula: ")
st.latex(r'Parameter_{i} = Parameter_{population} \times e^{n_{i}}')
st.write("- **Sigma Residual**: The data type is **float**. This is the standard deviation of the residual distribution. From this distribution, a sample with specific size, which is number of patients is picked, and each residual values will be added to the final concentration with the following formula:")
st.latex(r'Concentration_{i,final} = Concentration_{i} + Residual_{i}')


st.header('PD Simulation')
st.caption('Further description of the parameters and variables used in the simulation:')
st.write('- **Population Emax:** The data type is **float**. This is the mean of maximum effect among the whole population. The unit of Emax depends on the diseases or biomarkers.')
st.write('- **Population EC50:** The data type is **float**. This is the mean of half maximal effective concentration among the whole population. The unit of EC50 depends on the concentration of the investigating drugs. For example, if the contration of drug has unit of mg/L, the EC50 also has the unit of mg/L.')
st.write('- **Population Ebaseline:** The data type is **float**. This is the mean baseline effect of the whole population, when the concentration of drug at 0. The unit of Ebaseline is the same as Emax.')
st.write('- **Population Hill Coefficient:** The data type is **float**. This is the mean hill among the whole population.')
st.write('- **Number of Patients:** The data type is **integer**. This is the number of patients that you want to simulate.')
st.write("- **E Limit:** The data type is **float**. This is the drug effect that you don't want to exceed. The value can be a blank or a float number. The unit of E limit is the same as Emax and Ebaseline.")
st.write('- **Concentration range:** The data type is **integer**. This is the endpoint of the concentration range on the simulation plot. For example, if you input 100, the plot will show the simulation within the range between 0 and 100 unit of concentration. The unit will be the same as your input.')
st.write("- **Omega:**: The data type is **float**. Each PD parameter has its corresponding omega, which represents the standard deviation of the normal distribution with a mean of 0. Then, a sample of a specific size, which is the number of patients, is picked from this distribution, and each value in the sample (denoted as ni) is used to estimate the variability of the parameters. The estimation follows this formula: ")
st.latex(r'Parameter_{i} = Parameter_{population} \times e^{n_{i}}')
st.write("- **Sigma Residual**: The data type is **float**. This is the standard deviation of the residual distribution. From this distribution, a sample with specific size, which is number of patients is picked, and each residual values will be added to the final effect with the following formula:")
st.latex(r'Effect_{i,final} = Effect_{i} + Residual_{i}')
