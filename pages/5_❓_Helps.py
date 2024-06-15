import streamlit as st
import pandas as pd

st.set_page_config(page_title='Helps', page_icon='❓', layout="wide", initial_sidebar_state="auto", menu_items=None)
st.title('❓ Helps')
st.write('''This page contains further interpretation of the parameters and variables used in the different simulation applications.

The application provides the common standard units used in clinical trials, i.e. hour for time, mg for dose, mg/L for concentration. However, the units can be flexible depending on the users' case. In this scenario, users should keep in mind the units when interpreting the simulation and analysis results.''')

st.write("\n")
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h2 class="centered-text">---------------------💊💊💊---------------------</h2>', unsafe_allow_html=True)
st.write("\n")

st.header('PK Simulation')
st.caption('Further descriptions of the parameters and variables used in the simulation:')
st.write('- **Dose (mg):** The data type is **float**. This is the dosage used for simulation.')
st.write('- **Population Clearance (L/h):** The data type is **float**. This is the mean of clearance among the whole population.')
st.write('- **Population Volume of Distribution (L):** The data type is **float**. This is the mean volume of distribution among the whole population.')
st.write('- **Population Absorption Constant (h-1):** The data type is **float**. This is the mean of ka among the whole population. In case you want to simulate an intravenous drug, the value of ka can be blank, which means ignoring the absorption process.')
st.write('- **Population Bioavailability:** The data type is **float**. This is the mean total bioavailability of drugs among the whole population. The value is scaled from 0 to 1. For example, if the bioavailability is 85%, the input value should be 0.85.')
st.write('- **Number of Patients:** The data type is **integer**. This is the number of patients that you want to simulate.')
st.write("- **C Limit (mg/L):** The data type is **float**. This is the concentration that you don't want the drug to exceed. The value can be a blank or a float number.")
st.write('- **Time range (h)**: The data type is **integer**. This is the endpoint of the time range on the simulation plot. For example, if you input 100, the plot will show the simulation within the range between 0 and 100 hour.')
st.write("- **Omega:**: The data type is **float**. Each PK parameter has its corresponding omega, which represents the standard deviation of the normal distribution with a mean of 0. Then, a sample of a specific size, which is the number of patients, is picked from this distribution, and each value in the sample (denoted as ni) is used to estimate the variability of the parameters. The estimation follows this formula: ")
st.latex(r'Parameter_{i} = Parameter_{population} \times e^{n_{i}}')
st.write("- **Sigma Residual**: The data type is **float**. This is the standard deviation of the residual distribution. From this distribution, a sample with a specific size, which is the number of patients, is picked and each residual value will be added to the final concentration with the following formula:")
st.latex(r'Concentration_{i,final} = Concentration_{i} + Residual_{i}')

st.write("\n")
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h2 class="centered-text">---------------------💊💊💊---------------------</h2>', unsafe_allow_html=True)
st.write("\n")

st.header('PD Simulation')
st.caption('Further descriptions of the parameters and variables used in the simulation:')
st.write('- **Population Emax:** The data type is **float**. This is the mean of maximum effect among the whole population. The unit of Emax depends on the diseases or biomarkers.')
st.write('- **Population EC50:** The data type is **float**. This is the mean of half the maximal effective concentration among the whole population. The unit of EC50 depends on the concentration of the investigating drugs. For example, if the concentration has a unit of mg/L, the EC50 also has a unit of mg/L.')
st.write('- **Population Ebaseline:** The data type is **float**. This is the mean baseline effect of the whole population when the concentration of drug at 0. The unit of Ebaseline is the same as Emax.')
st.write('- **Population Hill Coefficient:** The data type is **float**. This is the mean hill among the whole population.')
st.write('- **Number of Patients:** The data type is **integer**. This is the number of patients that you want to simulate.')
st.write("- **E Limit:** The data type is **float**. This is the drug effect that you don't want to exceed. The value can be a blank or a float number. The unit of E limit is the same as Emax and Ebaseline.")
st.write('- **Concentration range:** The data type is **integer**. This is the endpoint of the concentration range on the simulation plot. For example, if you input 100, the plot will show the simulation within the range between 0 and 100 units of concentration. The unit will be the same as your input.')
st.write("- **Omega:**: The data type is **float**. Each PD parameter has its corresponding omega, which represents the standard deviation of the normal distribution with a mean of 0. Then, a sample of a specific size, which is the number of patients, is picked from this distribution, and each value in the sample (denoted as ni) is used to estimate the variability of the parameters. The estimation follows this formula: ")
st.latex(r'Parameter_{i} = Parameter_{population} \times e^{n_{i}}')
st.write("- **Sigma Residual**: The data type is **float**. This is the standard deviation of the residual distribution. From this distribution, a sample with a specific size, which is the number of patients, is picked and each residual value will be added to the final effect with the following formula:")
st.latex(r'Effect_{i,final} = Effect_{i} + Residual_{i}')

