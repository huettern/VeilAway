import numpy as np
import piexif
import os
import pandas as pd
import gpxpy
import json
from tabulate import tabulate

import base64
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets
import sys
import io
from math import sin, cos, sqrt, atan2, radians
from folium import IFrame
from io import BytesIO
from PIL import Image

def read_gps_data_from_json(path_to_json):
    with open(path_to_json, 'r') as fp:
        fp.seek(3)
        gps_data = json.load(fp)

    gps_data = pd.DataFrame(gps_data["Trackdata"])
    gps_data = gps_data.rename(columns={"Latitude": "GPSLatitude", "Longitude": "GPSLongitude"}, inplace=False)
    # print(tabulate(gps_data, headers='keys', tablefmt='psql'))
    return gps_data

def read_track_from_gpx(path_to_gpx):
    file = open(path_to_gpx)
    gpx = gpxpy.parse

def read_track_from_exif_images(path_to_images):
    images = os.listdir(path_to_images)[:1000]
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
    gps_measurements['GPSAltitude'] = gps_measurements['GPSAltitude'].map(lambda x: np.NaN if pd.isna(x) else x[0] / x[1])
    gps_measurements['GPSDOP'] = gps_measurements['GPSDOP'].map(lambda x: x[0] / x[1])
    gps_measurements['GPSSpeed'] = gps_measurements['GPSSpeed'].map(lambda x: x[0] / x[1])
    # gps_measurements_good = gps_measurements[gps_measurements['GPSDOP'] < 3]
    # gps_measurements_bad = gps_measurements[gps_measurements['GPSDOP'] >= 3]

    return gps_measurements

def linear_interpolation_of_tracks(good, bad):
    pass

def plot_markers(dataframe):
    app = QtWidgets.QApplication(sys.argv)
    token = "pk.eyJ1IjoiaGFja3p1cmljaHVzZXIiLCJhIjoiY2tmOWl4NjU0MG1rcDJ5cWdxbHphNzQ5ayJ9.IEOl1OkLzh_vgznx38Anog"  # your mapbox token
    tileurl = 'https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)

    m = folium.Map(
        location=[dataframe['GPSLatitude'].values[0], dataframe['GPSLongitude'].values[0]],
        zoom_start=13, tiles=tileurl, attr='Mapbox'
    )

    for index, row in dataframe.iterrows():
        folium.Marker([row['GPSLatitude'], row['GPSLongitude']]).add_to(m)

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec_())

def plot_track_as_line(dataframe):
    app = QtWidgets.QApplication(sys.argv)
    token = "pk.eyJ1IjoiaGFja3p1cmljaHVzZXIiLCJhIjoiY2tmOWl4NjU0MG1rcDJ5cWdxbHphNzQ5ayJ9.IEOl1OkLzh_vgznx38Anog"  # your mapbox token
    tileurl = 'https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)

    m = folium.Map(
        location=[dataframe['GPSLatitude'].values[0], dataframe['GPSLongitude'].values[0]],
        zoom_start=13, tiles=tileurl, attr='Mapbox'
    )

    points = []
    for index, row in dataframe.iterrows():
        points.append((row['GPSLatitude'], row['GPSLongitude']))

    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec_())

def plot_track_and_markers(track, markers):
    app = QtWidgets.QApplication(sys.argv)
    token = "pk.eyJ1IjoiaGFja3p1cmljaHVzZXIiLCJhIjoiY2tmOWl4NjU0MG1rcDJ5cWdxbHphNzQ5ayJ9.IEOl1OkLzh_vgznx38Anog"  # your mapbox token
    tileurl = 'https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)

    m = folium.Map(
        location=[track['GPSLatitude'].values[0], track['GPSLongitude'].values[0]],
        zoom_start=13, tiles=tileurl, attr='Mapbox'
    )

    points = []
    for index, row in track.iterrows():
        points.append((row['GPSLatitude'], row['GPSLongitude']))

    for index, row in markers.iterrows():
        folium.Marker([row['GPSLatitude'], row['GPSLongitude']]).add_to(m)

    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec_())


