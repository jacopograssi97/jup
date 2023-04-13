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


st.set_page_config(page_title="Time series", page_icon="📈")

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
###############################################################
####################   MAP visualization ######################
###############################################################

try:
    st.subheader('Time series visualization')

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


    var_to_plot = st.selectbox('Variable to plot',list(np.unique(variables_cleaned)))


    # # Scenarios with their colors
    scenarios = ['ssp126','ssp245','ssp585']
    colors = ['green','orange','red']




    fig,ax = plt.subplots(1,1, figsize=(6,4), dpi=600)

    variables_to_plot = []

    time_ext = list(st.slider('Time domain', 2020, 2100, (2021, 2099)))

    # Finding all the metrics associated with that variable (low, man, up)
    for var in variables:
        if var_to_plot in var:
            if '_HAZARD' not in var:
                variables_to_plot.append(var)

    # Plotting variable
    for var in variables_to_plot:

        for scen, color,scen_nm in zip(scenarios,colors,['SSP1-2.6','SSP2-4.5','SSP5-8.5']):
            by_scenario = file.groupby('scenario').get_group(scen)
            by_scenario_mod = by_scenario.where(by_scenario['year'] < time_ext[1] ).dropna()
            by_scenario_mod = by_scenario_mod.where(by_scenario_mod['year'] > time_ext[0] ).dropna()

            if 'upper' in var:
                ax.plot(by_scenario_mod.year, by_scenario_mod[var], '--', c=color)
            
            elif 'lower' in var:
                ax.plot(by_scenario_mod.year, by_scenario_mod[var], linestyle='dotted', c=color, lw=4)
            
            else:
                ax.plot(by_scenario_mod.year, by_scenario_mod[var], c=color, label = scen_nm, lw=2)
    
    ax.plot([], [], ':', c='k', label="Lower")
    ax.plot([], [], '-', c='k', label="Mean")
    ax.plot([], [], '--', c='k', label="Upper")


    forbidden_numb = np.arange(0,1000,1)
    var_to_band = var_to_plot[3:]


    for num in forbidden_numb:

            if 'Pct' in var_to_band:

                var_to_band = var_to_band

            elif str(num) in var_to_band:

                var_to_band = var_to_band.replace(str(num), "*")

    if '**' in var_to_band:
        var_to_band = var_to_band.replace("**", "*")

    if '**' in var_to_band:
        var_to_band = var_to_band.replace("**", "*")
    
    st.write(var_to_band)

    print(var_to_band)

    bands = file_thresholds.where(file_thresholds.Metric == var_to_band).dropna()
    print(bands)
    for index, band in bands.iterrows():

        ax.axhline(y = band['Min Value'], color = 'k', linestyle = '--', alpha=0.6)
        plt.text(time_ext[0] + 5, band['Min Value'], band['Tier'], fontsize=9)


    ax.set_xlabel('year')
    ax.set_ylabel('value')
    ax.set_title(var_to_plot)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1.1, 0.5), frameon=False)

    st.pyplot(fig)


    tbl = pd.DataFrame()
    for var in variables_to_plot:

        if 'mean' in var:

            for scen, color,scen_nm in zip(scenarios,colors,['SSP1-2.6','SSP2-4.5','SSP5-8.5']):
                by_scenario = file.groupby('scenario').get_group(scen)
                by_scenario_mod = by_scenario.where(by_scenario['year'] < time_ext[1] ).dropna()
                by_scenario_mod = by_scenario_mod.where(by_scenario_mod['year'] > time_ext[0]).dropna()
                tbl[f'{scen} {var}'] = by_scenario_mod[var].to_numpy()
            
                tbl['year'] = by_scenario_mod.year.to_numpy().astype(int)

    tbl = tbl.set_index('year')

    st.table(tbl)

except:
    st.write('Load the file')
