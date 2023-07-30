# Seqana_assignement - Amirtha varshini

 30/07/2023

 I have used QGIS to execute the tasks. Please change the file paths according your files. 

 # Task 1  - visualization

 1. Download the file
 2. Unzip the file
 3. open the Submission. qgz
 4. Right-click on the points _data geopackage -> click 'zoom to layer'<img width="1440" alt="Screenshot 2023-07-30 at 05 14 58" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/b4650b59-2298-44f2-9e74-543e213cc2a1">

 5. Check one layer and uncheck other layers to visualize each tiff file.
 6. Click layout to add images together as a map visualization

    
Result of Map Layout


<img width="1440" alt="Screenshot 2023-07-30 at 05 15 57" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/335e9ead-2623-42e4-96e9-24c325a964b2">

    
# Tasks for phase 2

1. Click on vectors -> Analysis Tools -> Basic Statistics fields
   <img width="1440" alt="Screenshot 2023-07-30 at 05 08 45" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/9d011322-8050-4147-82c4-d6e187807261">

   
2. Click the field that contains the SOC field from the data file
   <img width="1440" alt="Screenshot 2023-07-30 at 05 10 26" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/8996b04d-d73d-47ef-bfae-10b620713f12">

   
<img width="1440" alt="Screenshot 2023-07-30 at 05 10 34" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/939a0a69-d301-41dd-b326-e4b722023ba9">

3. Click run 

<img width="1440" alt="Screenshot 2023-07-30 at 05 10 43" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/73afd5ed-8c0c-43fb-899a-8ece38985395">

4. To visualize the histogram for each tiff file, right click on the file and go to the Histogram. 
<img width="1440" alt="Screenshot 2023-07-30 at 05 39 22" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/eb80d58f-e47d-43b5-b2a2-cff670fc6551">



# Tasks for phase 3

Covariate files

1.  open_land_map_soil_ph.tif - https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_PH-H2O_USDA-4C1A2A_M_v02
2.  open_land_map_soil_clay.tif -  https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_CLAY-WFRACTION_USDA-3A1A1A_M_v02
3.  modis_annual_npp_2009.tif - https://developers.google.com/earth-engine/datasets/catalog/UMT_NTSG_v2_MODIS_NPP
4.  landsat7_c01_t1_annual_ndvi_2009.tif - https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_ANNUAL_NDVI
5.  CGIAR_SRTM90_V4.tif - https://developers.google.com/earth-engine/datasets/catalog/CGIAR_SRTM90_V4




# Tasks for phase 4

1. Click Plugin -> open the python Plugin<img width="1440" alt="Screenshot 2023-07-30 at 05 25 41" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/85359298-8aff-461b-958d-1776cc8cadbe">

2. click on the show editor <img width="1440" alt="Screenshot 2023-07-30 at 05 28 09" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/39e8b360-f731-461c-b903-2957cd3451eb">

3. copy paste this code in the code editor and run it
   
``` python
import geopandas as gpd
import rasterio
from rasterio.features import rasterize
import numpy as np

# Load the sampling points from the Geopackage file
points_gpkg_file = '/Users/amirthavarshini/Downloads/intern_tasks/seqana_gis_solutions_engineering_working_student_challenge_data 2/seqana_gis_solutions_eng_challenge_existing_sample_data.gpkg'

points_gdf = gpd.read_file(points_gpkg_file)

# Load the covariates from the TIFF files
#!!!! change the location according to your file path
covariate_files = [
    '/Users/amirthavarshini/Downloads/intern_tasks/seqana_gis_solutions_engineering_working_student_challenge_data 2/covariates/open_land_map_soil_ph.tif',
    '/Users/amirthavarshini/Downloads/intern_tasks/seqana_gis_solutions_engineering_working_student_challenge_data 2/covariates/open_land_map_soil_clay.tif',
    '/Users/amirthavarshini/Downloads/intern_tasks/seqana_gis_solutions_engineering_working_student_challenge_data 2/covariates/modis_annual_npp_2009.tif',
    '/Users/amirthavarshini/Downloads/intern_tasks/seqana_gis_solutions_engineering_working_student_challenge_data 2/covariates/landsat7_c01_t1_annual_ndvi_2009.tif',
    '/Users/amirthavarshini/Downloads/intern_tasks/seqana_gis_solutions_engineering_working_student_challenge_data 2/covariates/CGIAR_SRTM90_V4.tif'
    # Add paths to other covariate TIFF files as needed
]


covariates = [rasterio.open(file) for file in covariate_files]

# Step 3: Extract the covariate values at the sampling point locations
def extract_covariate_values(point, covariate):
    row, col = covariate.index(point['geometry'].x, point['geometry'].y)
    return covariate.read(1)[row, col]

covariate_names = []
for i, covariate in enumerate(covariates):
    covariate_name = f'covariate_{i+1}'
    covariate_names.append(covariate_name)
    points_gdf[covariate_name] = points_gdf.apply(lambda x: extract_covariate_values(x, covariate), axis=1)

# Step 4: Calculate the correlation between each covariate and the SOC stocks
# Assuming you have a column named 'SOC_stocks' in the points_gdf containing the SOC stock values

correlation_results = {}
for covariate_name in covariate_names:
    correlation = np.corrcoef(points_gdf['soc_stock_t_ha'], points_gdf[covariate_name])[0, 1]
    correlation_results[covariate_name] = correlation

print(correlation_results)
```
5. Run the code and see the ouput
<img width="1440" alt="Screenshot 2023-07-30 at 05 28 38" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/06dc2038-a0fd-4dff-a5ea-05103c9f8ac8">


# Task 5 

The main objective of monitoring is to quantify the stock change of SOC and emissions of CO2, CH4
and N2O resulting from the project scenario during the verification period. 

1. Mathematical edge: To start with, I would start with the co-variate that is the most positively correlated with SOC. ' landsat7_c01_t1_annual_ndvi_2009.tif' has the highest positive correlation. 
Then consider 'open_land_map_soil_clay.tif'. The others are negatively correlated with SOC

2.  Relevance to Research Question: NDVI is directly related to SOC. Healthier and more productive vegetation often leads to increased carbon sequestration in the soil, resulting in higher SOC levels. The higher the content of clay in the soil, the higher the Soil Organic Carbon (SOC) content is likely to be.

3.  Unique variations: Even though 'modis_annual_npp_2009.tif ' is negatively correlated, this covariate exhibits substantial spatial variation within the AOI and is likely to be a key driver of SOC stocks' distribution, it can be a strong candidate for stratification.


# The End
Thank you for the opportunity 
