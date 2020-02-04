# SWAPI Search
A simple flask app using SWAPI


## Installation

Clone repo
```
git clone https://github.com/AhmedSa-mir/swapi-search
cd swapi-search/
```
Prepare flask env
```
pyvenv-3.5 env
mv * env/
source env/bin/activate
pip install flask flask-cors requests pytest
cd env/
```


## Run flask app
```
cd swapi_app/
python app.py
```

Open localhost:5000/ in your browser. This should load the index.html page in the templates dir


## Run tests
```
cd tests/
pytest
```
