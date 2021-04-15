"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object("config.Config")

mongo = PyMongo(app, authSource="admin")

from app.routes import nomina_routes, giro_routes

app.register_blueprint(nomina_routes)
app.register_blueprint(giro_routes)