def calc_distance_between_points(p1, p2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(p1[0])
    lon1 = radians(p1[1])
    lat2 = radians(p2[0])
    lon2 = radians(p2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def find_relative_pos_on_track(track, obj_markers):
    track_gps = track.copy()
    obj_gps_data = obj_markers.copy()
    obj_gps_data = obj_gps_data.rename(columns={"GPSLatitude": "GPSLatitudeObj", "GPSLongitude": "GPSLongitudeObj"}, inplace=False)
    table_relative_postions = obj_gps_data.groupby(["Relative Position"]).mean()
    for col_name in track_gps.columns:
        table_relative_postions[col_name] = None

    for index, row in table_relative_postions.iterrows():
        point = (row["GPSLatitudeObj"], row["GPSLongitudeObj"])
        track_gps['Distances'] = track_gps.apply(lambda x: calc_distance_between_points(point, (x["GPSLatitude"], x["GPSLongitude"])), axis=1)
        small_distances = track_gps[track_gps['Distances'] < 0.04]
        if not small_distances.empty:
            min_idx = track_gps['Distances'].idxmin()
            table_relative_postions.loc[index, track_gps.columns] = track_gps.loc[min_idx]

    table_relative_postions = table_relative_postions[table_relative_postions["ImgName"].notnull()]
    table_relative_postions = table_relative_postions.drop_duplicates(subset="ImgName", keep="first")
    table_of_obj = table_relative_postions.copy()
    table_relative_postions["ImgNumber"] = table_relative_postions.apply(lambda x: extract_img_number(x), axis=1)
    first_img = table_relative_postions["ImgNumber"].iloc[0]
    last_img = table_relative_postions["ImgNumber"].iloc[-1]
    table_relative_postions = table_relative_postions.reset_index().set_index("ImgNumber")
    new_index = pd.Index(np.arange(first_img, last_img, 1), name="ImgNumber")
    table_relative_postions = table_relative_postions.reindex(new_index)
    table_relative_postions["ImgNumber"] = table_relative_postions.index
    table_relative_postions["ImgName"] = table_relative_postions["ImgNumber"].apply(lambda x: "image_" + str(x).zfill(5) + ".jpg")
    table_relative_postions = table_relative_postions.interpolate(method="linear")
    table_relative_postions = table_relative_postions[["Relative Position", "ImgName", "ImgNumber"]]

    total_table = pd.merge(table_relative_postions, track_gps, on="ImgName")
    total_table = total_table.drop_duplicates(subset="Relative Position")
    total_table_sh = total_table.copy()
    for index, row in obj_gps_data.iterrows():
        total_table_sh['Distance Relative Position'] = total_table.apply(lambda x: abs(x["Relative Position"]-row["Relative Position"]), axis=1)
        min_idx = total_table_sh['Distance Relative Position'].idxmin()
        obj_gps_data.loc[index, total_table_sh.columns] = total_table_sh.loc[min_idx]

    return total_table, obj_gps_data

def extract_img_number(row):
    img_name = row["ImgName"]
    img_name = img_name.replace(".", "_").split("_")
    return [int(s) for s in img_name if s.isdigit()][0]

def plot_obj_images_on_map(obj_gps_pos, track_gps, path_to_images):
    app = QtWidgets.QApplication(sys.argv)
    token = "pk.eyJ1IjoiaGFja3p1cmljaHVzZXIiLCJhIjoiY2tmOWl4NjU0MG1rcDJ5cWdxbHphNzQ5ayJ9.IEOl1OkLzh_vgznx38Anog"  # your mapbox token
    tileurl = 'https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)

    m = folium.Map(
        location=[obj_gps_pos['GPSLatitude'].values[0], obj_gps_pos['GPSLongitude'].values[0]],
        zoom_start=13, tiles=tileurl, attr='Mapbox'
    )

    for index, row in obj_gps_pos.iterrows():
        img_path = "file:///" + path_to_images.replace("\\", "/") + "/" + row["ImgName"]
        html = '<div><img src="{}" width="512" height="384"></div>'.format(img_path)
        frame = IFrame(html=html, width=512, height=384)
        popup = folium.Popup(frame, max_width=1024)
        folium.Marker([row['GPSLatitude'], row['GPSLongitude']], popup=popup).add_to(m)

    points = []
    for index, row in track_gps.iterrows():
        points.append((row['GPSLatitude'], row['GPSLongitude']))
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(m)

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec_())

# print(tabulate(table_relative_postions, headers='keys', tablefmt='psql'))
if __name__ == "__main__":
    path_to_json_gps_data = r"D:\HackZurich\Data\Trackdata\TrackSiteData_2020_clean.json"
    gps_data_objects = read_gps_data_from_json(path_to_json_gps_data)
    gps_data_objects_with_gps_coords = gps_data_objects[gps_data_objects['GPSLatitude'].notna() & gps_data_objects['GPSLongitude'].notna()]
    #
    # plot_markers(gps_data_objects_with_gps_coords)


    # path_to_images_filisur_thusis = r"D:\HackZurich\Data\Trackpictures\nice_weather\nice_weather_filisur_thusis_20200824_pixelated"
    # gps_track_data_filisur_thusis = pd.DataFrame()
    # gps_track_data_filisur_thusis = read_track_from_exif_images(path_to_images_filisur_thusis)

    path_to_images_thusis_filisur = r"D:\HackZurich\Data\Trackpictures\nice_weather\nice_weather_thusis_filisur_20200827_pixelated"
    gps_track_data_thusis_filisur = pd.DataFrame()
    gps_track_data_thusis_filisur = read_track_from_exif_images(path_to_images_thusis_filisur)

    table_relative_postions, obj_gps_pos = find_relative_pos_on_track(gps_track_data_thusis_filisur, gps_data_objects_with_gps_coords)

    plot_obj_images_on_map(obj_gps_pos, gps_track_data_thusis_filisur, path_to_images_thusis_filisur)
    # plot_track_and_markers(gps_track_data_filisur_thusis, gps_data_objects_with_gps_coords)



    # plot_track_as_line(gps_track_data_filisur_thusis)


