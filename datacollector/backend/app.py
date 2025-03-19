"""
This is flask with REST API for backend usig to handle request parsing,
respond format amking it easier to work with data formats.

get_db():
    This function is used to get the database connection and get the collections.
UPLOAD_FOLDER:
    This is the folder where the files are uploaded to.
[POST]/spider/add:
    This is the endpoint for adding the spider to the database. This function handles the creation
    of a new spider by processing a POST request to the "/spider/add" route.
[GET]/spiders:
    This is the endpoint for getting all the spiders from the database.
[POST]/spider/<spider_id>/run:
    This is the endpoint for running the spider base on the spider ID.
[POST]/task/<task_id>/stop:
    This is the endpoint for stopping the task base on the task ID.
"""
import logging
import os
from collections import namedtuple
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from spider_manager import start_spider, stop_spider_task
from db.database import get_db
from dotenv import load_dotenv
from config import constants

load_dotenv()

app = FastAPI()

db = get_db()
spiders_collection = db["spiders"]
SpiderData = namedtuple("SpiderData", [
    "name",
    "cmd",
    "domain",
    "desc",
    "file_name",
    "spiderfile_path"
])


UPLOAD_FOLDER = r"..\\url_khmer_scraping\jsonl_scraper\spiders"
app.state.UPLOAD_FOLDER = UPLOAD_FOLDER
logging.basicConfig(level=logging.INFO)


@app.get("/spiders", response_class=JSONResponse)
async def get_spiders():
    """
    This is the endpoint for getting all the spiders from the database.
    """
    spiders = list(spiders_collection.find({}, {"_id": False}))
    return JSONResponse(content=spiders)


@app.post("/spider/add", response_class=JSONResponse)
async def create_spider(
    file: UploadFile = File(...),
    name: str = Form(...),
    cmd: str = Form(...),
    domain: str = Form(...),
    desc: str = Form(...)
):
    """
    This is the endpoint for adding a new spider by processing a POST request to the '/spider
    endpoint. The request must contain the following parameters:

        - name: The name of the spider.
        - cmd: The command to run the spider.
        - domain: The domain of the spider.
        - desc: The description of the spider.
        - file_name: The spider file contiant coding for scrape specific website.

    Returns:
        A JSON response with a success message and the ID of the newly created spider,
        or an error message in case of failure.
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail=constants.NO_SELECTED_FILE)

        if not file.filename.endswith(".py"):
            raise HTTPException(status_code=400, detail=constants.INVALID_FILE_TYPE_ERROR)

        file_path = os.path.join(app.state.UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        new_spider_data = SpiderData(
            name=name,
            cmd=cmd,
            domain=domain,
            desc=desc,
            file_name=file.filename,
            spiderfile_path=file_path
        )

        result = spiders_collection.insert_one(new_spider_data._asdict())
        logging.info("Inserted spider with ID: %s", result.inserted_id)

        return JSONResponse(content={
            "message": constants.SPIDER_CREATED_SUCCESSFULLY,
            "id": str(result.inserted_id)
            }, status_code=201)

    except HTTPException as e:
        logging.error("HTTP error occurred: %s", str(e.detail))
        raise e
    except Exception as e:
        logging.error("Unexpected error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=constants.SPIDER_SAVE_ERROR) from e


@app.post("/spider/{spider_id}/run", response_class=JSONResponse)
async def run_spider(
    spider_id: str,
):
    """
    This is the endpoint for running a spider by processing a POST request to the '/spider/{
    spider_id}/run endpoint parameters spider_id to run. function performs the following steps:

        - Retrieves the spider document from the "spiders_collection" based on spider_id.
        - Checks if the spider document exists, and if not, returns a 404 Not Found response.
        - Get (cmd) from the spider document, Return 400 If the command is not found
        - Determines the project directory and the spiders directory.
        - Starts running spider task and returns a 200 with the task_id.

    Returns:
        A JSON response with a success message and the task_id of the running spider,
        or an error message in case of failure.
    """
    try:
        spider = spiders_collection.find_one({
            "_id": ObjectId(spider_id)})
        if not spider:
            logging.error("Spider not found: %s", spider_id)
            raise HTTPException(status_code=400, detail=constants.SPIDER_NOT_FOUND)

        cmd = spider.get("cmd")
        if not cmd:
            raise HTTPException(status_code=400, detail=constants.SPIDER_CMD_NOT_FOUND)

        project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        spiders_dir = os.path.join(project_dir, "url_khmer_scraping", "jsonl_scraper", "spiders")

        task_id = start_spider(spider_id, cmd, spiders_dir)
        return JSONResponse(content={"message": constants.SPIDER_RUNNING, "task_id": str(task_id)})

    except HTTPException as e:
        logging.error("HTTP error occurred: %s", str(e))
        raise e
    except Exception as e:
        logging.error("Unexpected error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=constants.SPIDER_RUNNING_ERROR) from e


@app.post("/task/{task_id}/stop", response_class=JSONResponse)
async def stop_spider(task_id: str):
    """
    This is the endpoint for stopping a spider by processing a POST
    request to the '/task/{task_id}/stop. It performs as the following steps:

        - Retrieves the spider document from the "spiders_collection" based on task_id.
        - Checks if the spider document exists, and if not, returns a 404 Not Found response
        - Stops the spider task and returns a 200 with the task_id.

    Returns:
        A JSON response with a success message and the task_id of the stopped spider,
        or an error message in case of failure.
    """
    try:
        task_status = stop_spider_task(task_id)
        if task_status["message"] == constants.TASK_ALREADY_COMPLETED:
            return JSONResponse(content=task_status)
        elif task_status["message"] == constants.SPIDER_STOPPED_SUCCESSFULLY:
            return JSONResponse(content={"message": constants.SPIDER_STOPPED_SUCCESSFULLY})
        else:
            raise HTTPException(status_code=404, detail=constants.TASK_NOT_FOUND)

    except HTTPException as e:
        logging.error("HTTP error occurred: %s", str(e))
        raise e
    except Exception as e:
        logging.error("Unexpected error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=constants.SPIDER_STOPPING_ERROR) from e

if __name__ == "__main__":
    import uvicorn
    PORT_NUMBER = os.environ.get("PORT_NUMBER", 8000)
    uvicorn.run(app, host="0.0.0.0", port=PORT_NUMBER)
