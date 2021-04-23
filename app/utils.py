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
        new_filters = {"$and": [{item: value} for item, value in filters.items()]}
    elif type == FilterType.OR:
        new_filters = {"$or": [{item: value} for item, value in filters.items()]}
    elif type == FilterType.DATE:
        if "date_field" in kwargs:
            new_filters = {kwargs["date_field"]: {"$gte": filters["from_date"],
                                                  "$lte": filters["to_date"]}}
            if "rfc" in filters:
                new_filters[kwargs["rfc_field"]] = filters["rfc"]
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