st.write("\n")
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h2 class="centered-text">---------------------💊💊💊---------------------</h2>', unsafe_allow_html=True)
st.header('Multiple Dose PK Simulation')
st.caption('Further descriptions of the parameters and variables used in the simulation:')
st.write('- **Absorption Rate Constant (h-1):** The data type is **float**. This is the rate constant that characterizes the absorption, ka. If your dosing regimen has at least 1 non-iv dose, the ka is mandatory. Otherwise, this value can be left as None.')
st.write('- **Elimination Rate Constant (h-1):** The data type is **float**. This is the rate constant that characterizes the elimination, ke.')
st.write('- **Volume of Distribution (L):** The data type is **float**. This is the volume of distribution.')
st.write('- **Simulation Range (h):** The data type is **float**. This is the endpoint of the time range on the simulation plot. For example, if you input 100, the plot will show the simulation within the range between 0 and 100 hour.')
st.write('- **Start time (h):** The data type is *float*. This is the time point when you start the dose.')
st.write('- **Dose Amount (mg):** The data type is **float**. This is dose of the drug.')
st.write('- **Infusion Duration (h):** The data type is **integer**. This is the specific parameter of IV drugs. If the scenario is prolonged infusion drugs, the value of Infusion Duration should be higher than 0 hour. Otherwise, this value can be left as None.')
st.write('- **Bioavailability:** The data type is **float**. This is the total bioavailability of drugs on a scale from 0 to 1. For example, if the bioavailability is 85%, the input value should be 0.85.')



st.write("\n")
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h2 class="centered-text">---------------------💊💊💊---------------------</h2>', unsafe_allow_html=True)
st.write("\n")

st.header('PK Analysis')
st.subheader('File Characteristic')
st.write('- **Imported file**: The input file format should be a comma-separated value (.csv). After importing the data, the "File Characteristic" page allows users to select the columns in the input file that correspond to the given information.')
st.write("- **Compulsory Information**: they are the fundamental data that one clinical study must have. If your dataset doesn't have enough compulsory information, you should double-check your data, or your study design. ")
st.write("- **Additional Information**: they are optional. If they are not available, you can leave it blank.")
st.write("\n")
st.write("\n")

