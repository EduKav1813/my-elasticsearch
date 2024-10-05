import dotenv
import pytest

from my_elasticsearch.db import DatabaseClient, Document


@pytest.fixture
def setup_data():
    dotenv_data = dotenv.dotenv_values(dotenv.find_dotenv())
    assert dotenv_data != None
    client = DatabaseClient(
        hostname=dotenv_data["MONGODB_HOST"],
        port=int(dotenv_data["MONGODB_PORT"]),
        db_name="TESTDB",
        default_collection="TEST_COLLECTION",
    )
    client.drop_collection()
    return {"client": client}


def test_find(setup_data):
    client: DatabaseClient = setup_data["client"]
    document = Document(name="test_document_to_find", content="test_content")
    client.insert_document(document)

    found_document = client.find_document(document_name=document.name)
    assert document == found_document


def test_find_many(setup_data):
    client: DatabaseClient = setup_data["client"]
    documents = [
        Document(name="first_document", content="test_content"),
        Document(name="second_document", content="test_content2"),
    ]
    client.insert_documents(documents)

    found_documents = client.find_all_documents()

    assert documents == found_documents
