"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object("config.Config")

mongo = PyMongo(app, authSource="admin")
mongo_cfdi = PyMongo(app, uri=app.config["MONGO_CFDI_URI"], authSource="admin")

from app.routes import nomina_routes, giro_routes

app.register_blueprint(nomina_routes)
app.register_blueprint(giro_routes)
