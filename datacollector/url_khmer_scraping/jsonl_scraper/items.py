"""
This file defines a Scrapy Items. This item is used to
structure the data extracted by the Scrapy spider.
"""
from scrapy.item import Item, Field


class ScrapyItem(Item):
    """
    Defines a Scrapy item for storing scraped data.

    Attributes
    ----------
    category : scrapy.Field
        The category of the item.
    title : scrapy.Field
        The title of the item, typically extracted from a webpage.
    content : scrapy.Field
        The main content or body of the item, usually extracted from the text of a webpage.
    url : scrapy.Field
        The URL of the page from which the item was scraped.
    """
    category = Field()
    title = Field()
    content = Field()
    url = Field()
