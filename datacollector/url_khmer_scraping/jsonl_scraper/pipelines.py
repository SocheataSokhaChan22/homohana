"""
This file is to handle the storage of scraped data into MongoDB
while managing related data, tasks and metadata.
"""
from datetime import datetime
import pymongo
from bson import ObjectId
from jsonl_format.jsonl_formatter import get_metadata, get_content, get_warc_headers


class MongoDBPipeline:
    """
    MongoDBPipeline: Pipeline for storing scraped data into MongoDB.

    Attributes:
        data_collections (str): Name of the collection for storing scraped data.
        tasks_collection (str): Name of the collection for storing task-related information.
        metadata_collection (str): Name of the collection for storing metadata.
    """
    data_collections = "data"
    tasks_collection = "tasks"
    metadata_collection = "metadata"

    def __init__(self, mongo_uri, mongo_db):
        """
        Initializes the MongoDBPipeline with the MongoDB connection URI and database name.

        Initialize the MongoDBPipeline class.
            - param mongo_uri: URI for connecting to MongoDB.
            - param mongo_db: Name of the database to connect to.
        """
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.database = None
        self.task_id = None
        self.spider_id = None
        self.start_time = None

    @classmethod
    def from_crawler(cls, crawler):
        """
        Initializes the MongoDBPipeline with the MongoDB connection URI and database name.
        """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items")
        )

    def open_spider(self, spider):
        """
        Opens the MongoDB connection and initializes necessary
        configurations when the spider starts.

            Args:
                spider (scrapy.Spider): The Scrapy spider instance.

            Behavior:
                - Establishes a connection to MongoDB using the provided URI.
                - Sets up the database and initializes necessary collections.
                - Creates a unique index on the "url_ref_id" field in the metadata collection.
                - If a "task_id" is provided in the spider, updates
                the corresponding task status in the tasks collection to "running".
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.database = self.client[self.mongo_db]
        self.database[self.data_collections].create_index(
            [("url", pymongo.ASCENDING), ("spider_id", pymongo.ASCENDING)],
            unique=True
        )
        self.database[self.metadata_collection].create_index("url_ref_id", unique=True)

        self.task_id = getattr(spider, "task_id", None)
        self.spider_id = getattr(spider, "spider_id", None)
        if self.task_id:
            self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.database[self.tasks_collection].update_one(
                {"_id": ObjectId(self.task_id)},
                {"$set": {
                    "status": "running",
                    "start_time": self.start_time,
                }},
                upsert=True
            )

    def close_spider(self, spider):  # pylint: disable=unused-argument
        """
        Called when the spider closes. Updates task status to "completed in MongoDB.
        """
        if self.task_id:
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.database[self.tasks_collection].update_one(
                {"_id": ObjectId(self.task_id)},
                {"$set": {
                    "status": "completed",
                    "end_time": end_time
                }}
            )
        self.client.close()

    def process_item(self, item, spider):   # pylint: disable=unused-argument
        """
        Processes a scraped item and stores it in MongoDB, along with associated metadata.

        Args:
            item (dict): The scraped item to process.
            spider (scrapy.Spider): The Scrapy spider instance.

        Returns:
            dict: The processed item dictionary.

        Behavior:
            - Checks if an item with the same URL and spider
            ID already exists in the "data" collection.
            Raises a DropItem exception if a duplicate is found.
            - Retrieves content, metadata, and WARCs headers associated with the item's URL.
            - Inserts the item into the "data" collection in MongoDB.
            - If a "task_id" is provided, updates the corresponding
            task document in the "tasks" collection.
        """
        # Insert the new item into the data collection
        item_dict = dict(item)
        item_dict["spider_id"] = self.spider_id
        item_dict["task_id"] = self.task_id
        self.database[self.data_collections].insert_one(item_dict)

        content_html = get_content(item["url"])
        meta_data = get_metadata(content_html)
        warc_headers = get_warc_headers(item["url"])

        metadata = {
            "url_ref_id": item_dict.get("url"),
            "metadata": meta_data,
            "warc_headers": warc_headers
        }

        self.database[self.metadata_collection].update_one(
            {"url_ref_id": metadata["url_ref_id"]},
            {"$set": metadata},
            upsert=True
        )
        return item
