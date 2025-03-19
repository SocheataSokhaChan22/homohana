import  os
from unittest.mock import patch
from pymongo import MongoClient
from backend.db.database import get_db

def test_get_db():
    # Mock the contents of the mongodb.yaml file
    mock_env_vars = {
        "MONGO_URI": "mongodb://localhost:27017/scraperdb",
        "MONGO_DB_NAME": "kh_scraper"
    }

    mock_mongo_uri = mock_env_vars["MONGO_URI"]
    mock_db_name = mock_env_vars["MONGO_DB_NAME"]
    
    mock_client = MongoClient(mock_mongo_uri)

    with patch.dict(os.environ, mock_env_vars):
        with patch("pymongo.MongoClient", return_value=mock_client):
            db = get_db()
            assert db.name == mock_db_name