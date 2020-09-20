# trainline

## setup

```
python3.7 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## run

```
python src/main.py
```

## Examples

Folium map
```
python src/examples/folium.py
```

## Generate html for Signal view
```
npm install -g html-inline 
html-inline signal-app/index.html -o assets/signals.html
```