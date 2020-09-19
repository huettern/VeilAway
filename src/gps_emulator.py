import numpy as np
import piexif
import os
import pandas as pd
from tabulate import tabulate

import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets
import sys
import io
from math import sin, cos, sqrt, atan2, radians


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
    # gps_measurements_good = gps_measurements[gps_measurements['GPSDOP'] < 3]
    # gps_measurements_bad = gps_measurements[gps_measurements['GPSDOP'] >= 3]

    return gps_measurements
    # gps_measurements_interp = linear_interpolation_of_tracks(gps_measurements_good, gps_measurements_bad)
    # gps_measurements_interp.drop_duplicates()
    # return gps_measurements_interp

def linear_interpolation_of_tracks(good, bad):
    pass

def plot_track_as_line(dataframe):
    app = QtWidgets.QApplication(sys.argv)
    token = "pk.eyJ1IjoiaGFja3p1cmljaHVzZXIiLCJhIjoiY2tmOWl4NjU0MG1rcDJ5cWdxbHphNzQ5ayJ9.IEOl1OkLzh_vgznx38Anog"  # your mapbox token
    tileurl = 'https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token=' + str(token)

    m = folium.Map(
        location=[dataframe['GPSLatitude'][0], dataframe['GPSLongitude'][0]],
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

def combine_tracks(first_track, second_track):
    total_track = pd.DataFrame(columns=first_track.columns)
    total_track_unorderd = pd.concat([first_track, second_track])
    row = total_track_unorderd.iloc[0]
    current_point = (row['GPSLatitude'], row['GPSLongitude'])
    total_track = total_track.append(row)
    total_track_unorderd = total_track_unorderd.drop(0)
    while not total_track_unorderd.empty:
        total_track_unorderd['distances'] = total_track_unorderd.apply(lambda row:
                                                     calc_distance_between_points(
                                                         (row['GPSLatitude'], row['GPSLongitude']),
                                                         (current_point[0], current_point[1])
                                                     ))
        min_index = total_track_unorderd['distances'].idxmin()
        row = total_track_unorderd.iloc[min_index]
        total_track.append(row)
        current_point = (row['GPSLatitude'], row['GPSLongitude'])
        total_track_unorderd = total_track_unorderd.drop(min_index)




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

    # print("Result:", distance)
    # print("Should be:", 278.546, "km")


# print(tabulate(gps_measurements, headers='keys', tablefmt='psql'))
if __name__ == "__main__":
    path_to_images_filisur_thusis = r"D:\HackZurich\Data\Trackpictures\nice_weather\nice_weather_filisur_thusis_20200824_pixelated"
    path_to_images_thusis_filisur = r"D:\HackZurich\Data\Trackpictures\nice_weather\nice_weather_thusis_filisur_20200827_pixelated"
    gps_track_data_filisur_thusis = pd.DataFrame()
    gps_track_data_filisur_thusis = read_track_from_exif_images(path_to_images_filisur_thusis)
    # gps_track_data_thusis_filisur= pd.DataFrame()
    # gps_track_data_thusis_filisur= read_track_from_exif_images(path_to_images_thusis_filisur)
    #
    # total_track = combine_tracks(gps_track_data_filisur_thusis, gps_track_data_thusis_filisur)
    plot_track_as_line(gps_track_data_filisur_thusis)

    # app = QtWidgets.QApplication(sys.argv)
    # m = folium.Map(
    #     location=[gps_track_data['GPSLatitude'][0], gps_track_data['GPSLongitude'][0]], tiles="Stamen Toner", zoom_start=13
    # )
    #
    # for index, row in gps_track_data.iterrows():
    #     folium.Marker([row['GPSLatitude'], row['GPSLongitude']]).add_to(m)
    #
    # data = io.BytesIO()
    # m.save(data, close_file=False)
    #
    # w = QtWebEngineWidgets.QWebEngineView()
    # w.setHtml(data.getvalue().decode())
    # w.resize(640, 480)
    # w.show()
    #
    # sys.exit(app.exec_())


    # path_to_nice_weather_images = r"D:\HackZurich\Data\Trackpictures\nice_weather\nice_weather_filisur_thusis_20200824_pixelated"
    # img_name = "image_01248.jpg"
    # exif_dict = piexif.load(os.path.join(path_to_nice_weather_images, img_name))
    # for ifd in ("0th", "Exif", "GPS", "1st"):
    #     for tag in exif_dict[ifd]:
    #         print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])


