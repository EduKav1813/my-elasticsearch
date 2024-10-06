import dotenv
import fire

from my_elasticsearch.db import DatabaseClient, Document
from my_elasticsearch.searchengine import SearchEngine


class Cli:

    def __init__(self) -> None:
        dotenv_data = dotenv.dotenv_values(dotenv.find_dotenv())
        self.default_collection = dotenv_data["COLLECTION_NAME"]
        self.db_client = DatabaseClient(
            hostname=dotenv_data["MONGODB_HOST"],
            port=int(dotenv_data["MONGODB_PORT"]),
            db_name=dotenv_data["DB_NAME"],
            default_collection=self.default_collection,
        )
        self.search_engine = SearchEngine()

    def insert_document(self, name: str, content: str, collection: str = None) -> None:
        """Insert a single document into specified collection.

        Args:
            name (str): Name of the document.
            content (str): Content of the document.
            collection (str, optional): _description_. Defaults to None, in
                which case the "COLLECTION_NAME" from .env will be used.

        Raises:
            RuntimeError: Raised if inserting the document fails.
        """
        if not collection:
            collection = self.default_collection
        try:
            document = Document(name=name, content=content)
            self.db_client.insert_document(document)
            print(f"Inserted document with {name=}, {content=} into {collection=}.")
        except Exception as e:
            raise RuntimeError(
                f"Cannot insert document with {name=}, {content=} into {collection=}. Exception: {e}"
            )

    def drop_collection(self, collection: str = None) -> None:
        """Drops the specified or default collection.

        Args:
            collection (str, optional): Name of the collection to be dropped.
                Defaults to 'COLLECTION_NAME' from .env .
        """
        self.db_client.drop_collection(collection)

    def delete_documents_by_name(self, name: str, collection=None) -> None:
        """Delete all documents with given name from specified colletion.

        Args:
            name (str, optional): Name of the documents to be deleted.
            collection (_type_, optional): Collection. Defaults to 'COLLECTION_NAME' from .env .
        """
        self.db_client.delete_documents(name=name, collection=collection)

    def search(
        self,
        query: str,
        collection: str = None,
        limit: int = None,
        debug_score=False,
        debug_document_name=False,
    ) -> None:
        """Search among the documents from specified collection with a query.
        Prints results in a descending list of all matches.

        Args:
            query (str): Query for search.
            collection (str, optional): Name of the collections. Defaults to 'COLLECTION_NAME' from .env.
            limit (int, optional): Output limit.. Defaults to None.

            debug_score (bool): Debug option to print scores next to the result.
                Defaults to False.
             debug_score (bool): Debug option to print document name next to the result.
                Defaults to False.

        Raises:
            RuntimeError: Raised if there are no documents in the collection to
            search through.
        """
        documents = self.db_client.find_all_documents(collection)

        if len(documents) == 0:
            raise RuntimeError(
                f"Cannot search for {query=} in {collection=}: Collection is empty"
            )

        results = []
        for document in documents:
            results.append(
                {
                    "name": document.name,
                    "content": document.content,
                    "score": self.search_engine.get_score(query, document.content),
                }
            )

        results.sort(key=lambda x: x["score"], reverse=True)
        for index, result in enumerate(results):
            if limit and index >= limit:
                break

            if result["score"] <= 0:
                break

            output = f"{index+1}) {result['content']}"

            if debug_score:
                output += f" (score = {result["score"]})"

            if debug_document_name:
                output += f" (document_name = {result["name"]})"

            print(output)


def main():
    fire.Fire(Cli)


if __name__ == "__main__":
    main()
