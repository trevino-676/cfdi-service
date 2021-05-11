"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from flask import Blueprint, make_response, request
from bson.json_util import dumps

from app.service import service
from app.utils import FilterType, make_filters, validate_params
from app import app

nomina_routes = Blueprint("nomina", __name__, url_prefix="/v1/nomina")


@nomina_routes.route("/", methods=["GET"])
def find_nomina():
    """
    Busca un solo documento de nomina que coincida con los filtros
    """
    parameters = request.json
    try:
        if validate_params(parameters):
            nomina = service.find_one(
                make_filters(
                    FilterType.AND if parameters["type"] == "and" else FilterType.OR,
                    parameters["filters"],
                )
            )
        else:
            nomina = service.find_one({})
    except Exception as e:
        print(e)
        message = str(e)
        nomina = None

    if nomina is None:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": message
                    if message
                    else "No se encontro ningun recibo de nomina",
                }
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": nomina}), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@nomina_routes.route("/all", methods=["POST"])
def find_all_nominas():
    """find_all_nominas
    Busca todos los documentos que coincidan con los filtros
    """
    parameters = request.json
    app.logger.info(parameters)
    if validate_params(parameters):
        if parameters["type"] == "date":
            nominas = service.find(
                make_filters(
                    FilterType.DATE,
                    parameters["filters"],
                    date_field="datos.Fecha",
                    rfc_field="datos.Rfc",
                ), parameters["filters"]["tipo_nomina"]
            )
        else:
            nominas = service.find(
                make_filters(
                    FilterType.AND if parameters["type"] == "and" else FilterType.OR,
                    parameters["filters"],
                ), parameters["nomina_type"]
            )
    else:
        nominas = service.find({})

    if nominas is None or len(nominas) == 0:
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun recibo de nomina"}
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": nominas}), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp
