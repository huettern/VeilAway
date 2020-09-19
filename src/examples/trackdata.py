import json

import codecs

TDATA_FILE = '/home/noah/Trackdata/TrackSiteData_2020_clean.json'

d=json.load(codecs.open(TDATA_FILE, 'r', 'utf-8-sig'))
