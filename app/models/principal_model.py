"""
author: ErrataSEV
date: 12/08/2021
"""
from warnings import filters
from app import mongo_cfdi as mongo, app
from app.models import Model

class Principal(Model):
    collection = mongo.db[app.config["PRINCIPAL_COLLECTION"]]

    @classmethod
    def find_all(cls, filter):
        cfdis = cls.collection.find(filter)
        return list(cfdis)

    @classmethod
    def find_agg(cls, filter:list):
        cfdis = cls.collection.aggregate(filter)
        return list(cfdis)