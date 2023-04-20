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


st.set_page_config(page_title="Future climate", page_icon="📈")

def save_img(fig):
    fig.savefig('prova.png', dpi=600, bbox_inches='tight')

mth = ['Jan','Feb','Mar','Apr','May','Jun','Jul', 'Aug','Sep','Oct','Nov','Dec']
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
    st.subheader('Climatology on monthly mean values')

    fig,ax = plt.subplots(1,1, figsize=(7,4), dpi=100)

    columns = file.columns.to_list()

    variable = st.radio('Select variable', ['Precipitation', 'Temperature'])

    st.subheader('Seasonal Cycles')

    aggregation = st.radio('Select Aggregation', ['Reference periods', 'Years'])

    file=pd.read_excel(uploaded_file_data, sheet_name='Cycles')

    if variable == 'Precipitation':

        col = [c for c in columns if 'PR' in c]
        ylab = '[mm/month]'

    if variable == 'Temperature':

        col = [c for c in columns if 'HT' in c]
        ylab = '[°C]'
        
    col.append('years')    
    file_plot = file[col]
    variable_to_plot = file_plot.columns.to_list()


    scenarios = st.multiselect('Select scenario', ['ssp126','ssp245','ssp585'])
    bands = st.multiselect('Select band', ['lower', 'mean', 'upper'])
    colors_585 = ['orange', 'red', 'maroon']
    colors_126 = ['lime', 'olive', 'darkgreen']
    colors_245 = ['lightskyblue', 'royalblue', 'navy']

    for scen in scenarios:

        for band in bands:

            for c in col:

                if scen in c and band in c:

                    if scen == 'ssp126':
                        colors = colors_126

                    if scen == 'ssp585':
                        colors = colors_585

                    if scen == 'ssp245':
                        colors = colors_245

                    for periods,color in zip([[2020,2040],[2040,2060],[2080,2100]],colors):

                        file_plotti = file_plot.where(file_plot.years > periods[0])
                        file_plotti = file_plotti.where(file_plotti.years < periods[1]).dropna()
                        var = file_plotti[c].to_numpy().reshape((3,12)).mean(axis=0)

                        if band == 'lower':
                            ax.plot(mth, var, label=f'{periods[0]}-{periods[1]} {scen} {band}', lw=3, color = color, ls=':')

                        if band == 'mean':
                            ax.plot(mth, var, label=f'{periods[0]}-{periods[1]} {scen} {band}', lw=3, color = color, ls='-')

                        if band == 'upper':
                            ax.plot(mth, var, label=f'{periods[0]}-{periods[1]} {scen} {band}', lw=3, color = color, ls='--')

    
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)

    title = st.text_input('Chart title', '')
    ylabel = st.text_input('Y label', ylab)

    ax.set_xlabel('Month')
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    st.pyplot(fig)


    
except:
    raise
    st.write('Load the file')