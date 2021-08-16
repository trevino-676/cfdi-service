"""
author: ErrataSEV
date: 12/08/2021
"""
from bson import ObjectId

from app.models import Principal
from app.repository import Repository
from app import app


class PrincipalMongoRepository(Repository):
    def find(self, filters: dict) -> list:
        """
        Busca los documentos de ingresos en la base de datos
        :param filters: diccionario con los filtros de busqueda
        :return: lista con todos los documentos de ingresos encontrados
        """
        try:
            cfdis = Principal.find_all(filters)
            app.logger.info(f"Se encontraro {len(cfdis)} documentos")
            return cfdis
        except Exception as e:
            app.logger.error(e)
            return None

    def find_one(self, filters: dict) -> dict:
        """
        Busca el documento de ingresos en la base de datos
        :param filters: diccionario con los filtros de busqueda
        :return: diccionario con el documento encontrado.
        """
        try:
            cfdi = Principal()
            cfdi.find(filters)
            app.logger.info(f"Se encontro el ingreso {cfdi._id}")
            return cfdi
        except Exception as e:
            app.logger.error(e)
            return None

    def aggregate(self, filters: list) -> dict:
        """
        Busqueda de tipo aggregate a la coleccion de principal
        :param filters: lista de diccionarios con los filtros de busqueda
        :return: diccionario con los datos correspondientes.
        """
        try:
            cfdi = Principal.find_agg(filters)
            app.logger.info(f"Respuesta con {len(cfdi)} componentes")
            return cfdi
        except Exception as e:
            app.logger.error(e)
            return None
