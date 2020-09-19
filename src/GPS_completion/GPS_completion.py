import os
import pandas as pd
import numpy as np
from scipy import interpolate
import io
import sys
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets

import gpxpy


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

f_lat = interpolate.interp1d(rp[np.isfinite(lat)], lat[np.isfinite(lat)], fill_value='extrapolate')
f_lon = interpolate.interp1d(rp[np.isfinite(lon)], lon[np.isfinite(lon)], fill_value='extrapolate')
latint = f_lat(rp)
lonint = f_lon(rp)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    m = folium.Map(
        location=[np.mean(latint), np.mean(lonint)], tiles='OpenStreetMap', zoom_start=13
    )

    data = io.BytesIO()

    for i in range(0, len(latint)):
        folium.Marker(location=[latint[i], lonint[i]]).add_to(m)

    m = overlayGPX(os.path.realpath('rel.gpx'), m)
    m.save(data, close_file=False)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(data.getvalue().decode())
    w.resize(640, 480)
    w.show()



    sys.exit(app.exec_())