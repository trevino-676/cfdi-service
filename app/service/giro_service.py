"""
author: Luis Manuel Torres Trevino
date: 14/04/2021
"""
from app.repository import Repository, GiroMongoRepository
from app.service import Service


class GiroService(Service):
    def __init__(self, repository: Repository):
        self.repository = repository

    def find(self, filters: dict) -> list:
        return self.repository.find(filters)

    def find_one(self, filters: dict) -> dict:
        return self.repository.find_one(filters)

    def save(self, giro: dict) -> bool:
        return GiroMongoRepository.save(giro)

    def remove(self, id: str = None, giro: dict = None) -> bool:
        return GiroMongoRepository.delete(id, giro)
