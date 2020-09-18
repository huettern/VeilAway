# -*- coding: utf-8 -*-
# @Author: Noah Huetter
# @Date:   2020-09-18 22:58:52
# @Last Modified by:   Noah Huetter
# @Last Modified time: 2020-09-18 22:59:47

import io
import sys

import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets


html = '''<html>
<head>
<title>A Sample Page</title>
</head>
<body>
<h1>Hello, World!</h1>
<hr />
I have nothing to say.
</body>
</html>'''


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    w = QtWebEngineWidgets.QWebEngineView()
    w.setHtml(html)
    w.resize(640, 480)
    w.show()

    sys.exit(app.exec_())

