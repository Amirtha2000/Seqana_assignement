# Seqana_assignment: Amirtha varshini

 30/07/2023

 I have used QGIS to execute the tasks. Please change the file paths according to your files. 

 # Task 1: Visualization

 1. Download the file
 2. Unzip the file
 3. open the Submission. qgz
 4. Right-click on the points _data geopackage -> click 'zoom to layer'<img width="1440" alt="Screenshot 2023-07-30 at 05 14 58" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/bbe70987-de3c-47f9-a172-c4adc9116bed">


 5. Check one layer and uncheck other layers to visualize each tiff file.
 6. Click layout to add images together as a map visualization

    
Result of Map Layout

<img width="1440" alt="Screenshot 2023-07-30 at 05 15 57" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/4a894797-f92a-4d9d-8830-980525f8b03d">

    
# Tasks for phase 2

1. Click on vectors -> Analysis Tools -> Basic Statistics fields
   <img width="1440" alt="Screenshot 2023-07-30 at 05 08 45" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/0d679ce8-0626-4123-a576-550e1f1d05a8">

   
2. Click the field that contains the SOC field from the data file
   <img width="1440" alt="Screenshot 2023-07-30 at 05 10 26" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/1b84d978-8989-4511-8f03-ac54ba64dbdd">

   <img width="1440" alt="Screenshot 2023-07-30 at 05 10 34" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/a00e7fb4-021e-4d01-bc0d-fca5ca3cc3e2">

3. Click run 
<img width="1440" alt="Screenshot 2023-07-30 at 05 10 43" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/dc616f25-c7a1-485d-a235-8f271b8df509">


4. To visualize the histogram for each tiff file, right-click on the file and go to the Histogram. 
<img width="1440" alt="Screenshot 2023-07-30 at 05 39 22" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/8c11d536-fe04-4334-8009-6072ca315f3b">



# Tasks for phase 3

Covariate files

1.  open_land_map_soil_ph.tif - https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_PH-H2O_USDA-4C1A2A_M_v02
2.  open_land_map_soil_clay.tif -  https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_CLAY-WFRACTION_USDA-3A1A1A_M_v02
3.  modis_annual_npp_2009.tif - https://developers.google.com/earth-engine/datasets/catalog/UMT_NTSG_v2_MODIS_NPP
4.  landsat7_c01_t1_annual_ndvi_2009.tif - https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LE07_C01_T1_ANNUAL_NDVI
5.  CGIAR_SRTM90_V4.tif - https://developers.google.com/earth-engine/datasets/catalog/CGIAR_SRTM90_V4




# Tasks for phase 4

1. Click Plugin -> open the python Plugin<img width="1440" alt="Screenshot 2023-07-30 at 05 25 41" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/5d3193e5-50b3-47e6-8a3d-f101102c6e3d">

2. click on the Show editor 
<img width="1440" alt="Screenshot 2023-07-30 at 05 28 09" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/f3188d3f-464a-4bf5-94e0-6a45c0281a09">

3. copy and paste this code into the code editor and run it with your specific file paths
   
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
5. Run the code and see the output
<img width="1440" alt="Screenshot 2023-07-30 at 05 28 38" src="https://github.com/Amirtha2000/Seqana_assignement/assets/53963107/b678d4d8-b08b-4543-8703-b1b26b19700c">


# Task 5 

The main objective of monitoring is to quantify the stock change of SOC and emissions of CO2, CH4
and N2O resulting from the project scenario during the verification period. 

1. Mathematical edge: To start with, I would start with the co-variate that is the most positively correlated with SOC. ' landsat7_c01_t1_annual_ndvi_2009.tif' has the highest positive correlation. 
Then consider 'open_land_map_soil_clay.tif'. The others are negatively correlated with SOC

2. Relevance to Research Question: NDVI is directly related to SOC. Healthier and more productive vegetation often leads to increased carbon sequestration in the soil, resulting in higher SOC levels. The higher the content of clay in the soil, the higher the Soil Organic Carbon (SOC) content is likely to be.

3. Unique variations: Even though 'modis_annual_npp_2009.tif ' is negatively correlated, this covariate exhibits substantial spatial variation within the AOI and is likely to be a key driver of SOC stocks' distribution, making it a strong candidate for stratification.

Is there sufficient supporting data to stratify the AOI and assign sampling points? 

I think adding some more covariates that might be affecting the topsoil of the SOC could drastically improve the precision of the stratification process. After assessing the usefulness of each covariate, we can proceed with stratification by grouping similar areas together based on combinations of these covariates. The stratified areas can then serve as sampling strata, and we can assign sampling points within each stratum for further data collection or analysis. The goal is to ensure that each stratum represents a distinct portion of the AOI in terms of the selected covariates, thus enhancing the efficiency and accuracy of your subsequent analyses.

But the effectiveness of stratification will ultimately be determined by the quality and relevance of the selected covariates and the thoroughness of the data analysis process. 
# The End
Thank you for the opportunity 
