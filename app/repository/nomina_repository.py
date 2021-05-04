"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from bson import ObjectId

from app.models import Nomina
from app.repository import Repository
from app import app

class NominaMongoRepository(Repository):
    def find(self, filters: dict) -> list:
        """
        Busca los documentos de nomina en la base de datos
        :param filters: diccionario con los filtros de busqueda
        :return: lista con todos los documentos de nomina encontrados
        """
        try:
            nominas = Nomina.find_all(filters)
            app.logger.info(f"Se encontraro {len(nominas)} documentos")
            return nominas
        except Exception as e:
            app.logger.error(e)
            return None

    def find_one(self, filters: dict) -> dict:
        """
        Busca el documento de nomina en la base de datos
        :param filters: diccionario con los filtros de busqueda
        :return: diccionario con el documento encontrado.
        """
        try:
            nomina = Nomina()
            nomina.find(filters)
            app.logger.info(f"Se encontro la nomina {nomina._id}")
            return nomina
        except Exception as e:
            app.logger.error(e)
            return None

