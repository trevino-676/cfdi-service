"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app.models import Nomina
from app.repository import Repository
from app import app


class NominaMongoRepository(Repository):
    def find(self, filters: dict, nomina_type: str = None) -> list:
        """
        Busca los documentos de nomina en la base de datos
        :param filters: diccionario con los filtros de busqueda
        :return: lista con todos los documentos de nomina encontrados
        """
        try:
            nominas = Nomina.find_all(filters, nomina_type)
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

    def find_by_period(self, filters: dict, company_rfc: str):
        try:
            nominas = Nomina.find_by_period(filters, company_rfc)
            return nominas
        except Exception as e:
            app.logger.error(e)
            return None

    def aggregate(self, filters: list) -> dict:
        """
        Busqueda de tipo aggregate a la coleccion de Nomina
        :param filters: lista de diccionarios con los filtros de busqueda
        :return: diccionario con los datos correspondientes.
        """
        try:
            cfdi = Nomina.find_agg(filters)
            app.logger.info(f"Respuesta con {len(cfdi)} datos")
            return cfdi
        except Exception as e:
            app.logger.error(e)
            return None