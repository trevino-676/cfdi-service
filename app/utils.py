"""
author: Luis Manuel Torres Trevino
date: 13/04/2021
"""
from enum import Enum


class FilterType(Enum):
    """FilterType
    Clase enum para los tipos de filtros
    """
    AND = 1
    OR = 2
    DATE = 3


def make_filters(type: FilterType, filters: dict, **kwargs) -> dict:
    """make_filters
    Genera un diccionario con los filtros para las consultas de mongodb
    :param type: Tipo de filtro que se va a generar
    :param filters: Datos que va a contener el filtro
    :return: Diccionario con la estructura aceptada por mongo
    """
    new_filters = {}
    if type == FilterType.AND:
        new_filters = {"$and": [{item: value}
                                for item, value in filters.items() if item != "tipo_nomina"]}
    elif type == FilterType.OR:
        new_filters = {"$or": [{item: value}
                               for item, value in filters.items() if item != "tipo_nomina"]}
    elif type == FilterType.DATE:
        new_filters = {
            "$and": [
                {
                    kwargs["date_field"]:{
                        "$gte": filters["from_date"], "$lte": filters["to_date"]
                    }
                },
                {
                    kwargs["rfc_field"]: filters["rfc"]
                }
            ]
        }
    else:
        raise Exception("The type isn't valid option")

    return new_filters


def validate_params(params: dict) -> bool:
    """validate_params
    Valida si los parametros enviados incluyen el tipo de filtro y
    los filtros correspondientes.
    :param params: diccionario con los filros enviados desde el
        cliente
    :return: Boolean True si cumplen, False si no
    """
    if "type" in params and "filters" in params:
        if params["type"] == "and" or params["type"] == "or" or params["type"] == "date":
            return True
        else:
            return False
    return False


def get_set_dict():
    return {
        "tipo": "$datos.Tipo",
        "fecha_comprobante": "$datos.Fecha",
        "fecha_cancelacion": "",
        "giro": {"$cond": [{"$eq": ["$giro_data", None]}, "", "$giro_data.giro"]},
        "rfc_emisor": "$datos.Rfc",
        "nombre_direccion": "$datos.Nombre",
        "xml_estado": "V",
        "xml_subtotal": "$nomina.TotalPercepciones",
        "giro_subtotal": {"$cond": [{"$eq": ["$giro_data", None]}, "0.00", "$giro_data.subtotal"]},
        "xml_impuesto_gravado": {"$cond": [{"ne": ["$nomina.Percepciones.TotalGravado", None]}, "$nomina.Percepciones.TotalGravado", "0.00"]},
        "giro_impuesto_gravado": {"$cond": [{"$eq": ["$giro_data", None]}, "0.00", "$giro_data.giro_impuesto_gravado"]},
        "xml_impuesto_exento": {"$cond": [{"$ne": ["$nomina.Percepciones.TotalExento", None]}, "$nomina.Percepciones.TotalExento", "0.00"]},
        "giro_impuesto_exento": {"$cond": [{"$eq": ["$giro_data", None]}, "", "$giro_data.giro_impuesto_exento"]},
        "xml_otros_pagos": "$nomina.TotalOtrosPagos",
        "giro_otros_pagos": {"$cond": [{"$eq": ["$giro_data", None]}, "0.00", "$giro_data.giro_otros_pagos"]},
        "xml_iva": {"$toString": "$impuestos.TrasladoIVA"},
        "giro_iva": {"$cond": [{"$eq": ["$giro_data", None]}, "0.00", "$giro_data.giro_iva"]},
        "xml_retencion": {"$cond": [{"$ne": ["$nomina.Deducciones.TotalImpuestosRetenidos", None]}, "$nomina.Deducciones.TotalImpuestosRetenidos", "0.00"]},
        "giro_retencion": {"$cond": [{"$eq": ["$giro_data", None]}, "0.00", "$giro_data.giro_retencion"]},
        "xml_descuento": "$datos.Descuento",
        "giro_descuento": {"$cond": [{"$eq": ["$giro_data", None]}, "0.00", "$giro_data.giro_descuento"]},
        "xml_total": "$datos.Total",
        "giro_total": {"$cond": [{"$eq": ["$giro_data", None]}, "0.00", "$giro_data.giro_total"]},
        "uso": "P01",
        "descripcion": "Por definir",
        "uuid": "$_id",
        "nombre_receptor": "$Receptor.Nombre",
        "rfc_receptor": "$Receptor.Rfc"
    }


def get_period_set():
    return {
        "tipo": "$nomina.datos.Tipo",
        "fecha_comprobante": "$nomina.datos.Fecha",
        "fecha_cancelacion": "",
        "giro": "$giro",
        "rfc_emisor": "$nomina.datos.Rfc",
        "nombre_direccion": "$nomina.datos.Nombre",
        "xml_estado": "V",
        "xml_subtotal": "$nomina.nomina.TotalPercepciones",
        "giro_subtotal": "$subtotal",
        "xml_impuesto_gravado": {
            "$cond": [
                {"ne": ["$nomina.nomina.Percepciones.TotalGravado", None]},
                "$nomina.nomina.Percepciones.TotalGravado",
                "0.00"
            ]
        },
        "giro_impuesto_gravado": "$giro_impuesto_gravado",
        "xml_impuesto_exento": {
            "$cond": [
                {"$ne": ["$nomina.nomina.Percepciones.TotalExento", None]},
                "$nomina.nomina.Percepciones.TotalExento",
                "0.00"
            ]
        },
        "giro_impuesto_exento": "$giro_impuesto_exento",
        "xml_otros_pagos": "$nomina.nomina.TotalOtrosPagos",
        "giro_otros_pagos": "$giro_otros_pagos",
        "xml_iva": {"$toString": "$nomina.impuestos.TrasladoIVA"},
        "giro_iva": "$giro_iva",
        "xml_retencion": {"$toString": "$nomina.nomina.Deducciones.TotalImpuestosRetenidos"},
        "giro_retencion": "$giro_retencion",
        "xml_descuento": "$nomina.datos.Descuento",
        "giro_descuento": "$giro_descuento",
        "xml_total": "$nomina.datos.Total",
        "giro_total": "$giro_total",
        "uso": "P01",
        "descripcion": "Por definir",
        "uuid": "$uuid",
        "nombre_receptor": "$nomina.Receptor.Nombre",
        "rfc_receptor": "$nomina.Receptor.Rfc",
        "periodo_giro": "$periodo",
    }
