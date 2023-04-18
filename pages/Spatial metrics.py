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
        'size'   : 13}

matplotlib.rc('font', **font)


st.set_page_config(page_title="Spatial merics", page_icon="📈")

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

    # Scenarios with their colors
    scenarios = ['ssp126','ssp245','ssp585']
    colors = ['green','orange','red']


    years = file['year'].to_list()
    var_to_plot = st.selectbox('Variable to plot',list(np.unique(variables_cleaned)))
    band_to_plot = st.selectbox('Band to plot',list(np.unique(key_words)))
    scen_to_plot = st.selectbox('Scenario',list(np.unique(scenarios)))
    time_ext = st.multiselect('Years', np.arange(2020,2105,5))

    fig,ax = plt.subplots(1,1, figsize=(9,5), dpi=100)

    variables_to_plot = []

    


    # Finding all the metrics associated with that variable (low, man, up)
    for var in variables:
        if var_to_plot in var:
            if '_HAZARD' not in var:
                variables_to_plot.append(var)

    # Plotting variable
    for var in variables_to_plot:

        by_scenario_mod = file.groupby('scenario').get_group(scen_to_plot)
        colors = plt.cm.rainbow(np.linspace(0,1,len(time_ext)))

        for yr,i in zip(time_ext,range(len(time_ext))):

            by_yr = by_scenario_mod.where(by_scenario_mod['year']==yr).dropna()

            if band_to_plot in var:
                ax.plot(np.linspace(5,100,20), by_yr[var].to_list(), '-', label=int(yr), color=colors[i])
            
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
    

    bands = file_thresholds.where(file_thresholds.Metric == var_to_band).dropna()
    print(bands)
    for index, band in bands.iterrows():

        ax.axhline(y = band['Min Value'], color = 'k', linestyle = '--', alpha=0.6)
        plt.text(0, band['Min Value'], band['Tier'], fontsize=11)


    title = st.text_input('Chart title', var_to_plot)
    ylabel = st.text_input('Y label', 'value')

    ax.set_xlabel('Km')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(np.arange(5,105,5))


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

except:
    raise
    st.write('Load the file')
