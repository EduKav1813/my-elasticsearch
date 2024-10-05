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

    return {"client": client}


def test_insert(setup_data):
    client: DatabaseClient = setup_data["client"]
    document = Document(name="test_document", content="test_content")
    client.insert_document(document)
    assert True
