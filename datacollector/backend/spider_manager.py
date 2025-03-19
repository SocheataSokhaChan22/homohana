"""
This file is for managing spiders and data collections in MongoDB.
"""
import subprocess
from datetime import datetime
from collections import namedtuple
from db.database import get_db
from bson.objectid import ObjectId
import psutil
from config import constants


db = get_db()
tasks_collection = db["tasks"]
data_collection = db["data"]

TaskData = namedtuple("TaskData", ["spider_id", "status", "start_time", "end_time", "log"])


def start_spider(spider_id, cmd, spiders_dir):
    """Start a spider and return its process id.
    Args:
        spider_id (str): The spider's id.
        cmd (str): The command to start the spider.
        spiders_dir (str): The directory where the spiders are located.
    cmd_with_task_id :
        Modify the command to pass the task_id to the spider
    task_data : dict
        Insert the initial task data into the tasks_collection.
    Returns:
        task_id (str): The task's id.
    """
    try:

        task_data = TaskData(
            spider_id=spider_id,
            status="running",
            start_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            end_time=None,
            log="",
        )
        result = tasks_collection.insert_one(task_data._asdict())
        task_id_str = str(result.inserted_id)

        cmd_with_task_id = cmd + f" -a task_id={task_id_str} -a spider_id={spider_id}"

        # Start the spider process
        process = subprocess.Popen(cmd_with_task_id.split(),
                                   cwd=spiders_dir,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        process_id = process.pid

        # Update the task with the process_id
        tasks_collection.update_one(
            {"_id": ObjectId(task_id_str)},
            {"$set": {"process_id": process_id}}
        )

        return task_id_str
    except Exception as e:
        raise RuntimeError(f"Error starting spider: {str(e)}") from e


def stop_spider_task(task_id):
    """
    Function to stop a Scrapy spider task. Stops a running spider task by updating
    its status in the MongoDB collection and terminating the associated process.

    Args:
        task_id (str): The unique identifier of the spider task to be stopped.

    Returns:
        bool: True if the task was successfully stopped or was already stopped,
        False if the task was not found or could not be stopped.
    """
    try:
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            return False

        # Check if the task is already completed
        if task["status"] == "completed":
            return {"message": constants.TASK_ALREADY_COMPLETED}

        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {
                "status": "stopped",
                "end_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }}
        )

        if result.modified_count > 0:
            try:
                process = psutil.Process(task["process_id"])
                process.terminate()
            except psutil.NoSuchProcess:
                # Process already terminated
                pass

            return {"message": constants.SPIDER_STOPPED_SUCCESSFULLY}
        else:
            return False
    except Exception as e:
        raise RuntimeError(f"Error stopping spider task: {str(e)}") from e
