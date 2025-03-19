"""Test Case For Pkasla website"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.pkalsa import PkaslaSpider

pkasla_spider = PkaslaSpider()


def test_parse_data_pkasla():
    """
    Test the `parse_data` method of the `PkaslaSpider` spider.

    This test checks the following:
    - The category of the article is not empty
    - The title of the article is not empty.
    - The content of the article is not an empty dictionary.
    - The URL of the article is not an empty dictionary.

    Attributes:
    ----------
    article_url (str):
        The URL of the article to be tested.
    article (Response):
        The HTTP response object for the article URL.
    article_response (HtmlResponse):
        The response object to be passed to the spider's `parse_data` method.
    article_result (list):
        The result returned by the spider's `parse_data` method.
    expected_value: dict
        Expected result of the parsed data.
    """
    expected_value = {
        "category": "វប្បធម៌-សិល្បៈ,កសិកម្ម-ទេសចរណ៍,បច្ចេកវិទ្យា,សង្គម-ជីវិត,អចលនទ្រព្យ",
        "title": "ក្រុមហ៊ុន វឌ្ឍនៈ គ្រុប ចូលរួមប្រារព្ធពិធីទូងស្គរអបអរសាទរការបើកការដ្ឋាន«ព្រែកជីកហ្វូណនតេជោ» ជាមួយរាជរដ្ឋាភិបាល និងប្រជាជនខ្មែរទូទាំងប្រទេស ប្រកបដោយក្តីរំភើបរីករាយ",
        "content": ("នៅថ្ងៃទី០៥ ខែសីហា ឆ្នាំ២០២៤ អ្នកឧកញ៉ា សំ អាង និងអ្នកឧកញ៉ា ឈុន លាង សហស្ថាបនិក​ក្រុមហ៊ុន "
                    "វឌ្ឍនៈ គ្រុប និងអ្នកឧកញ៉ា សំអាង វឌ្ឍនៈ អគ្គនាយកក្រុមហ៊ុន វឌ្ឍនៈ ប្រ៊ូវើរី ដឹកនាំបុគ្គលិកគ្រប់ជាន់ថ្នាក់ សិល្បៈករ សិល្បៈការីនី និងកីឡាករគុនខ្មែរ "
                    "ចូលរួមប្រារព្ធពិធីទូងស្គរអបអរសាទរការបើកការដ្ឋាន«ព្រែកជីកហ្វូណនតេជោ» ជាមួយរាជរដ្ឋាភិបាល និងប្រជាជនខ្មែរទូទាំងប្រទេស ប្រកបដោយក្តីរំភើបរីករាយ ក្រោមផ្ទៃមេឃដ៏អំណោយផល និងត្រជាក់ត្រជុំ "
                    "នាថ្ងៃទី៥ ខែសីហា ឆ្នាំ២០២៤ វេលាម៉ោង ៩ និង ៩នាទីព្រឹក នៅពីមុខអគារពាណិជ្ជកម្មដ៏ខ្ពស់ស្កឹមស្កៃ វឌ្ឍនៈ កាពីតាល។នេះជាជោគជ័យដ៏ត្រចះត្រចង់នៃ "
                    "ការលេចឡើងនូវសមិទ្ធផលជាប្រវត្តិសាស្រ្តថ្មី ចំថ្ងៃចម្រើនអាយុវឌ្ឍនៈមង្គលរបស់សម្តេចតេជោ។ក្រុមហ៊ុន វឌ្ឍនៈ គ្រុប សូមគោរពជូនពរ សម្តេចតេជោ "
                    "ប្រធានក្រុមឧត្តមប្រឹក្សាផ្ទាល់ព្រះមហាក្សត្រ និងជាប្រធានព្រឹទ្ធសភាព និងសម្តេចកិត្តិព្រឹទ្ធបណ្ឌិត ព្រមទាំងក្រុមគ្រួសារជាទីស្រលាញ់ "
                    "សូមបានសមប្រកបដោយសុខភាពល្អបរិបូរណ៍ អាយុយឺនយូរដើម្បីនៅជាម្លប់ដ៏ត្រជាក់សម្រាប់យើងខ្ញុំទាំងអស់គ្នា "
                    "និងសូមប្រកបដោយសុភមង្គលក្នុងក្រុមគ្រួសារ និងជោគជ័យគ្រប់ប្រការជានិច្ចនិរន្តរ៍។")
        }


    article_url = "https://www.pkaslatv.com/vathan-group-f/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(pkasla_spider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_pkasla():
    """
    Test the `parse` method of the `PkaslaSpider` spider.

    This test performs the following checks:
    - Extracts all article URLs from the category page.
    - Tests the pagination by verifying that the last URL corresponds to the next page.
    - Ensures that the generated next page URL is correct.

    Attributes:
    ----------
    category_url (str):
        The URL of the category page to be tested.
    category (Response):
        The HTTP response object for the category URL.
    category_response (HtmlResponse):
        The response object to be passed to the spider's `parse` method.
    category_result (list):
        The result returned by the spider's `parse` method.
    links (list):
        A list of URLs extracted from the category page.
    next_page (str):
        The URL of the next page after pagination.
    """

    category_url = "https://www.pkaslatv.com/category/វប្បធម៌-សិល្បៈ/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = pkasla_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    next_page = category_response.css(".penci-pagination .page-numbers a.next::attr(href)").get()
    if next_page:
        next_page_url = category_response.urljoin(next_page)
    assert len(links) - 1 == 10
    assert links[10] == next_page_url
    assert links[10] == "https://www.pkaslatv.com/category/%E1%9E%9C%E1%9E%94%E1%9F%92%E1%9E%94%E1%9E%92%E1%9E%98%E1%9F%8C-%E1%9E%9F%E1%9E%B7%E1%9E%9B%E1%9F%92%E1%9E%94%E1%9F%88/page/2/"

