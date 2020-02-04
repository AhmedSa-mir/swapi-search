from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
from functools import wraps
import requests
import json
import time
import os

template_dir = os.path.abspath('../templates/')
static_dir = os.path.abspath('../static/')

app = Flask(__name__, template_folder=template_dir,static_folder=static_dir)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

SWAPI = "https://swapi.co/api/"


def print_timing(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        result = func(*args,**kwargs)
        end = time.perf_counter()
        fs = 'Function {} took {:.3f} seconds'
        print(fs.format(func.__name__, (end - start)))
        return result
    return wrapper


@print_timing
def get_film_info(film):
    return requests.get(film).json()

@print_timing
def get_homeworld_info(homeworld):
    return requests.get(homeworld).json()

@print_timing
def get_species_info(species_api):
    return requests.get(species_api).json()

@print_timing
def get_all_people_info():
    return requests.get(SWAPI + "people/").json()

@app.route('/character_info/<charactername>')
@cross_origin()
@print_timing
def get_character_info(charactername):
    if(charactername == ""):
        return('', 204)
    ret = []

    response = get_all_people_info();
    if(response == {'detail': 'Not found'}):
        return (json.dumps(ret), 204)
    else:
        for char in response['results']:
            if(charactername.lower() in char['name'].lower()):
                
                info = {}

                info["name"] = char['name']
                info["gender"] = char['gender']

                species_names = []
                species_lifespan = []
                for species_api in char['species']:
                	species_info = get_species_info(species_api);
                	species_names.append(species_info['name'])
                	species_lifespan.append(species_info['average_lifespan'])
                info["species"] = species_names
                info["average_lifespan"] = species_lifespan

                homeworld = get_homeworld_info(char['homeworld'])
                info["homeworld"] = homeworld['name']

                films = []
                for film in char['films']:
                	film_info = get_film_info(film)
                	films.append(film_info['title'])
                info["films"] = films

                ret.append(info)

        if(not ret):
            return ('[]', 200)
        return (json.dumps(ret),200)

@app.route("/")
def home():
    return render_template('index.html', title='SWAPI SEARCH')

if __name__ == "__main__":
    app.run(debug = True)