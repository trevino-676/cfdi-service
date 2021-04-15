"""
author: Luis Manuel Torres Trevino
date: 14/04/2021
"""
from app import mongo, app
from app.models import Model


class Giro(Model):
    collection = mongo.db[app.config["GIRO_COLLECTION"]]
