"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app import mongo_cfdi as mongo, app
from app.models import Model
from app.utils import get_set_dict


class Nomina(Model):
    collection = mongo.db[app.config["NOMINA_COLLECTION"]]
    
    def save(self):
        """
        Guarda el documento de nomina actual
        """
        if not self._id:
            self.collection.insert_one(self)
        else:
            self.collection.replace_one({"_id": self._id}, self)

    @classmethod
    def find_all(cls, filter):
        pipeline = [
            {"$match": filter},
            {"$lookup": {
                "from": "giro",
                "localField": "_id",
                "foreignField": "uuid",
                "as": "giro"
            }},
            {"$project": {"_id": 1, "impuestos": 1, "datos": 1, "nomina": 1,
                          "giro_data": {"$arrayElemAt": ["$giro_data", 0]}}},
            {"$set": get_set_dict()},
            {"$project": {"_id": 0, "impuestos": 0,
                          "datos": 0, "nomina": 0, "giro_data": 0}},
        ]
        nominas = cls.collection.aggregate(pipeline)
        return list(nominas)
