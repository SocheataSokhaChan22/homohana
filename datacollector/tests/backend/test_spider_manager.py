"""
Test case for app flask endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from bson import ObjectId
from backend.spider_manager import start_spider,stop_spider_task 
import subprocess
from backend.config import constants


@pytest.fixture
def mock_tasks_collection():
    """
    Fixture that mocks the "tasks_collection" in the backend.

    Yields:
        MagicMock: Mock object representing the tasks collection.
    """
    with patch("backend.spider_manager.tasks_collection") as mock:
        yield mock


@pytest.fixture
def mock_subprocess_popen():
    """
    Fixture that mocks the "subprocess.Popen" function.

    Yields:
        MagicMock: Mock object representing subprocess.Popen.
    """
    with patch("backend.spider_manager.subprocess.Popen") as mock:
        yield mock


@pytest.fixture
def mock_psutil_process():
    """
    Fixture that mocks the "psutil.Process" class.

    Yields:
        MagicMock: Mock object representing psutil.Process.
    """

    with patch("backend.spider_manager.psutil.Process") as mock:
        yield mock


def test_start_spider(mock_tasks_collection, mock_subprocess_popen):
    """
    Test case for starting a spider execution.

    Args:
        mock_tasks_collection (MagicMock): Mock object for tasks collection.
        mock_subprocess_popen (MagicMock): Mock object for subprocess.Popen.

    Assertions:
        - Verifies the task insertion with correct parameters.
        - Checks the subprocess.Popen call with the correct command and arguments.
        - Verifies the update of "process_id" in the tasks collection.
    """

    spider_id = "spider1"
    cmd = "scrapy crawl spider1"
    spiders_dir = "/path/to/spiders"
    task_id = ObjectId()
    
    mock_tasks_collection.insert_one.return_value.inserted_id = task_id
    
    # Mock the Popen object and its attributes
    mock_process = MagicMock()
    mock_process.pid = 12345
    mock_subprocess_popen.return_value = mock_process
    
    result_task_id = start_spider(spider_id, cmd, spiders_dir)
    
    assert result_task_id == str(task_id)
    mock_tasks_collection.insert_one.assert_called_once_with({
        "spider_id": spider_id,
        "status": "running",
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": None,
        "log": "",
    })
    mock_subprocess_popen.assert_called_once_with(
        (cmd + f" -a task_id={task_id} -a spider_id={spider_id}").split(),
        cwd=spiders_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    mock_tasks_collection.update_one.assert_called_once_with(
        {"_id": ObjectId(result_task_id)},
        {"$set": {"process_id": 12345}}
    )


def test_stop_spider_task(mock_tasks_collection, mock_psutil_process):
    """
    Test case for stopping a spider task.

    Args:
        mock_tasks_collection (MagicMock): Mock object for tasks collection.
        mock_psutil_process (MagicMock): Mock object for psutil.Process.

    Assertions:
        - Verifies the update of task status and end time upon successful termination.
        - Checks the termination of the process associated with the task.
    """

    task_id = "60ad78f5e1c4e9e2d4efb123"
    process_id = 12345

    task_data = {
        "_id": ObjectId(task_id),
        "process_id": process_id,
        "status": "running"
    }

    mock_tasks_collection.find_one.return_value = task_data
    mock_tasks_collection.update_one.return_value.modified_count = 1
    mock_process = MagicMock()
    mock_psutil_process.return_value = mock_process

    result = stop_spider_task(task_id)

    assert result == {"message": constants.SPIDER_STOPPED_SUCCESSFULLY}
    mock_tasks_collection.find_one.assert_called_once_with({"_id": ObjectId(task_id)})
    mock_tasks_collection.update_one.assert_called_once_with(
        {"_id": ObjectId(task_id)},
        {"$set": {
            "status": "stopped",
            "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }}
    )
    mock_psutil_process.assert_called_once_with(process_id)
    mock_process.terminate.assert_called_once()


def test_stop_spider_task_not_found(mock_tasks_collection):
    """
    Test case for stopping a spider task when the task is not found.

    Args:
        mock_tasks_collection (MagicMock): Mock object for tasks collection.

    Assertions:
        - Verifies the function returns False when no task is found.
    """

    task_id = "60ad78f5e1c4e9e2d4efb123"
    mock_tasks_collection.find_one.return_value = None

    result = stop_spider_task(task_id)

    assert result is False
    mock_tasks_collection.find_one.assert_called_once_with({"_id": ObjectId(task_id)})


def test_stop_spider_task_already_stopped(mock_tasks_collection):
    """
    Test case for stopping a spider task that is already stopped.

    Args:
        mock_tasks_collection (MagicMock): Mock object for tasks collection.

    Assertions:
        - Verifies the function returns True when the task is already stopped.
    """

    task_id = "60ad78f5e1c4e9e2d4efb123"
    task_data = {
        "_id": ObjectId(task_id),
        "status": "completed"
    }

    mock_tasks_collection.find_one.return_value = task_data

   
    result = stop_spider_task(task_id)

    assert result["message"] == constants.TASK_ALREADY_COMPLETED
    mock_tasks_collection.find_one.assert_called_once_with({"_id": ObjectId(task_id)})


def test_stop_spider_task_update_failed(mock_tasks_collection):
    """
    Test case for stopping a spider task when the update operation fails.

    Args:
        mock_tasks_collection (MagicMock): Mock object for tasks collection.

    Assertions:
        - Verifies the function returns False when the update operation fails.
    """

    task_id = "60ad78f5e1c4e9e2d4efb123"
    process_id = 12345

    task_data = {
        "_id": ObjectId(task_id),
        "process_id": process_id,
        "status": "running"
    }

    mock_tasks_collection.find_one.return_value = task_data
    mock_tasks_collection.update_one.return_value.modified_count = 0

    result = stop_spider_task(task_id)

    assert result is False
    mock_tasks_collection.find_one.assert_called_once_with({"_id": ObjectId(task_id)})
    mock_tasks_collection.update_one.assert_called_once_with(
        {"_id": ObjectId(task_id)},
        {"$set": {
            "status": "stopped",
            "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }}
    )
