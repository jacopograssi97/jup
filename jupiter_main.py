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


st.header('Dashboard for Jupiter Intelligence data analysis - v 1.0')



st.markdown('Author: jacopo.grassi@wsp.com')
st.divider()




st.subheader('Updates - v 1.0')
st.subheader('Major release')
with st.expander('Show updates'):
        st.text('-Bug fixed \n-Section Future Climate added')
        st.text('-Please note that this section will need the file _CLIMATE.xlsx')

st.divider()


st.subheader('Updates - v 0.2')
with st.expander('Show updates'):
        st.text('-Bug fixed \n-Section Spatial metrics added')

st.divider()

st.subheader('Updates - v 0.1')
with st.expander('Show updates'):
        st.text('-Bug fixed \n-Dashed and dotted lines added for lower and upper limits in Time series \n-Tables simplified in Time series')