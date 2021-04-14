"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app import mongo, app
from app.models import Model


class Nomina(Model):
    collection = mongo.db[app.config["NOMINA_COLLECTION"]]

    def response_data(self) -> dict:
        """response_data
        esta funcion genera un diccionario con la respuesta que se espera.
        :return: (dict) nuevo diccionario con respuesta
        """
        return {
            "tipo": self.datos["Tipo"] if self.datos["Tipo"] is not None else "N",
            "fecha_comprobante": self.datos["Fecha"],
            "Fecha_cancelacion": "",
            "giro": "",
            "rfc_emisor": self.datos["Rfc"],
            "nombre_direccion": self.datos["Nombre"],
            "xml_estado": "",
            "xml_subtotal": "",
            "giro_subtotal": "",
            "xml_impuesto_gravado": "",
            "giro_impuesto_gravado": "",
            "xml_impuesto_exento": "",
            "giro_impuesto_exento": "",
            "xml_otros_pagos": "",
            "giro_otros_pagos": "",
            "xml_iva": "",
            "giro_iva": "",
            "xml_retencion": "",
            "giro_retencion": "",
            "xml_descuento": "",
            "giro_descuento": "",
            "xml_total": "",
            "giro_total": "",
            "uso": "",
            "descripcion": "",
            "uuid": self.uuid,
            "semp": ""
        }