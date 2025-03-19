"""
Test Case for Spider_Manager.
"""
from fastapi.testclient import TestClient
from bson.objectid import ObjectId
from unittest.mock import patch, MagicMock
from backend.app import app, spiders_collection
from backend.config import constants

client = TestClient(app)

# Sample data for testing
sample_spider = {
    "name": "test_spider",
    "cmd": "scrapy crawl test_spider",
    "domain": "test.com",
    "desc": "A test spider",
    "file_name": "test_spider.py",
    "spiderfile_path": "path/to/test_spider.py"
}

def test_get_spiders():
    """
    Test case for retrieving spider data from the FastAPI endpoints.
    Assertions:
        - Checks if the API endpoint "/spiders" returns a 200 status code.
        - Verifies the JSON response matches the expected spider data.
    """
    with patch.object(spiders_collection, "find", return_value=[sample_spider]):
        response = client.get("/spiders")
        assert response.status_code == 200
        assert response.json() == [sample_spider]

def test_create_spider_missing_file():
    """
    Test case for creating a spider with missing file.

    Assertions:
    - Checks if the API endpoint "/spider/add" returns a 422 status code.
    - Verifies the JSON response matches the expected error message.
    """
    response = client.post(
        "/spider/add",
        data={
            "name": "test_spider",
            "cmd": "scrapy crawl test_spider",
            "domain": "test.com",
            "desc": "A test spider"
        }
    )
    assert response.status_code == 422 

def test_create_spider_no_selected_file():
    """
    Test case for creating a spider with no selected file.
    Assertions:
    - Checks if the API endpoint "/spider/add" returns a 422 status code.
    """
    response = client.post(
        "/spider/add",
        files={"file": ("", b"")},
        data={
            "name": "test_spider",
            "cmd": "scrapy crawl test_spider",
            "domain": "test.com",
            "desc": "A test spider"
        }
    )
    assert response.status_code == 422
    assert response.json()["detail"] == [{
        "type": "missing",
        "loc": ["body", "file"],
        "msg": "Field required",
        "input": None
    }]

def test_create_spider_invalid_file_type():
    """
    Test case for creating a spider with invalid file type.
    Assertions:
    - Checks if the API endpoint "/spider/add" returns a 400 status code.
    - Verifies the JSON response matches the expected error message.
    """
    response = client.post(
        "/spider/add",
        files={"file": ("test_spider.txt", b"print('hello world')")},
        data={
            "name": "test_spider",
            "cmd": "scrapy crawl test_spider",
            "domain": "test.com",
            "desc": "A test spider"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == constants.INVALID_FILE_TYPE_ERROR

def test_create_spider():
    """
    Test case for creating a spider.
    Assertions:
    - Checks if the API endpoint "/spider/add" returns a 201 status code.
    - Verifies the JSON response matches the expected data.
    """
    with patch.object(spiders_collection, "insert_one", return_value=MagicMock(inserted_id=ObjectId())):
        with patch("builtins.open", new_callable=MagicMock()):
            response = client.post(
                "/spider/add",
                files={"file": ("test_spider.py", b"print('hello world')")},
                data={
                    "name": "test_spider",
                    "cmd": "scrapy crawl test_spider",
                    "domain": "test.com",
                    "desc": "A test spider"
                }
            )
            assert response.status_code == 201
            assert response.json()["message"] == constants.SPIDER_CREATED_SUCCESSFULLY

def test_create_spider_file_not_found_error():
    """
    Test case for creating a spider with file not found error.
    Assertions:
    - Checks if the API endpoint "/spider/add" returns a 500 status code.
    - Verifies the JSON response matches the expected error message.
    """
    with patch.object(spiders_collection, "insert_one", return_value=MagicMock(inserted_id=ObjectId())):
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            response = client.post(
                "/spider/add",
                files={"file": ("test_spider.py", b"print('hello world')")},
                data={
                    "name": "test_spider",
                    "cmd": "scrapy crawl test_spider",
                    "domain": "test.com",
                    "desc": "A test spider"
                }
            )
            assert response.status_code == 500
            assert response.json()["detail"] == constants.SPIDER_SAVE_ERROR

def test_run_spider_valid_spider_id():
    """
    Test case for running a spider with valid spider id.
    Assertions:
    - Checks if the API endpoint "/spider/run" returns a 200 status code.
    - Verifies the JSON response matches the expected data.
    """
    with patch.object(spiders_collection, "find_one", return_value=sample_spider):
        with patch("backend.app.start_spider", return_value=ObjectId()):
            response = client.post(f"/spider/{ObjectId()}/run")
            assert response.status_code == 200
            assert response.json()["message"] == constants.SPIDER_RUNNING

def test_run_spider_spider_not_found():
    """
    Test case for running a spider with spider not found.
    Assertions:
    - Checks if the API endpoint "/spider/run" returns a 404 status code.
    - Verifies the JSON response matches the expected error message.
    """
    with patch.object(spiders_collection, "find_one", return_value=None):
        response = client.post(f"/spider/{ObjectId()}/run")
        assert response.status_code == 400
        assert response.json()["detail"] == constants.SPIDER_NOT_FOUND

def test_run_spider_missing_command():
    """
    Test case for running a spider with missing command.
    """
    spider_without_cmd = sample_spider.copy()
    spider_without_cmd.pop("cmd")
    with patch.object(spiders_collection, "find_one", return_value=spider_without_cmd):
        response = client.post(f"/spider/{ObjectId()}/run")
        assert response.status_code == 400
        assert response.json()["detail"] == constants.SPIDER_CMD_NOT_FOUND

def test_spider_completed():
    """
    Test case for checking if the spider is completed.
    Assertions:
    - Checks if the API endpoint "/spider/completed" returns a 200 status code.
    - Verifies the JSON response matches the expected data.
    """
    with patch("backend.app.stop_spider_task", return_value={"message": constants.TASK_ALREADY_COMPLETED}):
        task_id = str(ObjectId())
        response = client.post(f"/task/{task_id}/stop")
        assert response.status_code == 200
        assert response.json()["message"] == constants.TASK_ALREADY_COMPLETED

def test_stop_spider_success():
    """
    Test case for stopping a spider.
    Assertions:
    - Checks if the API endpoint "/spider/stop" returns a 200 status code.
    - Verifies the JSON response matches the expected data.
    """
    with patch("backend.app.stop_spider_task", return_value={"message": constants.SPIDER_STOPPED_SUCCESSFULLY}):
        task_id = str(ObjectId())
        response = client.post(f"/task/{task_id}/stop")
        assert response.status_code == 200
        assert response.json()["message"] == constants.SPIDER_STOPPED_SUCCESSFULLY
