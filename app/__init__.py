"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
import logging

from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

mongo = PyMongo()
mongo_cfdi = PyMongo()
app = None
cors = None


def create_app(settings_module="config.Config"):
    global app
    global cors
    global mongo
    global mongo_cfdi

    if app is not None:
        return app

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(settings_module)
    cors = CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    configure_logging(app)

    mongo.init_app(app, authSource="admin")
    mongo_cfdi.init_app(
        app, uri=app.config["MONGO_CFDI_URI"], authSource="admin")

    from app.routes import nomina_routes
    app.register_blueprint(nomina_routes)

    from app.routes import giro_routes
    app.register_blueprint(giro_routes)

    from app.routes import principal_routes
    app.register_blueprint(principal_routes)

    from app.routes import pagos_routes
    app.register_blueprint(pagos_routes)

    return app


def configure_logging(app: Flask):
    """
    Configura el modulo de logs. Establece los manejadores para cada logger.

    :param app (Flask): Instancia de la aplicacion Flask
    """
    del app.logger.handlers[:]

    loggers = [app.logger, ]
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(verbose_formatter())

    if app.config["FLASK_ENV"] == "development" or app.config["FLASK_ENV"] == "test":
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config["FLASK_ENV"] == "production":
        console_handler(logging.INFO)
        handlers.append(console_handler)

    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)


def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )
