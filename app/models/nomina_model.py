"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app import mongo_cfdi as mongo, app
from app.models import Model
from app.utils import get_set_dict, get_period_set


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
    def find_all(cls, filter, nomina_type=None):
        pipeline = [
            {"$match": filter},
            {"$lookup": {
                "from": "giro",
                "localField": "_id",
                "foreignField": "uuid",
                "as": "giro_data"
            }},
            {"$project": {"_id": 1, "Receptor": 1, "impuestos": 1, "datos": 1,
                          "nomina": 1, "giro_data": {"$arrayElemAt": ["$giro_data", 0]}}},
            {"$project": {"_id": 1, "Receptor": 1, "impuestos": 1, "datos": 1,
                          "nomina": 1, "giro_data": {"$ifNull": ["$giro_data", None]}}},
            {"$match": {"giro_data": {"$ne": None},
                        "giro_data.tipo_nomina": nomina_type}},
            {"$set": get_set_dict()},
            {"$project": {"_id": 0, "Receptor": 0, "impuestos": 0,
                          "datos": 0, "nomina": 0, "giro_data": 0}},
            {"$sort": {"fecha_comprobante": 1}},
        ]
        nominas = cls.collection.aggregate(pipeline)
        return list(nominas)

    @classmethod
    def find_by_period(cls, filters: dict, company_rfc: str):
        pipeline = [
            {"$match": filters},
            {"$lookup": {
                "from": "nomina",
                "localField": "uuid",
                "foreignField": "_id",
                "as": "nomina_data"
            }},
            {"$set": {"nomina": {"$arrayElemAt": ["$nomina_data", 0]}}},
            {"$project": {"nomina_data": 0}},
            {"$match": {"nomina.datos.Rfc": company_rfc}},
            {"$set": get_period_set()},
            {"$project": {
                "uuid": 0, "_id": 0, "giro": 0, "subtotal": 0,
                "giro_impuesto_gravado": 0, "giro_impuesto_exento": 0,
                "giro_otros_pagos": 0, "giro_iva": 0,
                "giro_retencion": 0, "giro_descuento": 0, "giro_total": 0,
                "tipo_nomina": 0, "periodo": 0,
                "nomina": 0
            }}
        ]
        nominas = mongo.db.giro.aggregate(pipeline)
        return list(nominas)
