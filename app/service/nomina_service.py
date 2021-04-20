"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app.models import Giro, Nomina
from app.service import Service
from app.repository import Repository


class NominaService(Service):
    def __init__(self, repo: Repository):
        self.repository = repo

    def find_one(self, filters: dict) -> dict:
        nomina = self.repository.find_one(filters)
        giro = self.__find_giro_data(nomina._id)
        return nomina.response_data(giro)

    def find(self, filters: dict) -> list:
        nominas = self.repository.find(filters)
        result_nomina = []
        for element in nominas:
            nomina = Nomina(element)
            giro = self.__find_giro_data(nomina._id)
            result_nomina.append(nomina.response_data(giro))
        return result_nomina

    def __find_giro_data(self, uuid: str) -> dict:
        """
        Busca la informacion de giro en la base de datos relacionada
        con el uuid del documento de nominas.
        :param uuid: uuid del documento a buscar
        :return: diccionario con la informacion de giro.
        """
        filter = {"uuid": uuid}
        try:
            giro = Giro()
            giro.find(filter)
            return giro
        except Exception as e:
            print(e)
            return None