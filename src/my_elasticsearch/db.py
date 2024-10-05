from typing import List

from pydantic import BaseModel, Field
from pymongo import MongoClient


class Document(BaseModel):
    name: str = Field(...)
    content: str = Field(...)


def dict_to_document_mapper(db_document: dict) -> Document:
    return Document(name=db_document["name"], content=db_document["content"])


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

    def drop_collection(self, collection=None):
        if not collection:
            collection = self.default_collection
        self.database[collection].drop()

    def insert_document(self, document: Document, collection: str = None) -> None:
        if not collection:
            collection = self.default_collection
        self.database[collection].insert_one(document.model_dump())

    def insert_documents(
        self, documents: List[Document], collection: str = None
    ) -> None:
        if not collection:
            collection = self.default_collection
        documents_dump = [doc.model_dump() for doc in documents]
        self.database[collection].insert_many(documents_dump)

    def find_document(self, document_name: str, collection: str = None) -> Document:
        if not collection:
            collection = self.default_collection
        document = self.database[collection].find_one({"name": document_name})
        return dict_to_document_mapper(document)

    def find_all_documents(self, collection: str = None) -> List[Document]:
        if not collection:
            collection = self.default_collection
        documents_list = self.database[collection].find().to_list()

        return list(map(dict_to_document_mapper, documents_list))
