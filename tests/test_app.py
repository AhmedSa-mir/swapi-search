import pytest
from flask import Flask
import json
import sys
sys.path.append('../swapi_app/')	
from app import *

@pytest.fixture
def app_context():
	with app.app_context():
		with app.test_request_context():
			yield
	app.config['Testing'] = True

def test_empty_name(app_context):
	response = get_character_info("")
	assert response.status_code == 204
	assert response.data == b''

def test_invalid_name(app_context):
	response = get_character_info("Ahmed")
	assert response.status_code == 200
	assert response.data == b'[]'

def test_valid_name(app_context):
	response = get_character_info("Luke")
	assert response.status_code == 200
	assert all(["luke" in (a['name'].lower()) for a in json.loads(response.data.decode('utf-8'))])