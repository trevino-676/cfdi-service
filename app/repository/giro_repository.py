"""
author: Luis Manuel Torres Trevino
date: 14/04/2021
"""
from bson import ObjectId

from app.models import Giro
from app.repository import Repository


class GiroMongoRepository(Repository):
    def find_one(self, filters: dict) -> dict:
        """
        Busca en la base de datos el documento de giro que coincida
        con los filtros
        :param filters: diccionario con los filtros aceptados por
            mongodb
        :return: Documento de con los datos de giro
        """
        try:
            giro = Giro()
            giro.find(filters)
            return giro
        except Exception as e:
            print(e)
            return None

    def find(self, filters: dict) -> list:
        """
        Busca en la base de datos todos los documentos de giro que
        coinciden con los filtros.
        :param filters: diccionario con los filtros aceptados por
            mongodb
        :return: lista con los documentos de giro
        """
        try:
            giro_documents = Giro.find_all(filters)
            return giro_documents
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def save(giro: dict) -> bool:
        """
        Guarda un diccionario con los datos de giro
        :param giro: datos que contiene el documento de giro
        :return: bandera True si se guardo correctamente y False si
            hubo un error.
        """
        try:
            giro = Giro(giro)
            giro.save()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def delete(id: str = None, giro: dict = None) -> bool:
        """
        ELimina un documento de giro en la base de datos
        :param id: id del documento (opcional)
        :param giro: documento de giro que se va a eliminar (opcional)
        :return: bandera True si se elimino correctamente y False si
            hubo un error.
        """
        temporal_giro = None
        try:
            if id is not None:
                temporal_giro = Giro().find({"_id": ObjectId(id)})
            else:
                temporal_giro = Giro(giro)
            temporal_giro.remove()
            return True
        except Exception as e:
            print(e)
            return False
