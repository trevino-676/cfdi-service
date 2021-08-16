"""
author: ErrataSEV
date: 12/08/2021
"""
from app.models import Principal
from app.service import Service
from app.repository import Repository


class PrincipalService(Service):
    def __init__(self, repo: Repository):
        self.repository = repo

    def find_one(self, filters: dict) -> dict:
        return self.repository.find_one(filters)

    def find(self, filters: dict) -> list:
        return self.repository.find(filters)
    
    def aggregate(self, filters: list) -> dict:
        return self.repository.aggregate(filters)