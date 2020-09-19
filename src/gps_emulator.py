import numpy as np
import piexif
import os
import pandas as pd
from tabulate import tabulate

import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets
import sys
import io


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
    gps_measurements = gps_measurements[gps_measurements['GPSDOP'] < 3]
    gps_measurements.drop_duplicates()
    return gps_measurements


# print(tabulate(gps_measurements, headers='keys', tablefmt='psql'))
if __name__ == "__main__":
    # path_to_images = r"D:\HackZurich\Data\Trackpictures\nice_weather\nice_weather_filisur_thusis_20200824_pixelated"
    path_to_images = r"D:\HackZurich\Data\Trackpictures\nice_weather\nice_weather_thusis_filisur_20200827_pixelated"
    gps_track_data = pd.DataFrame()
    gps_track_data = read_track_from_exif_images(path_to_images)

    app = QtWidgets.QApplication(sys.argv)
    m = folium.Map(
        location=[gps_track_data['GPSLatitude'][0], gps_track_data['GPSLongitude'][0]], tiles="Stamen Toner", zoom_start=13
    )

    for index, row in gps_track_data.iterrows():
        folium.Marker([row['GPSLatitude'], row['GPSLongitude']]).add_to(m)

    data = io.BytesIO()
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec_())


    # path_to_nice_weather_images = r"D:\HackZurich\Data\Trackpictures\nice_weather\nice_weather_filisur_thusis_20200824_pixelated"
    # img_name = "image_01248.jpg"
    # exif_dict = piexif.load(os.path.join(path_to_nice_weather_images, img_name))
    # for ifd in ("0th", "Exif", "GPS", "1st"):
    #     for tag in exif_dict[ifd]:
    #         print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])


