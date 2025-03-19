"""
This file defines a Scrapy middleware to handle the prevention of processing duplicate URLs.
The middleware check for the existence of previously processed URLs with MongoDB.
If a duplicate is found, the request is ignored.
"""
import scrapy
from scrapy.utils.request import request_fingerprint
from scrapy.exceptions import IgnoreRequest
from pymongo import MongoClient


class UrlKhmerScrapingSpiderMiddleware:
    """
    Middleware to handle duplicate URLs in a Scrapy spider.

    This middleware interacts with a MongoDB database to check if a URL has already been processed.
    If a URL is found to be a duplicate, the request is ignored.

    Attributes:
    -----------
    mongo_uri : str
        The URI of the MongoDB instance.
    mongo_db : str
        The name of the MongoDB database.
    client : MongoClient
        The MongoDB client.
    database : Database
        The MongoDB database.
    data_collection : Collection
        The MongoDB collection to store and check for duplicate URLs.
    """
    def __init__(self, mongo_uri, mongo_db):
        """
        Initialize the middleware with MongoDB connection details.

        Parameters:
        -----------
        mongo_uri : str
            The URI of the MongoDB instance.
        mongo_db : str
            The name of the MongoDB database.
        """
        self.client = MongoClient(mongo_uri)
        self.database = self.client[mongo_db]
        self.data_collection = self.database["data"]

    @classmethod
    def from_crawler(cls, crawler):
        """
        Create an instance of the middleware from a Scrapy crawler.

        Parameters:
        -----------
        crawler : Crawler
            The Scrapy crawler.

        Returns:
        --------
        UrlKhmerScrapingSpiderMiddleware
            An instance of the middleware.
        """
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
        )

    def process_request(self, request, spider):  # pylint: disable=unused-argument
        """
        The process_request method is called for each request the spider makes.
        It checks if this url already exists in the MongoDB collection.
        If the URL has already been processed.

        Parameters:
        -----------
        request : Request
            The Scrapy request.
        spider : Spider
            The Scrapy spider.

        Raises:
        -------
        IgnoreRequest
            If the URL has already been processed.
        """
        if self.data_collection.find_one({"url": request.url}):
            raise IgnoreRequest("Duplicate URL found in MongoDB: %s" % request.url)

    def process_spider_output(self, response, result, spider):  # pylint: disable=unused-argument
        """
        Processes the output from the spider, filtering out duplicate requests
        and yielding items for further processing.

        Parameters
        ----------
        response : scrapy.http.Response
            The response object containing the content of the page that was processed.
        result : iterable
            An iterable of results (items and/or requests) yielded by the spider's parsing methods.
        spider : scrapy.Spider
            The spider instance that is currently running.
        Yields
        ------
        scrapy.Item
            Items to be processed by the item pipeline (e.g., stored in a database).
        scrapy.Request
            Requests that are not filtered out, to be processed further (e.g., following new links).
        Notes
        -----
        - filters out requests based on their fingerprints to avoid duplicate processing.
        - Requests with fingerprints found in the `data_collection` are skipped.
        - Items are yielded for further processing, such as saving to a database.
        """
        for item in result:
            if isinstance(item, scrapy.Request):
                fingerprint = request_fingerprint(item)
                if self.data_collection.find_one({"_id": fingerprint}):
                    continue
            yield item

    def close_spider(self, spider):  # pylint: disable=unused-argument
        """
        Close the MongoDB client when the spider is closed.

        Parameters:
        -----------
        spider : Spider
            The Scrapy spider.
        """
        self.client.close()
