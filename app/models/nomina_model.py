"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app import mongo, app
from app.models import Model


class Nomina(Model):
    collection = mongo.db[app.config["NOMINA_COLLECTION"]]
