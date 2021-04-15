"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from flask import Blueprint, make_response, request
from bson.json_util import dumps

from app.service import service
from app.utils import FilterType, make_filters

nomina_routes = Blueprint('nomina', __name__, url_prefix="/v1/nomina")


@nomina_routes.route("/", methods=["GET"])
def find_nomina():
    """
    Busca un solo documento de nomina que coincida con los filtros
    """
    nomina = service.find_one(make_filters(
        FilterType.AND if request.json["filter_type"] == "and" else FilterType.OR,
        request.json["filter"]))
    if nomina is None:
        make_response(
            dumps({"status": False, "message": "No se encontro ningun recibo de nomina"}),
            404)
    return make_response(dumps({"status": True, "data": nomina}), 200)


@nomina_routes.route("/all", methods=["GET"])
def find_all_nominas():
    """find_all_nominas
    Busca todos los documentos que coincidan con los filtros
    """
    nominas = service.find(
        make_filters(FilterType.AND if request.json["filter_type"] else FilterType.OR,
                     request.json["filter"]))
    if nominas is None:
        make_response(
            dumps({"status": False, "message": "No se encontro ningun recibo de nomina"}),
            404)
    return make_response(dumps({"status": True, "data": nominas}), 200)
