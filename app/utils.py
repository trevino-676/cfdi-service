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


def make_filters(type: FilterType, filters: dict) -> dict:
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
    else:
        raise Exception("The type isn't valid option")

    return new_filters

