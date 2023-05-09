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

st.info('Some anomalous arrests have been reported due to technical problems. Pease contact the author if anything strange happens.', icon='⚠️')


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
    st.subheader('Map visualization of the grid points present in the files')

    try:
        locations = file[['locationId','latitude', 'longitude']]
        loc_unique = locations.drop_duplicates(subset=['locationId'])
        grid_points = loc_unique[['latitude', 'longitude']]

        latitude = grid_points['latitude'].to_list()
        longitude = grid_points['longitude'].to_list()

        lat_corr = []
        lon_corr = []

        for lat, lon in zip(latitude, longitude):
            n = 2
            lat_corr.append(float(lat) / (10 ** (len(str(lat))-n)))
            lon_corr.append(float(lon) / (10 ** (len(str(lon))-n)))

        grid_points_new = pd.DataFrame()
        grid_points_new['latitude'] = lat_corr
        grid_points_new['longitude'] = lon_corr

    except:
        raise

    st.map(grid_points)


    ###############################################################
    ##################   OVERVIEW ON VARIABLES ####################
    ###############################################################
    st.subheader('Managing variables')

    all_columns = file.columns.to_list()
    st.write(all_columns)

    reserved = ['Unnamed: 0', 'resultId', 'locationId', 'latitude', 'longitude', 'ouputMeshGrid', 'outputMeshGrid', 'parentLocationId', 'scenario', 'year', 'r_value']
    variables = list(set(all_columns) - set(reserved))
    var_ID_all = [var[0:2] for var in variables]
    var_ID = list(np.unique(var_ID_all))

    variable_group = st.radio('Select variable group',var_ID)

    variables_selected = [var for var in variables if var[0:2]==variable_group]

    # Cleaning variables from keywords
    key_words = ['_mean','_upper','_lower','_HAZARD']

    variables_cleaned_one = []
    for var in variables_selected:
        for kw in key_words:
            if kw in var:
                variables_cleaned_one.append(var.replace(kw, ""))

    variables_cleaned = []
    for var in variables_cleaned_one:
        for kw in key_words:
            if kw in var:
                variables_cleaned.append(var.replace(kw, ""))

    st.write('Variables found \n', list(np.unique(variables_cleaned)))

    # Checking bands if some are missing
    forbidden_numb = np.arange(0,1000,1)
    not_present_band = []
    for variable_check in variables_cleaned:
        var_to_band_check = variable_check[3:]
        for num in forbidden_numb:

                if 'Pct' in var_to_band_check:
                    var_to_band_check = var_to_band_check

                elif str(num) in var_to_band_check:
                    var_to_band_check = var_to_band_check.replace(str(num), "*")

        if '**' in var_to_band_check:
            var_to_band_check = var_to_band_check.replace("**", "*")

        bands = file_thresholds.where(file_thresholds.Metric == var_to_band_check).dropna()

        if len(bands)==0:
            not_present_band.append(variable_check)

    st.write('The following variables do not have bands scheduled\n', not_present_band)

except:
    st.write('Load the file')