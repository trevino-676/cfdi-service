"""
author: ErrataSEV
date: 12/08/2021
"""
from flask import Blueprint, make_response, request
from flask_cors import cross_origin
from bson.json_util import dumps

from app.service import pagos_service
from app.utils import FilterType, make_filters, validate_params
from app import app

pagos_routes = Blueprint("pagos", __name__, url_prefix="/v1/pagos")


@pagos_routes.route("/", methods=["GET"])
@cross_origin()
def find_principal():
    """
    Busca un solo documento de ingresos que coincida con los filtros
    """
    parameters = request.args
    try:
        if validate_params(parameters):
            cfdi = pagos_service.find_one(
                make_filters(
                    FilterType.AND if parameters["type"] == "and" else FilterType.OR,
                    parameters["filters"],
                )
            )
        else:
            cfdi = pagos_service.find_one({})
    except Exception as e:
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


@pagos_routes.route("/all", methods=["POST"])
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

    cfdis = pagos_service.find(filters)

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


@pagos_routes.route("/get-group", methods=["POST"])
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
    try:
        cfdis = pagos_service.aggregate([
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
    except Exception as e:
        message = str(e)
        cfdi = None
    if cfdis is None or len(cfdis) == 0:
        resp = make_response(
            dumps(
                {"status": True, "data": []}
            ),
            200,
        )
    else:
        resp = make_response(dumps({"status": True, "data": cfdis}), 200)

    resp.headers["Content-Type"] = "application/json"
    return resp


@pagos_routes.route("/get-count", methods=["POST"])
@cross_origin()
def data_count():
    """data_count
    Hace una suma de los documentos que coincidan con los filtros
    """
    parameters = request.form.to_dict()
    if (not "totalCol" in parameters) :
        parameters["totalCol"] = "datos.Total"
    if (not "subTotalCol" in parameters) :
        parameters["subTotalCol"] = "datos.SubTotal"
    try:
        cfdis = pagos_service.aggregate([
            {"$match": {
                parameters["fieldMatch"]: parameters["user"],
                "datos.Fecha": {
                    "$gte": parameters["dateBegin"],
                    "$lte": parameters["dateEnd"]
                },
                "datos.Cancelado": None
            }},
            {"$project":{
                parameters["fieldMatch"]:1,
                "count": {"$sum":1},
                "total": {"$sum": "$"+parameters["totalCol"] },
                "subTotal": {"$sum": "$"+parameters["subTotalCol"]},
            }},
            {"$group":{
                "_id":"$"+parameters["fieldMatch"],
                "count": {"$sum": "$count"},
                "total": {"$sum": "$total"},
                "subTotal": {"$sum": "$subTotal"}
            }}
        ])
        if cfdis is None or len(cfdis) == 0:
            resp = make_response(
                dumps(
                    {"status": True, "data": []}
                ),
                200,
            )
        resp = make_response(dumps({"status": True, "data": cfdis}), 200)
    except Exception as e:
        app.logger.error(e)
        resp = make_response(
            dumps(
                {"status": False, "message": "No se encontro ningun cfdi de pagos"}
            ),
            404,
        )

    resp.headers["Content-Type"] = "application/json"
    return resp
