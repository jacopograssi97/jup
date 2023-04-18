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


st.header('Dashboard for Jupiter Intelligence data analysis - v 0.2')


st.subheader('Updates - v 0.2')
st.text('-Bug fixed \n-Section Spatial metrics added')

st.divider()

st.subheader('Updates - v 0.1')
st.text('-Bug fixed \n-Dashed and dotted lines added for lower and upper limits in Time series \n-Tables simplified in Time series')

