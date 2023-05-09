import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import plotly.express as px
import plotly.graph_objects as go

# using the style for the plot
plt.style.use('seaborn-v0_8-darkgrid')

font = {'family' : 'Arial',
        'weight' : 'normal',
        'size'   : 12}

matplotlib.rc('font', **font)


st.set_page_config(page_title="Time series", page_icon="📈", layout="wide")

st.info('Some anomalous arrests have been reported due to technical problems. Pease contact the author if anything strange happens.', icon='⚠️')

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


st.subheader('Time series visualization')
st.markdown('In this section it is possible to analyze the time evolution of a selected metric. Please note that in this section you have to load a _PROCESSED file.')

if uploaded_file_data == None:
    st.warning(f'Please upload a file', icon="🚨")
    st.stop()

if '_PROCESSED' not in uploaded_file_data.name:
    st.error(f'The file you uploaded is: {uploaded_file_data.name}. Please note that this section needs a _PROCESSED file.', icon="🚨")
    st.stop()

if '_PROCESSED' in uploaded_file_data.name:
    st.success(f'The file you uploaded is: {uploaded_file_data.name}.')

# Taking all the columns from the file
all_columns = file.columns.to_list()

# Some columns 
reserved = ['Unnamed: 0', 'resultId', 'locationId', 'latitude', 'longitude', 'ouputMeshGrid', 'outputMeshGrid', 'parentLocationId', 'scenario', 'year', 'r_value']
variables = list(set(all_columns) - set(reserved))
var_ID_all = [var[0:2] for var in variables]
var_ID = list(np.unique(var_ID_all))

col1, col2= st.columns([1, 2])
with col1:
    variable_group = st.radio('Select variable group',var_ID)

variables_selected = [var for var in variables if var[0:2]==variable_group]

# Cleaning variables from keywords
key_words = ['_HAZARD']

variables_cleaned_one = []
for var in variables_selected:
    for kw in key_words:
        if kw in var:
            variables_cleaned_one.append(var.replace(kw, ""))
        else:
            variables_cleaned_one.append(var)

variables_cleaned_one = list(np.unique(variables_cleaned_one))        

key_words = ['_mean','_upper','_lower']
variables_cleaned = []
for var in variables_cleaned_one:
    for kw in key_words:
        if kw in var:
            variables_cleaned.append(var.replace(kw, ""))

fig,ax = plt.subplots(1,1, figsize=(6,4), dpi=600)
fig_iter = go.Figure()

# Scenarios with their colors
scenarios = ['ssp126','ssp245','ssp585']
colors = ['green','orange','red']

variables_to_plot = []

with col1:

    var_to_plot = st.selectbox('Variable to plot',list(np.unique(variables_cleaned)))
    time_ext = list(st.slider('Time domain', 2019, 2101, (2019, 2101)))


# Finding all the metrics associated with that variable (low, man, up)
for var in variables:
    if var_to_plot in var:
        if '_HAZARD' not in var:
            variables_to_plot.append(var)

# Plotting variable
for var in variables_to_plot:

    for scen, color,scen_nm in zip(scenarios,colors,['SSP1-2.6','SSP2-4.5','SSP5-8.5']):
        by_scenario = file.groupby('scenario').get_group(scen)
        by_scenario_mod = by_scenario.where(by_scenario['year'] <= time_ext[1] ).dropna()
        by_scenario_mod = by_scenario_mod.where(by_scenario_mod['year'] >= time_ext[0] ).dropna()

        if 'upper' in var:
            ax.plot(by_scenario_mod.year, by_scenario_mod[var], '--', c=color)
            fig_iter.add_trace(go.Scatter(x=by_scenario_mod.year, y=by_scenario_mod[var],
                    mode='lines', line=dict(color=color, width=4, dash='dash'),
                    name=f'{scen} upper'))
        
        elif 'lower' in var:
            ax.plot(by_scenario_mod.year, by_scenario_mod[var], linestyle='dotted', c=color, lw=4)
            fig_iter.add_trace(go.Scatter(x=by_scenario_mod.year, y=by_scenario_mod[var],
                    mode='lines', line=dict(color=color, width=4, dash='dot'),
                    name=f'{scen} lower'))
        
        else:
            ax.plot(by_scenario_mod.year, by_scenario_mod[var], c=color, label = scen_nm, lw=2)
            fig_iter.add_trace(go.Scatter(x=by_scenario_mod.year, y=by_scenario_mod[var],
                    mode='lines', line=dict(color=color, width=4),
                    name=f'{scen} lower'))

ax.plot([], [], ':', c='w', label=" ")
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


bands = file_thresholds.where(file_thresholds.Metric == var_to_band).dropna()

for index, band in bands.iterrows():

    ax.axhline(y = band['Min Value'], color = 'k', linestyle = '--', alpha=0.6)
    plt.text(time_ext[0] + 5, band['Min Value'], band['Tier'], fontsize=9)

    fig_iter.add_trace(go.Scatter(x=by_scenario_mod.year, y=np.squeeze(np.ones((len(by_scenario_mod.year),1))*band['Min Value']),
            mode='lines', line=dict(color='grey', width=2, dash='dashdot'),
            name=band['Tier']))

    fig_iter.add_annotation(dict(font=dict(color='grey',size=9),
                                    x=time_ext[0] + 5,
                                    y=band['Min Value'],
                                    showarrow=False,
                                    text=band['Tier'],
                                    textangle=0,
                                    xanchor='left',
                                    xref="paper",
                                    yref="paper"))
            
with col1:
    title = st.text_input('Chart title', var_to_plot)
    ylabel = st.text_input('Y label', 'value')

ax.set_xlabel('year')
ax.set_ylabel(ylabel)
ax.set_title(title)


handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1.1, 0.5), frameon=False)


tbl = pd.DataFrame()
for var in variables_to_plot:

    for scen, color,scen_nm in zip(scenarios,colors,['SSP1-2.6','SSP2-4.5','SSP5-8.5']):
        by_scenario = file.groupby('scenario').get_group(scen)
        by_scenario_mod = by_scenario.where(by_scenario['year'] < time_ext[1] ).dropna()
        by_scenario_mod = by_scenario_mod.where(by_scenario_mod['year'] > time_ext[0]).dropna()
        tbl[f'{scen} {var}'] = by_scenario_mod[var].to_numpy()
    
        tbl['year'] = by_scenario_mod.year.to_numpy().astype(int)

tbl = tbl.set_index('year')




with col2:
    tab1, tab2, tab3= st.tabs(["Final plot", "Interactive plot", "Tabular data"])
    with tab1:
        st.pyplot(fig)
    
    with tab2:
        st.plotly_chart(fig_iter, theme="streamlit")
    
    with tab3:
        bd = st.selectbox('Band',['mean','lower','upper'])
        cl = tbl.columns.to_list()

        col_to_tbl = []
        for c in cl:
            if bd in c:
                col_to_tbl.append(c)
        st.table(tbl[col_to_tbl])


