"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from app.service import Service
from app.repository import Repository


class NominaService(Service):
    def __init__(self, repo: Repository):
        self.repository = repo

    def find_one(self, filters: dict) -> dict:
        return self.repository.find_one(filters)

    def find(self, filters: dict) -> dict:
        return self.repository.find(filters)
