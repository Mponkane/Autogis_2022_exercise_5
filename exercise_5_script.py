import geopandas as gpd
import pandas as pd
from pyproj import CRS
import numpy as np
import mapclassify
import matplotlib.pyplot as plt
from IPython.display import display

""" 
When I was trialing out r5r as an aggregation method for my master's thesis I made a test 
for the area of Oulu municipality. For my test I made cumulative opportunity metrics of access from 
a ttm aggregated on a hexagonial grid that I tessallated for the area. I decided to look at cycling accessibility of 
pizza places imported from a google maps KML file. I made some maps from these calculations using ArcGIS, 
but I wanted to see what would the workflow be when I would create such maps using the relevant modules and methods 
we have looked at on this course using Python
"""

# Reading an aggrageted cumulative cycling accessibility (30 min) metrics done on r5r
grid = gpd.read_file("shapes/accessible_pizzerias_30min_oulu.shp")
grid.to_crs(epsg=3879,inplace=True)
grid.drop(labels=(["Jon_Cnt","Shp_Lng","Shap_Ar","lon","lat"]),axis=1,inplace=True)
grid.replace(0.,np.nan, inplace=True)
grid.dropna(inplace=True)

# Reading a Oulu and Kempele municipality borders
borders = gpd.read_file("shapes/Oulu_borders.shp")
borders.to_crs(epsg=3879,inplace=True)

# Reading an OSM street newtwork restricted to Oulu/Kempele area
osm_streets = gpd.read_file("shapes/osm_network.shp")
osm_streets.to_crs(epsg=3879,inplace=True)

# Reading ocean polygon for visualization
ocean = gpd.read_file("shapes/meri10.shp")
ocean.to_crs(epsg=3879,inplace=True)

# Restricting the figure boundary to the hex grid geometry
minx, miny, maxx, maxy = grid.geometry.total_bounds

#Classifier
classifier = mapclassify.UserDefined.make(bins=[5, 10, 15, 20, 25, 30, 35, 40])

# Plotting
output_fig = "number_of_accessible_pizzaplaces.png"
fig, axes = plt.subplots(figsize=(25,22))
borders.plot(ax=axes,color="#f7fcf9")
hexplot = grid.plot(ax=axes,cmap="YlOrRd",column="accssbl", antialiased=False,legend=True,legend_kwds={'shrink': 0.5})
figureleg = hexplot.figure
legend = figureleg.axes[1]
legend.tick_params(labelsize=22)
ocean.plot(ax=axes, color="#b5b5b5",edgecolor="#1f1f1f",linewidth = 0.5)
osm_streets.plot(ax=axes, color="black",linewidth = 0.2)
axes.set_xlim(minx - .1, maxx + .1)
axes.set_ylim(miny - .1, maxy + .1)
axes.set_title("Numer of accessible pizzerias in 30 minutes with cycling", fontsize = 26)
axes.ticklabel_format(style='plain')
plt.tight_layout()
plt.show()
fig.savefig(fname=output_fig)




# output_fig3 = "shopping_center_accessibility.png"



# fd = ["data/TravelTimes_to_5902043_Myyrmanni.txt", "data/TravelTimes_to_5944003_Itis.txt"]
# shopping_centers = ["Myyrmanni", "Itis"]
# mode = ["PT","Car"]
# mode_data_names = ["pt_r_t_cl", "car_r_t_cl"]
# cols = ["pt_r_t", "car_r_t", "from_id", "to_id"]
# fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10,5), )
# for i in range(len(fd)):
#     for j in range(len(fd)):
#         data = pd.read_csv(fd[i], usecols=cols, sep=";")
#         data_geo = data.merge(data, how="inner", left_on="YKR_ID", right_on="from_id")
#         data_geo.replace(-1.,np.nan, inplace=True)
#         data_geo.dropna(inplace=True)
#         classifier = mapclassify.UserDefined.make(bins=[5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60])
#         data_geo[["pt_r_t_cl", "car_r_t_cl"]]= data_geo[["pt_r_t", "car_r_t"]].apply(classifier)
#         axes[i][j].ticklabel_format(style='plain')
#         axes[i][j].tick_params(labelsize=6.5)
#         axes[i][j].set_title("{}- Classified travel times by {}".format(shopping_centers[i],mode[j]))
#         data_geo.plot(column="{}".format(mode_data_names[j]), ax = axes[i][j], linewidth=0, legend=True,legend_kwds={'shrink': 0.5}, antialiased=False)
# plt.tight_layout()


# fig.savefig(fname=output_fig3)
