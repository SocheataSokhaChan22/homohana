import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.cambonomist import CambonomistSpider
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle

cambonomist_spider = CambonomistSpider()
pagination_handle = PaginationHandle()


def test_parse_data_cambonomist():
    """
    Test the `parse_data` method of the `CambonomistSpider` spider.

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
    expected_value (dict):
        Expected result of the parsed data.
    """
    expected_value = {
        "category": "ពន្ធដារលើកទឹកចិត្តវិស័យកសិកម្មទាំងស្រុង",
        "title": "ពន្ធដារ ចាត់ទុកវិស័យកសិកម្ម ជាវិស័យអាទិភាពដែលបានលើកទឹកចិត្តផ្នែកពន្ធដារ",
        "content": [
            "អគ្គនាយកដ្ឋានពន្ធដារបានអះអាងថា វិស័យកសិកម្ម នៅតែទទួលបានការលើកទឹកចិត្តផ្នែកពន្ធដារ និងបានច្រានចោលការលើកឡើងថា ការធ្លាក់ថ្លៃនៃផលិតផលកសិកម្ម បណ្ដាលមកពីការយកពន្ធ គឺពុំបានឆ្លុះបញ្ចាំងពីការពិត និងកិច្ចខិតខំប្រឹងប្រែងរបស់រាជរដ្ឋាភិបាល ក្នុងការជួយជ្រោមជ្រែង "
            "វិស័យកសិកម្មឡើយ។", "អគ្គនាយកដ្ឋានពន្ធដារបានចេញមកច្រាលចោលចំពោះការលើកឡើងដែលថាការធ្លាក់ចុះតម្លៃកសិផលរបស់កសិករនៅកម្ពុជា គឺបណ្តាលមកពីការយកពន្ធរបស់អគ្គនាយកដ្ឋានពន្ធដារ។ សម្រាប់អគ្គនាយកដ្ឋានពន្ធដារ ការចោទប្រកាន់បែបនេះ "
            "គឺមិនបានឆ្លុះបញ្ចាំងពីការពិតនោះទេ ពោលគឺវាជាការចោទប្រកាន់ ដែលគ្មានមូលដ្ឋានច្បាស់លាស់ និងមិនបានឆ្លុះបញ្ចាំងពីកិច្ចខិតខំប្រឹងប្រែងរបស់រាជរដ្ឋាភិបាល និងក្រសួងស្ថាប័នពាក់ព័ន្ធ។", "ឯកឧត្តម "
            "គង់ វិបុល រដ្ឋមន្ត្រីប្រតិភូអមនាយករដ្ឋមន្ត្រី និងជាអគ្គនាយកនៃអគ្គនាយកដ្ឋានពន្ធដារបានគូសបញ្ជាក់ថា "
            "កន្លងមករាជរដ្ឋាភិបាលតែងតែមានការគិតគូរ និងយកចិត្តទុកដាក់ខ្ពស់ ព្រមទាំងចាត់ទុកវិស័យកសិកម្ម គឺជាវិស័យអាទិភាព។ រាជរដ្ឋាភិបាលបានដាក់ចេញជាបន្តបន្ទាប់នូវវិធានការលើកទឹកចិត្តលើផ្នែកផ្សេងៗ "
            "និងជាពិសេសបានផ្ដល់ការលើកទឹកចិត្តផ្នែកពន្ធដារ ចំពោះវិស័យកសិកម្មទាំងស្រុង។ ដូច្នេះការលើកឡើងថា ការធ្លាក់ថ្លៃនៃផលិតផល កសិកម្មបណ្ដាលមកពីការយកពន្ធ ពុំឆ្លុះបញ្ចាំងពីការពិត និងកិច្ចខិតខំប្រឹងប្រែងរបស់រាជរដ្ឋាភិបាលក្នុងការជួយជ្រោមជ្រែង "
            "វិស័យកសិកម្មឡើយ។", "អគ្គនាយកដ្ឋានពន្ធដារពិនិត្យឃើញ ថាក្នុងចំណោមការលើកឡើងទាំងនោះ "
            "មួយចំនួនលើកឡើងក្នុងន័យបង្កាច់បង្ហូចកិច្ចខិតខំប្រឹងប្រែងរបស់រាជរដ្ឋាភិបាល នីតិកាលថ្មីពីសំណាក់ក្រុមប្រឆាំង, "
            "មួយចំនួនផ្សព្វផ្សាយក្រោមចេតនាធ្វើឱ្យមានការភាន់ច្រឡំដើម្បីប្រយោជន៍ផ្ទាល់ខ្លួន, "
            "មួយចំនួនលើកឡើងដោយការភាន់ច្រឡំហើយផ្សព្វផ្សាយបន្តគ្នា និងមួយចំនួនទៀតលើកឡើងក្នុងគោលដៅទាក់ទាញ អ្នកទស្សនា។", "សូមបញ្ជាក់ថា រាជរដ្ឋាភិបាលកម្ពុជាបានដាក់ចេញនូវវិធានការលើកទឹកចិត្តដល់វិស័យកសិកម្ម "
            "រួមមានការលើកទឹកចិត្តពន្ធបន្ថែមចំពោះការដាំដុះស្រូវ ការប្រមូលទិញស្រូវ និងការផលិតអង្ករនាំចេញ, ការចាត់ទុកជាបន្ទុករបស់រដ្ឋនូវអាករលើតម្លៃបន្ថែមលើការនាំចូល និងផ្គត់ផ្គង់ទំនិញក្នុងវិស័យកសិកម្ម, "
            "ការអនុគ្រោះអាករលើតម្លៃបន្ថែមចំពោះអ្នកចុះកិច្ចសន្យាផ្គត់ផ្គង់អង្ករសម្រាប់បម្រើការនាំចេញអង្ករ, ការលើកទឹកចិត្តផ្នែកពន្ធដារដល់សហគ្រាសធុនតូច និងមធ្យមក្នុងវិស័យអាទិភាព "
            "និងការលើកទឹកចិត្តផ្នែកពន្ធដារចំពោះការផ្គត់ផ្គង់ផលិតផលកសិកម្មមិនទាន់កែច្នៃជាដើម៕", "អត្ថបទ ៖ បូ ដូឡា"]
    }

    article_url = "https://cambonomist.com/articles/taxes-encourage-the-whole-agricultural-sector/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(cambonomist_spider.parse_data(article_response))

    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_cambonomist():
    """
    Test the `parse` method of the `CambonomistSpider` spider.

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

    category_url = "https://cambonomist.com/articles/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = cambonomist_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    current_url = category_response.url
    next_page = pagination_handle.get_next_page_url_with_param(current_url)
    assert len(links) - 1 == 10
    assert links[10] == next_page
    assert links[10] == "https://cambonomist.com/articles/?page=2"

