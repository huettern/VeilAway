import os
import piexif
import pandas as pd
import numpy as np
from scipy import spatial
import io
import sys
import folium
import re
from PyQt5 import QtWidgets, QtWebEngineWidgets

import gpxpy
import geojson
import geopy.distance as gpd
from scipy.interpolate import interpolate

path_to_images_filisur_thusis = r"D:\Dataset_complete\Trackpictures\nice_weather\nice_weather_filisur_thusis_20200824_pixelated"
path_to_images_thusis_filisur = r"D:\Dataset_complete\Trackpictures\nice_weather\nice_weather_thusis_filisur_20200827_pixelated"

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
    return map

def read_geojson(path):
    with open(os.path.realpath(path)) as f:
        gj = geojson.load(f)
        return gj

def geojson_to_df(gj):

    # Keep only polyline
    gj['features'] = [gj['features'][2]]
    df=pd.DataFrame()
    for feat in gj['features']:
        for coord in feat['geometry']['coordinates']:
            df_new = pd.DataFrame([[coord[0], coord[1], 'geojson']], columns=['Longitude', 'Latitude', 'Element Type'])
            df = pd.concat([df, df_new])

    posold = (df['Latitude'].iloc[0], df['Longitude'].iloc[0])
    dis = np.zeros(df.values.shape[0])
    for coord in range(1, df.values.shape[0]):
        pos = (df['Latitude'].iloc[coord], df['Longitude'].iloc[coord])
        dis[coord] = gpd.distance(posold, pos).km + dis[coord - 1]
        posold = pos
    df['Relative Position'] = dis + 39.54579102261809  # correct offset
    return df

def concat_interp(dfs_to_concat):
    df = pd.concat(dfs_to_concat)
    df = df.sort_values(by=['Relative Position'])
    df = df[df['Relative Position'] > 40] #Filter what's out of range
    df = df[df['Relative Position'] < 65.5]

    rp = df['Relative Position'].to_numpy()
    lat = df['Latitude'].to_numpy()
    lon = df['Longitude'].to_numpy()

    f_lat = interpolate.interp1d(rp[np.isfinite(lat)], lat[np.isfinite(lat)], fill_value='extrapolate')
    f_lon = interpolate.interp1d(rp[np.isfinite(lon)], lon[np.isfinite(lon)], fill_value='extrapolate')
    latint = f_lat(rp)
    lonint = f_lon(rp)
    df['Longitude'] = lonint
    df['Latitude'] = latint
    return df

def init_gps_dist_tree(df):
    points = df[['Latitude', 'Longitude']].to_numpy()
    availpt = np.reshape(points[np.isfinite(points)], [-1, 2])
    return spatial.KDTree(availpt)

def gps_to_dist(pts,tree):
    return tree.query(pts)

def read_track_from_exif_images(path_to_images):
    images = os.listdir(path_to_images)
    images = [img for img in images if img[-4:] == ".jpg"]
    gps_measurements = pd.DataFrame()

    for img in images:
        exif_dict = piexif.load(os.path.join(path_to_images, img))
        row_dict = exif_dict['GPS']
        row_dict["ImgName"] = img
        gps_measurements = gps_measurements.append(row_dict, ignore_index=True)

    column_names = []
    for tag in gps_measurements.columns:
        if tag != "ImgName":
            column_names.append(piexif.TAGS['GPS'][tag]["name"])
        else:
            column_names.append("ImgName")

    gps_measurements.columns = column_names
    gps_measurements['GPSLatitude'] = gps_measurements['GPSLatitude'].map(lambda x: x[0] / x[1])
    gps_measurements['GPSLongitude'] = gps_measurements['GPSLongitude'].map(lambda x: x[0] / x[1])
    gps_measurements['GPSAltitude'] = gps_measurements['GPSAltitude'].map(lambda x: 1 if pd.isna(x) else x[0] / x[1])
    gps_measurements['GPSDOP'] = gps_measurements['GPSDOP'].map(lambda x: x[0] / x[1])
    gps_measurements['GPSSpeed'] = gps_measurements['GPSSpeed'].map(lambda x: x[0] / x[1])
    return gps_measurements



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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    m = folium.Map(
        location=[46.689477, 9.499883], zoom_start=13
    )

    data = io.BytesIO()

    dfobj = pd.read_excel(os.path.realpath('TrackSiteData_2020_clean.xlsx'), index_col=None)
    gj = read_geojson('export.geojson')
    dfgj = geojson_to_df(gj)
    dfobjgj = concat_interp([dfobj, dfgj]).reset_index(drop=True)
    tree_dist = init_gps_dist_tree(dfobjgj)
    dfimg = pd.DataFrame(read_track_from_exif_images(path_to_images_thusis_filisur))
    closest_gps_points = gps_to_dist(dfimg[['GPSLatitude', 'GPSLongitude']].to_numpy().reshape([-1,2]), tree_dist)
    print(np.max(closest_gps_points[0]))#max approx error
    closest_gps_points_unique, idx_closest_gps_points_unique, inv_closest_gps_points_unique = np.unique(closest_gps_points[1], return_index=True, return_inverse=True)
    pic = dict(zip(closest_gps_points_unique, dfimg['ImgName'][idx_closest_gps_points_unique]))
    dfobjgj['Closest Image'] = np.zeros_like(dfobjgj['Relative Position'].to_numpy())
    dfobjgj['Closest Image'][pic.keys()] = pic
    imagenums = dfobjgj['Closest Image'].str.extract('(\d+)')


    folium.GeoJson(
        gj,
        name='geojson'
    ).add_to(m)

    m.save(outfile='map_1.html', close_file=False)