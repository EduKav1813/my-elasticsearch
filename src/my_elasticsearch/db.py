from typing import List

from pydantic import BaseModel, Field
from pymongo import MongoClient


class Document(BaseModel):
    name: str = Field(...)
    content: str = Field(...)


class DatabaseClient:

    def __init__(
        self,
        hostname: str,
        db_name: str,
        port: int = 27017,
        default_collection: str = "DEFAULT",
    ) -> None:
        self.client: MongoClient = MongoClient(hostname, port)
        self.database = self.client[db_name]
        self.default_collection = default_collection

    def __del__(self):
        if self.__getattribute__("client"):
            self.client.close()

    def insert_document(self, document: Document, collection: str = None) -> None:
        if not collection:
            collection = self.default_collection
        self.database[collection].insert_one(document.model_dump())

    def get_document(self, document_name: str, collection: str = None) -> Document:
        if not collection:
            collection = self.default_collection
        return self.database[collection].find_one({"name": document_name})

    def get_all_documents(self, collection: str = None) -> List[Document]:
        if not collection:
            collection = self.default_collection
        return self.database[collection].find_all()
