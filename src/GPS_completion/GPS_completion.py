import os
import pandas as pd
import numpy as np
from scipy import interpolate
import io
import sys
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets

import gpxpy
import geojson
import geopy.distance as gpd

def overlayGPX(gpxData, map):
    '''
    overlay a gpx route on top of an OSM map using Folium
    some portions of this function were adapted
    from this post: https://stackoverflow.com/questions/54455657/
    how-can-i-plot-a-map-using-latitude-and-longitude-data-in-python-highlight-few
    '''
    gpx_file = open(gpxData, 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
                folium.Marker([point.latitude,point.longitude], color="red", weight=2.5, opacity=1).add_to(map)
    return (map)


df = pd.read_excel(os.path.realpath('TrackSiteData_2020_clean.xlsx'), index_col=None)
rp = df['Relative Position'].to_numpy()
lat = df['Latitude'].to_numpy()
lon = df['Longitude'].to_numpy()

with open(os.path.realpath('export.geojson')) as f:
    gj = geojson.load(f)

# Keep only polyline
gj['features'] = [gj['features'][2]]
df2=pd.DataFrame()
for feat in gj['features']:
        if (feat['geometry']['type'] == 'Point'):
            None
            #df_new = pd.DataFrame([[feat['geometry']['coordinates'][0], feat['geometry']['coordinates'][1], 'geojson']],columns=['Latitude', 'Longitude', 'Element Type'])
            #df2 = pd.concat([df2,df_new])
        else:
            for coord in feat['geometry']['coordinates']:
                df_new = pd.DataFrame([[coord[0], coord[1], 'geojson']], columns=['Longitude', 'Latitude', 'Element Type'])
                df2 = pd.concat([df2, df_new])

#Find out what the closest points are
# minval = np.inf
# for idx in np.argwhere(np.isfinite(df['Latitude'].values)):
#     testdis = np.zeros(df2.values.shape[0])
#     testpos = (df['Latitude'].values[idx], df['Longitude'].values[idx])
#     for coord in range(0,df2.values.shape[0]):
#         pos = (df2['Latitude'].iloc[coord], df2['Longitude'].iloc[coord])
#         testdis[coord] = gpd.distance(testpos, pos).km
#     mindistidx = np.argmin(testdis)
#     if(testdis[mindistidx] < minval):
#         print(idx)#=237
#         print(mindistidx) #=649
#         print(testdis[mindistidx]) #0.0010567557775868317
#         minval = testdis[mindistidx]



posold = (df2['Latitude'].iloc[0],df2['Longitude'].iloc[0])
dis = np.zeros(df2.values.shape[0])
for coord in range(1,df2.values.shape[0]):
    pos = (df2['Latitude'].iloc[coord], df2['Longitude'].iloc[coord])
    dis[coord] = gpd.distance(posold, pos).km + dis[coord-1]
    posold=pos

dis = dis - np.ones_like(dis)*(dis[649]-df['Relative Position'].values[237]) #correct offset

df2['Relative Position'] = dis

df = pd.concat([df,df2])
df = df.sort_values(by=['Relative Position'])
df = df[df['Relative Position']>40]
df = df[df['Relative Position']<65.5]
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    m = folium.Map(
        location=[np.mean(lat[np.isfinite(lat)]), np.mean(lon[np.isfinite(lat)])], zoom_start=13
    )

    data = io.BytesIO()

    lat = df['Latitude'].to_numpy()
    lon = df['Longitude'].to_numpy()
    relpos = df['Relative Position'].to_numpy()
    latc = lat[np.isfinite(lat)]
    lonc = lon[np.isfinite(lon)]
    relpos = relpos[np.isfinite(lon)]
    for i in range(0,len(lonc)):
        folium.Marker(location=[latc[i], lonc[i]], popup=relpos[i]).add_to(m)

    # for i in range(0, len(latint)):
    #     folium.Marker(location=[latint[i], lonint[i]]).add_to(m)
    #
    folium.GeoJson(
        gj,
        name='geojson'
    ).add_to(m)

    m.save(outfile='map_1.html', close_file=False)

    # w = QtWebEngineWidgets.QWebEngineView()
    # w.setHtml(data.getvalue().decode())
    # w.resize(640, 480)
    # w.show()



    #sys.exit(app.exec_())