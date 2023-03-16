import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# using the style for the plot
plt.style.use('seaborn-v0_8-darkgrid')

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 12}

matplotlib.rc('font', **font)


st.set_page_config(page_title="File Explorer", page_icon="📈")

def save_img(fig):
    fig.savefig('prova.png', dpi=600, bbox_inches='tight')


###############################################################
#######################   DATA LOADER #########################
###############################################################
# Importing file with the data
uploaded_file_data = st.file_uploader('DATA FILE ')

try:
    file=pd.read_excel(uploaded_file_data)

except:
    try:
            file=pd.read_excel(uploaded_file_data)
    except:      
            pass


file_thresholds = pd.read_excel('Table Formatted RANGES.xlsx')

try:
    ###############################################################
    ####################   MAP visualization ######################
    ###############################################################
    st.subheader('Tabel visualization of number of classes')

    all_columns = file.columns.to_list()

    reserved = ['Unnamed: 0', 'resultId', 'locationId', 'latitude', 'longitude', 'ouputMeshGrid', 'outputMeshGrid', 'parentLocationId', 'scenario', 'year', 'r_value']

    variables = list(set(all_columns) - set(reserved))
    var_ID_all = [var[0:2] for var in variables]
    var_ID = list(np.unique(var_ID_all))

    variable_group = st.radio('Select variable group',var_ID)

    variables_selected = [var for var in variables if var[0:2]==variable_group]

    # Cleaning variables from keywords
    key_words = ['_HAZARD']

    variables_cleaned_one = []
    for var in variables_selected:
        for kw in key_words:
            if kw in var:
                variables_cleaned_one.append(var.replace(kw, ""))

    variables_cleaned_one = list(np.unique(variables_cleaned_one))        

    key_words = ['_mean','_upper','_lower']
    variables_cleaned = []
    for var in variables_cleaned_one:
        for kw in key_words:
            if kw in var:
                variables_cleaned.append(var.replace(kw, ""))

    for scen in ['ssp126','ssp245','ssp585']:

        risks = []
        nrisks = []
        vari = []
        st.subheader(scen)

        for var in list(np.unique(variables_cleaned)):

            
            fil = file.where(file['scenario']==scen)
            risk = fil[var + '_mean_HAZARD'].dropna().to_list()
            risks.append(np.unique(risk))
            nrisks.append(len(np.unique(risk)))
            vari.append(var)


        table = pd.DataFrame()

        table['Variable'] = vari
        table['Risks'] = risks
        table['#Risks'] = nrisks


        st.table(table)
    
except:
    st.write('Load the file')