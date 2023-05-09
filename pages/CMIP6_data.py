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


st.set_page_config(page_title="CMIP6 data", page_icon="📈", layout="wide")

st.info('Some anomalous arrests have been reported due to technical problems. Pease contact the author if anything strange happens.', icon='⚠️')

###############################################################
#######################   DATA LOADER #########################
###############################################################
# Importing file with the data
uploaded_file_data = st.file_uploader('DATA FILE ')
file = uploaded_file_data
# try:
#     file=pd.read_excel(uploaded_file_data)

# except:
#     try:
#             file=pd.read_excel(uploaded_file_data)
#     except:      
#             pass


file_thresholds = pd.read_excel('Table Formatted RANGES.xlsx')
###############################################################
####################   MAP visualization ######################
###############################################################


st.markdown('In this section it is possible to analyze the time evolution of a selected metric. Please note that in this section you have to load a _stats file.')

if uploaded_file_data == None:
    st.warning(f'Please upload a file', icon="🚨")
    st.stop()

if '_stats' not in uploaded_file_data.name:
    st.error(f'The file you uploaded is: {uploaded_file_data.name}. Please note that this section needs a _stats file.', icon="🚨")
    st.stop()

if '_stats' in uploaded_file_data.name:
    st.success(f'The file you uploaded is: {uploaded_file_data.name}.')


variable = st.selectbox('Select variable', ['tas','pr'])



fig,ax = plt.subplots(1,1, figsize=(6,4), dpi=600)
fig_iter = go.Figure()
fig_anomaly = go.Figure()


colors = ['green','orange','red']
scenarios = ['ssp126','ssp245','ssp585']
scenarios_name = ['SSP1-2.6','SSP2-4.5','SSP5-8.5']
vars = ['tas','tasmin','tasmax']
operations = ['mean','min','max']
titles = ['Daily mean temperature','Daily min temperature','Daily max temperature']



for var,tit,op in zip(vars,titles,operations):

    fig, ax = plt.subplots(1,1, figsize=(8,4))

    tab = pd.read_excel(file, sheet_name='ssp126')
    tab = tab.where(tab.Date.dt.year<2015).dropna()

    if variable == 'tas':
        fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab.Avg.rolling(window=5).mean()- 273.15,
                        mode='lines', line=dict(color='blue', width=4),
                        name=f'Baseline'))
        
        fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['95th_perc'].rolling(window=5).mean() - 273.15,
                        mode='lines', line=dict(color='Blue', width=4, dash='dash'),
                        name=f'Baseline upper'))

        fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['5th_perc'].rolling(window=5).mean() - 273.15,
                        mode='lines', line=dict(color='Blue', width=4, dash='dot'),
                        name=f'Baseline lower'))

        for scen, col, name in zip(scenarios, colors, scenarios_name):
            tab = pd.read_excel(file, sheet_name=scen)

            tab = tab.where(tab.Date.dt.year>2010).dropna()


            fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab.Avg.rolling(window=5).mean() -273.15,
                        mode='lines', line=dict(color=col, width=4),
                        name=f'{scen} upper'))
            
            fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['95th_perc'].rolling(window=5).mean() -273.15,
                        mode='lines', line=dict(color=col, width=4, dash='dash'),
                        name=f'{scen} upper'))

            fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['5th_perc'].rolling(window=5).mean() -273.15,
                        mode='lines', line=dict(color=col, width=4, dash='dot'),
                        name=f'{scen} upper'))

    
    if variable == 'pr':

        fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab.Avg.rolling(window=5).mean() * 86400 * 365,
                        mode='lines', line=dict(color='blue', width=4),
                        name=f'Baseline'))
        
        fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['95th_perc'].rolling(window=5).mean() * 86400 * 365,
                        mode='lines', line=dict(color='Blue', width=4, dash='dash'),
                        name=f'Baseline upper'))

        fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['5th_perc'].rolling(window=5).mean() * 86400 * 365,
                        mode='lines', line=dict(color='Blue', width=4, dash='dot'),
                        name=f'Baseline lower'))

        for scen, col, name in zip(scenarios, colors, scenarios_name):
            tab = pd.read_excel(file, sheet_name=scen)

            tab = tab.where(tab.Date.dt.year>2010).dropna()


            fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab.Avg.rolling(window=5).mean()  * 86400 * 365,
                        mode='lines', line=dict(color=col, width=4),
                        name=f'{scen} upper'))
            
            fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['95th_perc'].rolling(window=5).mean()  * 86400 * 365,
                        mode='lines', line=dict(color=col, width=4, dash='dash'),
                        name=f'{scen} upper'))

            fig_iter.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['5th_perc'].rolling(window=5).mean() * 86400 * 365,
                        mode='lines', line=dict(color=col, width=4, dash='dot'),
                        name=f'{scen} upper'))




for var,tit,op in zip(vars,titles,operations):

    fig, ax = plt.subplots(1,1, figsize=(8,4))

    tab = pd.read_excel(file, sheet_name='ssp126')
    tab = tab.where(tab.Date.dt.year<2015).dropna()
    baseline = tab.Avg.mean() 

    print(op)

    for scen, col, name in zip(scenarios, colors, scenarios_name):
        tab = pd.read_excel(file, sheet_name=scen)

        tab = tab.where(tab.Date.dt.year>2010).dropna()

        if variable == 'tas':


            fig_anomaly.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab.Avg.rolling(window=5).mean() - baseline,
                        mode='lines', line=dict(color=col, width=4),
                        name=f'{scen} upper'))
            
            fig_anomaly.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['95th_perc'].rolling(window=5).mean() - baseline,
                        mode='lines', line=dict(color=col, width=4, dash='dash'),
                        name=f'{scen} upper'))

            fig_anomaly.add_trace(go.Scatter(x=tab.Date.dt.year, y=tab['5th_perc'].rolling(window=5).mean() - baseline,
                        mode='lines', line=dict(color=col, width=4, dash='dot'),
                        name=f'{scen} upper'))
        
        if variable == 'pr':

            fig_anomaly.add_trace(go.Scatter(x=tab.Date.dt.year, y=(tab.Avg.rolling(window=5).mean() - baseline)  * 86400 * 365,
                        mode='lines', line=dict(color=col, width=4),
                        name=f'{scen} upper'))
            
            fig_anomaly.add_trace(go.Scatter(x=tab.Date.dt.year, y=(tab['95th_perc'].rolling(window=5).mean() - baseline)  * 86400 * 365,
                        mode='lines', line=dict(color=col, width=4, dash='dash'),
                        name=f'{scen} upper'))

            fig_anomaly.add_trace(go.Scatter(x=tab.Date.dt.year, y=(tab['5th_perc'].rolling(window=5).mean() - baseline)  * 86400 * 365,
                        mode='lines', line=dict(color=col, width=4, dash='dot'),
                        name=f'{scen} upper'))

        


    ax.plot([],[],'-',c='w', label=' ')
    ax.plot([],[],'-',c='k', label='Mean', lw=3)
    ax.plot([],[],'--',c='k', label='95th perc', lw=2)
    ax.plot([],[],':',c='k', label='5th perc', lw=2)

    ax.grid()
    ax.legend(frameon=False, loc='upper right', bbox_to_anchor=(1.3,1))
    ax.set_title(f'{tit} anomaly')
    ax.set_ylabel('T [°C]')
    ax.set_xlabel('Year')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)




tab1, tab2 = st.tabs(['Plots', 'Tables'])

with tab1:
    col1, col2= st.columns([1, 1])

    with col1:

        st.subheader('Plot')
        st.plotly_chart(fig_iter, theme="streamlit")
        
    with col2:
        st.subheader('Anomaly plot')
        st.plotly_chart(fig_anomaly, theme="streamlit")

with tab2:
    

    yr = [[2000,2020],[2030,2040],[2050,2060],[2080,2100]]
    periods = ['Baseline','Short range','Medium range', 'Long range']

    s = st.selectbox('Scenario',['ssp126','ssp245','ssp585'])
    tab = pd.read_excel(file, sheet_name=s)


    final_table = []
    anomaly_table = []
    percentage = []
    for year, per in zip(yr,periods):

        tb = tab.where(tab.Date.dt.year>year[0])
        tb = tb.where(tb.Date.dt.year<year[1]).dropna().set_index('Date')

        if variable == 'pr':
            tb = tb * 86400 * 365
        
        if variable == 'tas':
            tb = tb - 273.15

        if year == [2000,2020]:
            baseline = tb.mean()

        # st.write(f'{per} - {year}')
        # st.table(tb.mean())
        # st.table(tb.mean() - baseline)

        final_table.append(tb.mean())
        anomaly_table.append(tb.mean() - baseline)
        percentage.append((100/baseline) * (tb.mean() - baseline))

    final_table = pd.concat(final_table, axis=1, ignore_index=True).set_axis(periods, axis=1, inplace=False)
    anomaly_table = pd.concat(anomaly_table, axis=1, ignore_index=True).set_axis(periods, axis=1, inplace=False)
    percentage = pd.concat(percentage, axis=1, ignore_index=True).set_axis(periods, axis=1, inplace=False)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader('Values')
        st.write(final_table)

    with col2:
        st.subheader('Anomaly')
        st.write(anomaly_table)

    with col3:
        st.subheader('Percentage')
        st.write(percentage)




