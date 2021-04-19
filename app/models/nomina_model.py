"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app import mongo_cfdi as mongo, app
from app.models import Model


class Nomina(Model):
    collection = mongo.db[app.config["NOMINA_COLLECTION"]]

    def response_data(self, giro: dict) -> dict:
        """response_data
        esta funcion genera un diccionario con la respuesta que se espera.
        :return: (dict) nuevo diccionario con respuesta
        """
        return {
            "tipo": self.datos["Tipo"] if self.datos["Tipo"] is not None else "N",
            "fecha_comprobante": self.datos["Fecha"],
            "Fecha_cancelacion": "",
            "giro": giro["giro"],
            "rfc_emisor": self.datos["Rfc"],
            "nombre_direccion": self.datos["Nombre"],
            "xml_estado": "V",
            "xml_subtotal": "",
            "giro_subtotal": giro["giro_subtotal"],
            "xml_impuesto_gravado": self.nomina["Percepciones"]["TotalGravado"],
            "giro_impuesto_gravado": giro["giro_impuesto_gravado"],
            "xml_impuesto_exento": self.nomina["Percepciones"]["TotalExento"],
            "giro_impuesto_exento": giro["giro_impuesto_exento"],
            "xml_otros_pagos": self.nomina["TotalOtrosPagos"],
            "giro_otros_pagos": giro["giro_otros_pagos"],
            "xml_iva": self.impuestos["TrasladoIVA"],
            "giro_iva": giro["giro_iva"],
            "xml_retencion": self.nomina["Deducciones"]["TotalImpuestosRetenidos"],
            "giro_retencion": giro["giro_retencion"],
            "xml_descuento": "",
            "giro_descuento": giro["giro_descuento"],
            "xml_total": self.datos["Total"],
            "giro_total": giro["giro_total"],
            "uso": "P01",
            "descripcion": "Por definir",
            "uuid": self._id,
        }