st.subheader('Non-Compartmental Analysis')
st.write("Non-compartmental analysis (NCA) is a method used in pharmacokinetics to analyze and interpret drug concentration data without assuming a specific compartmental model for the body's drug distribution and elimination processes. Instead of relying on a predetermined biological model, NCA calculates pharmacokinetic (PK) parameters directly from the observed concentration-time data.")
st.caption("Below are detailed descriptions of the PK parameters derived from the analysis:")
st.write("- **Slope:** This is the terminal rate constant of drug's PK profile. The unit of the terminal slope is the inverse of the time unit used in the analysis. For example, if the time unit is hours (h), the terminal slope unit is 1/h. To determine the slope, the algorithm tries to make a linear regression between the logarithm of concentration and time (equation below). This regression is carried out using different numbers of last data points, also known as lambda points. The number of lambda points that results in the highest R-squared value during the regression is selected to calculate the slope. However, it is important to note that the terminal slope can be either ka or ke, depending on the PK scenario.")
st.markdown(
    """
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="centered-text"><i>On the terminal phase:</i></div>', unsafe_allow_html=True)
st.latex(r'ln(Concentration) = ln(Concentration_{0}) - slope \times Time')
st.write('- **Number of lambda points:** The chosen number of last data points on the PK profile used for linear regression.')
st.write('- **R2 value:** R2 values of the linear regression between logarithm of concentration and time.')
st.write('- **AUC_0-last:** The AUC from time point 0 to the last measured time point. This AUC has a unit depending on the concentration and time used in the analysis. For example, if the unit of concentration is mg/L and the unit of time is hour, AUC has the unit of mg*h/L. AUC_0-last is calculated by the sum of the trapezoid area created by different data points.')
st.latex(r'AUC_{0-last} = \sum_{i=2}^{n} \frac{(C_{i} + C_{i-1}) \times (t_{i} - t_{i-1})}{2}')
st.write('- **AUC_last-inf:** The AUC from the last measured time point to the infinity. This AUC has a unit depending on the concentration and time used in the analysis. For example, if the unit of concentration is mg/L and the unit of time is hour, AUC has the unit of mg*h/L. AUC_last-inf is estimated from the last concentration and the terminal slope, using the following formula.')
st.latex(r'AUC_{last-inf} = \frac{\text{Concentration}_{\text{last}}}{\text{slope}}')
st.write('- **AUC_0-inf:** The AUC from time point 0 to the infinity. This AUC has a unit depending on the concentration and time used in the analysis. For example, if the unit of concentration is mg/L and the unit of time is hour, AUC has the unit of mg*h/L. AUC_0-inf is the sum of AUC_0-last and AUC_last-inf.')
st.latex(r'AUC_{0-inf} = \sum_{i=2}^{n} \frac{(C_{i} + C_{i-1}) \times (t_{i} - t_{i-1})}{2} + \frac{\text{Concentration}_{\text{last}}}{\text{slope}}')
st.write("- **Apparent Clearance**: This is the drug's total apparent clearance. It has the unit of volume divided by time. Therefore the unit depends on the concentration and time unit used in the analysis. Clearance is calculated from AUC_0-inf and the Dose. It is called apparent clearance as it incorporates the drug bioavailability. If you have information about the drug's bioavailability, you can calculate the true value of clearance.")
st.latex(r'CL_{Apparent} = \frac{CL}{F} = \frac{\text{Dose}}{AUC_{0-inf}}')
st.write('- **Half life**: This is the time it takes for the body to eliminate half of the drug. The half life has the same unit as the time unit used in the analysis.')
st.latex(r'T_{1/2} = \frac{ln(2)}{slope}')

st.subheader('One-Compartmental Analysis')
st.write('One-compartmental analysis (OCA) is a method used in pharmacokinetics to analyze and interpret drug concentration data by assuming the body behaves as a single, homogeneous compartment. OCA is the model-based method, which uses the data to fit the predefined model or equations.')
st.write('The important assumption of the analysis in this application is that drug absorption and elimination follow first-order kinetic. There are two scenarios used for analysis, which are IV drug and non-IV drug.')
st.write("\n")
st.write('**1) IV drug analysis**: This scenario can be used for drugs that are instantaneously absorbed into the central plasma compartment. The model used for this scenario is described by the following equation:')
st.latex(r'ln(C) = ln(C_{0}) - k_{e} \times Time')
st.caption('Further descriptions of the variables and parameters used in the linear regression:')
st.write('- **ln(C)** _ variable: This is the logarithm of concentration, which is the dependent variable of the linear regression. This is the unitless variable.')
st.write('- **Time** _ variable: This is the time point when the concentration is measured, which is the independent variable of the linear regression. The unit of time can be flexible depending on the study design.')
st.write('- **ln(C0)** _ parameter: This is the logarithm of initial concentration, right after the drug administration into the body. The logarithm is a unitless variable but the initial concentration has the same unit with the concentration used in the study.')
st.write('- **ke** _ parameter: This is the elimination rate constant. The unit of ke is the inverse of the time unit used in the analysis. For example, if the time unit is hours (h), the ke unit is 1/h. ')
st.write('- **R2** _ model evaluation metric: This is the R-squared score for the linear regression. It is a unitless metric.')
st.write('- **RMSE** _ model evaluation metric: This is the root mean squared error for the linear regression. It has the same unit with the concentration used in the study.')
st.write('- **Apparent Vd** _ generated parameter: This is the drug volume of distribution. It can have flexible units depending on the dose and the concentration used in the study. It is called apparent Vd as it incorporates the drug bioavailability. If you have information about the drug bioavailability, you can calculate the true value of Vd.')
st.latex(r'V_{d,Apparent} = \frac{Dose}{C_{0}}')
st.write('- **Apparent CL** _ generated parameter: This is the drug total apparent clearance. It has the unit of volume divided by time, therefore the unit depends on the concentration and time unit used in the analysis. Clearance is calculated from ke and Vd. It is called apparent clearance as it incorporates the drug bioavailability. If you have information about the drug bioavailability, you can calculate the true value of clearance.')
st.latex(r'CL_{Apparent} = k_{e} \times V_{d,Apparent}')
st.write('- **AUC_0-inf** _ generated parameter: The AUC from time point 0 to the infinity. This AUC has a unit that depends on the concentration and time used in the analysis. For example, if the unit of concentration is mg/L and the unit of time is hour, AUC has the unit of mg*h/L.')
st.latex(r'\text{AUC}_{0-\infty} = \int_{0}^{\infty} C_0 \cdot e^{-k t} \, dt = \frac {C_{0}}{k_{e}}')
st.write('- **Half life** _ generated parameter: This is the time it takes for the body to eliminate half of the drug. The half life has the same unit with the time unit used in the analysis.')
st.latex(r'T_{1/2} = \frac{ln(2)}{k_{e}}')

st.write("\n")
st.write('**2) Non-IV drug analysis**: This scenario can be used for drugs that are gradually absorbed into the central plasma compartment. The model used for this scenario is described by the following equation:')
st.latex(r'C = \frac{F \times \text{Dose} \times k_a}{V_{d} \times (k_a - k_{e})} \times \left( e^{-k_{e} \times time} - e^{-k_a \times time} \right)')
st.write("The non-linear model fitting process requires initial guesses for the parameters, which can be based on previous studies. If the initial guesses are significantly different from the actual values, alternative values should be considered.")
st.caption('Further descriptions of the  variables and parameters used in the non-linear regression:')
st.write("- **C** _ variable: This is the drug's plasma concentration, which is the dependent variable of the non-linear regression. The unit of concentration can be flexible depending on your study design.")
st.write('- **Time** _ variable: This is the time point when the concentration is measured, which is the independent variable of the linear regression. The unit of time can be flexible depending on the study design.')
st.write("- **F** _ constant: This is the total bioavailability of the drug, which is unitless. It can be determined from the previous study or estimated using different methodologies. The reason why F is a predefined constant instead of a parameter is that it will require at least 40 data points to generate a reliable regression if F is included as a parameter, which is unavailable in the clinical trial scenario.")
st.write("- **Dose** _ constant: This is the dose of the correponding id. The unit can be flexible depending on your study.")
st.write('- **ka** _ parameter: This is the absorption rate constant. The unit of ka is the inverse of the time unit used in the analysis. For example, if the time unit is hours (h), the ke unit is 1/h.')
st.write('- **ke** _ parameter: This is the elimination rate constant. The unit of ke is the inverse of the time unit used in the analysis. For example, if the time unit is hours (h), the ke unit is 1/h.')
st.write("- **Vd** _ parameter: This is the volume of distribution. The unit of Vd can be flexible depending on your study.")
st.write('- **RMSE** _ model evaluation metric: This is the root mean squared error for the linear regression. It has the same unit with the concentration used in the study.')
st.write('- **Tmax** _ generated parameter: This is the time needed for the drug to reach its maximum concentration. It has the same unit as the time used in the study.')
st.latex(r'T_{max} = \frac{ln(k_{a})-ln(k_{e})}{k_{a}-k_{e}} ')
st.write('- **Cmax** _ generated parameter: This is the maximum concentration of drug. It has the same unit with the concentration used in the study.')
st.latex(r'C_{max} = \frac{F \times \text{Dose} \times k_a}{V_{d} \times (k_a - k_{e})} \times \left( e^{-k_{e} \times T_{max}} - e^{-k_a \times T_{max}} \right)')
st.write('- **Half life**: This is the time it takes for the body to eliminate half of the drug. The half life has the same unit as the time unit used in the analysis. Half life is determined by the following formula. In the formula, k is the terminal slope of the PK profile. If the drug has ka < ke, the k is ka. Otherwise, it is ke.')
st.latex(r'T_{1/2} = \frac{ln(2)}{k}')
st.write('- **AUC_0-inf** _ generated parameter: The AUC from time point 0 to the infinity. This AUC has a unit depends on the concentration and time used in the analysis. For example, if the unit of concentration is mg/L and the unit of time is hour, AUC has the unit of mg*h/L. To determine AUC_0-inf, the integral from 0 to infinity of the model equation is considered.')
st.latex(r'\text{AUC}_{0-\infty} = \int_{0}^{\infty} \frac{F \times \text{Dose} \times k_a}{V_d \times (k_a - k_e)} \times \left( e^{-k_e \times t} - e^{-k_a \times t} \right) \, dt')
st.write('- **Clearance** _ generated parameter: This is the total clearance of drug. It has the unit of volume divided by time, therefore the unit depends on the concentration and time unit used in the analysis. Clearance is calculated from Dose and AUC_0-inf.')
st.latex(r'CL = \frac{\text{Dose}}{AUC_{0-inf}}')
