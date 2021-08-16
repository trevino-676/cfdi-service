"""
author: ErrataSEV
date: 12/08/2021
"""
from flask import Blueprint, make_response, request
from flask_cors import cross_origin
from bson.json_util import dumps

from app.service import principal_service
from app.utils import FilterType, make_filters, validate_params
from app import app

principal_routes = Blueprint("principal", __name__, url_prefix="/v1/principal")


@principal_routes.route("/", methods=["GET"])
@cross_origin()
def find_principal():
    """
    Busca un solo documento de ingresos que coincida con los filtros
    """
    parameters = request.args
    try:
        if validate_params(parameters):
            cfdi = principal_service.find_one(
                make_filters(
                    FilterType.AND if parameters["type"] == "and" else FilterType.OR,
                    parameters["filters"],
                )
            )
        else:
            cfdi = principal_service.find_one({})
    except Exception as e:
        print(e)
        message = str(e)
        cfdi = None

    if cfdi is None:
        resp = make_response(
            dumps(
                {
                    "status": False,
                    "message": message
                    if message
                    else "No se encontro ningun recibo de cfdi",
                }
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": cfdi}), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp


@principal_routes.route("/all", methods=["POST"])
@cross_origin()
def find_all_cfdis():
    """find_all_cfdis
    Busca todos los documentos que coincidan con los filtros
    """
    parameters = request.form.to_dict()
    filters = {}
    for k, v in parameters.items():
        if v == "null":
            filters[k] = None
        else:
            filters[k] = v

    cfdis = principal_service.find(filters)

    if cfdis is None or len(cfdis) == 0:
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun recibo de nomina"}
            ),
            404,
        )
    else:
        resp = make_response(dumps({"status": True, "data": cfdis}), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp


@principal_routes.route("/get-group", methods=["POST"])
@cross_origin()
def find_data_basics():
    """find_all_cfdis
    Busca todos los documentos que coincidan con los filtros
    """

    parameters = request.form.to_dict()
    filters = {}
    for k, v in parameters.items():
        if v == "null":
            filters[k] = None
        else:
            filters[k] = v
    response = {"top": [], "data": []}
    try:
        cfdis = principal_service.aggregate([
            {"$match": {
                filters["fieldMatch"]: filters["user"],
                "datos.Fecha": {
                    "$gte": filters["dateBegin"],
                    "$lte": filters["dateEnd"]
                }
            }},
            {"$group": {
                "_id": "$"+filters["fieldGroup"],
                "count": {"$sum": 1}
            }}
        ])
        response["data"] = [filters["data"].split(",")]
    except Exception as e:
        print(e)
        message = str(e)
        cfdi = None
    if cfdis is None or len(cfdis) == 0:
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun recibo de nomina"}
            ),
            404,
        )
    else:
        print(cfdis)
        for pair in cfdis:
            response["top"].append(pair["_id"])
            response["data"].append([pair["_id"], pair["count"]])
        resp = make_response(dumps({"status": True, "data": response}), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp


@principal_routes.route("/get-count", methods=["POST"])
@cross_origin()
def data_count():
    """data_count
    Hace un conteo de los documentos que coincidan con los filtros
    """

    parameters = request.form.to_dict()
    try:
        cfdis = principal_service.aggregate([
            {"$match": {
                parameters["fieldMatch"]: parameters["user"],
                "datos.Fecha": {
                    "$gte": parameters["dateBegin"],
                    "$lte": parameters["dateEnd"]
                },
                "datos.Cancelado": None
            }},
            {"$group": {
                "_id": "$"+parameters["fieldMatch"],
                "count": {"$sum": 1},
                "total": {"$sum": "$datos.Total"},
                "subtotal": {"$sum": "$datos.SubTotal"}
            }}
        ])
        if cfdis is None or len(cfdis) == 0:
            resp = make_response(
                dumps(
                    {"status": False, "message": "No se encontro ningun recibo de nomina"}
                ),
                404,
            )
        resp = make_response(dumps({"status": True, "data": cfdis}), 200)
    except Exception as e:
        app.logger.error(e)
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun recibo de nomina"}
            ),
            404,
        )

    resp.headers["Content-Type"] = "application/json"
    return resp
