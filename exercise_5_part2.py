import geopandas as gpd
import pandas as pd
from pyproj import CRS
import numpy as np
import mapclassify
import matplotlib.pyplot as plt
from IPython.display import display
import folium
from folium.plugins import HeatMap

#Making an interactive map
m = folium.Map(location=[65.00578330601479, 25.459831040804357],
               tiles = "cartodbpositron", zoom_start=10,
               control_scale=True)
points = gpd.read_file("shapes/Oulu_pizzerias.shp")
points.to_crs(epsg=4326,inplace=True)
points_gjson = folium.features.GeoJson(points, name = "Pizzerias",
                                       style_function=lambda x: {'color':'orange',
                                                                 'icon':'glyphicon-thumbs-up'},
                                       tooltip=folium.features.GeoJsonTooltip(fields=['Name'],
                                                                              labels=True,
                                                                              sticky=False)
                                       ).add_to(m)
points_gjson.data.get('features')
points_gjson.add_to(m)
grid = gpd.read_file("shapes/accessible_pizzerias_30min_oulu.shp")
grid.to_crs(epsg=3879,inplace=True)
grid.drop(labels=(["Jon_Cnt","Shp_Lng","Shap_Ar","lon","lat"]),axis=1,inplace=True)
grid.replace(0.,np.nan, inplace=True)
grid.dropna(inplace=True)
grid['geoid'] = grid.index.astype(str)

folium.Choropleth(geo_data = grid,
                  data = grid,
                  columns=['geoid','accssbl'],
                  key_on='feature.id',
                  fill_color='YlGnBu',
                  line_weight=0,
                  legend_name='Number of accessible pizzaplaces').add_to(m)

m.save("mypizzamap.html")
