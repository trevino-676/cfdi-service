"""
author: Luis Manuel Torres Trevino
date: 14/04/2021
"""
from flask import Blueprint, make_response, request
from bson.json_util import dumps

from app.service import giro_service
from app.utils import FilterType, make_filters

giro_routes = Blueprint("giro", __name__, url_prefix="/v1/giro")


@giro_routes.route("/", methods=["POST"])
def save_giro():
    """
    Guarda un nuevo registro de giro en la base de datos
    """
    giro = request.json["giro"]
    if giro_service.save(giro):
        resp = make_response(
            dumps({"status": True, "message": "Giro guardado correctamente"})
        )
    else:
        resp = make_response(
            dumps({"status": False, "message": "Error al guardar los datos de giro"})
        )
    resp.headers["Content-type"] = "application/json"
    return resp


@giro_routes.route("/", methods=["GET"])
def get_giro():
    """
    Busca la informacion del giro que se pasa en los filtros
    """
    filters = make_filters(
        FilterType.AND if request.json["type"] == "and" else FilterType.OR,
        request.json["filters"],
    )
    giro = giro_service.find_one(filters)
    if giro is not None:
        resp = make_response(dumps({"status": True, "data": giro}), 200)
    else:
        resp = make_response(
            dumps({"status": False, "message": "No se encontro el giro"}), 404
        )
    resp.headers["Content-type"] = "application/json"
    return resp


@giro_routes.route("/all", methods=["GET"])
def get_all_giro():
    """
    Busca los documentos de giro que coincidan con los filtros
    """
    filters = make_filters(
        FilterType.AND if request.json["type"] == "and" else FilterType.OR,
        request.json["filters"],
    )
    documents_giro = giro_service.find(filters)
    if documents_giro is not None:
        resp = make_response(dumps({"status": True, "data": documents_giro}), 200)
    else:
        resp = make_response(
            dumps({"status": False, "message": "No se encontro el giro"}), 404
        )
    resp.headers["Content-type"] = "application/json"
    return resp


@giro_routes.route("/bulk", methods=["POST"])
def save_all():
    """
    Guarda una lista de documentos de giro
    """
    documents = request.json["documents"]
    if type(documents) is not list:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": "Este endpoint solo es para hacer un guardado masivo",
                }
            ),
            500,
        )
        resp.headers["Content-Type"] = "application/json"
        return resp
    if giro_service.save_all(documents):
        resp = make_response(
            dumps({"status": True, "message": "Documentos guardados correctamente"}),
            200,
        )
        resp.headers["Content-Type"] = "application/json"
        return resp
    resp = make_response(
        dumps({"status": False, "message": "Error al guardar los datos de giro"}), 404
    )
    resp.headers["Content-Type"] = "application/json"
    return resp
