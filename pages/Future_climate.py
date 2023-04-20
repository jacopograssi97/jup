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


st.set_page_config(page_title="Future climate", page_icon="📈")

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
    st.subheader('Climatology on monthly mean values')

    st.write('WORK IN PROGRESS')
    st.write('Soon available')


    
except:
    st.write('Load the file')