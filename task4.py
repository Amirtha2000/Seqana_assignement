import geopandas as gpd
import rasterio
from rasterio.features import rasterize
import numpy as np

# Load the sampling points from the Geopackage file
points_gpkg_file = '/Users/amirthavarshini/Downloads/intern_tasks/seqana_gis_solutions_engineering_working_student_challenge_data 2/seqana_gis_solutions_eng_challenge_existing_sample_data.gpkg'

points_gdf = gpd.read_file(points_gpkg_file)

# Load the covariates from the TIFF files
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
