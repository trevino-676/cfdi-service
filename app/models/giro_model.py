"""
author: Luis Manuel Torres Trevino
date: 14/04/2021
"""
from app import mongo_cfdi as mongo, app
from app.models import Model


class Giro(Model):
    collection = mongo.db[app.config["GIRO_COLLECTION"]]

    def save(self):
        if not self.uuid:
            self.collection.insert_one(self)
        else:
            self.collection.replace_one({"uuid": self.uuid}, self)
