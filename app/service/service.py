"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def find(self, filters: dict) -> list:
        pass

    @abstractmethod
    def find_one(self, filters: dict) -> dict:
        pass