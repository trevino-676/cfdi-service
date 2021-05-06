"""
author: Luis Manuel Torres Trevino
date: 12/04/2021
"""
from bson import ObjectId


class Model(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delattr__
    __setattr__ = dict.__setattr__

    def save(self):
        if not self._id:
            self.collection.insert_one(self)
        else:
            self.collection.replace_one({"_id": ObjectId(self._id)}, self)

    def reload(self):
        if self._id:
            self.update(self.collection.find_one({"_id": ObjectId(self._id)}))

    def remove(self):
        if self._id:
            self.collection.delete_one({"_id": ObjectId(self._id)})
            self.clear()

    def find(self, filters: dict):
        if dict is not None:
            self.update(self.collection.find_one(filters))

    @classmethod
    def find_all(cls, filters: dict) -> list:
        mongo_documents = cls.collection.find(filters)
        documents = [document for document in mongo_documents]
        return documents

    @classmethod
    def save_all(cls, documents: list):
        cls.collection.insert_many(documents)
