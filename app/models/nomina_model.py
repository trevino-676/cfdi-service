"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app import mongo_cfdi as mongo, app
from app.models import Model


class Nomina(Model):
    collection = mongo.db[app.config["NOMINA_COLLECTION"]]

    def response_data(self, giro: dict = None) -> dict:
        """response_data
        esta funcion genera un diccionario con la respuesta que se espera.
        :return: (dict) nuevo diccionario con respuesta
        """
        if not self.__validate_structure():
            raise Exception(
                f"La nomina {self._id} no cuenta con la estructura correcta"
            )

        if giro is not None:
            if "giro_descuento" in giro:
                descuento = giro["giro_descuento"]
            else:
                descuento = giro["giro_descuneto"]
        else:
            descuento = ""

        return {
            "tipo": self.datos["Tipo"] if self.datos["Tipo"] is not None else "N",
            "fecha_comprobante": self.datos["Fecha"],
            "Fecha_cancelacion": "",
            "giro": giro["giro"] if giro is not None else "",
            "rfc_emisor": self.datos["Rfc"],
            "nombre_direccion": self.datos["Nombre"],
            "xml_estado": "V",
            "xml_subtotal": "",
            "giro_subtotal": giro["subtotal"] if giro is not None else "",
            "xml_impuesto_gravado": self.nomina["Percepciones"]["TotalGravado"]
            if "Percepciones" in self.nomina
            else "",
            "giro_impuesto_gravado": giro["giro_impuesto_gravado"]
            if giro is not None
            else "",
            "xml_impuesto_exento": self.nomina["Percepciones"]["TotalExento"]
            if "Percepciones" in self.nomina
            else "",
            "giro_impuesto_exento": giro["giro_impuesto_exento"]
            if giro is not None
            else "",
            "xml_otros_pagos": self.nomina["TotalOtrosPagos"]
            if "TotalOtrosPagos" in self.nomina
            else "",
            "giro_otros_pagos": giro["giro_otros_pagos"] if giro is not None else "",
            "xml_iva": self.impuestos["TrasladoIVA"],
            "giro_iva": giro["giro_iva"] if giro is not None else "",
            "xml_retencion": self.nomina["Deducciones"]["TotalImpuestosRetenidos"]
            if ("Deducciones" in self.nomina)
            and ("TotalImpuestosRetenidos" in self.nomina["Deducciones"])
            else "",
            "giro_retencion": giro["giro_retencion"] if giro is not None else "",
            "xml_descuento": "",
            "giro_descuento": descuento,
            "xml_total": self.datos["Total"],
            "giro_total": giro["giro_total"] if giro is not None else "",
            "uso": "P01",
            "descripcion": "Por definir",
            "uuid": self._id,
        }

    def __validate_structure(self):
        flag = True
        if self.datos is None:
            flag = False

        if self.nomina is None:
            flag = False

        if self.impuestos is None:
            flag = False

        if "Deducciones" not in self.nomina:
            flag = False

        if "Percepciones" not in self.nomina:
            flag = False

        return flag
