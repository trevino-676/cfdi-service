"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app.service import Service
from app.repository import Repository
from app.repository import NominaMongoRepository


class NominaService(Service):
    def __init__(self, repo: Repository):
        self.repository = repo

    def find_one(self, filters: dict) -> dict:
        return self.repository.find_one(filters)

    def find(self, filters: dict, nomina_type: str = None) -> list:
        return self.repository.find(filters, nomina_type)

    def find_by_period(self, filters: dict, company_rfc: str):
        service = NominaMongoRepository()
        return service.find_by_period(filters, company_rfc)
