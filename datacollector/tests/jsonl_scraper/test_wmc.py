""" Test Case WMC Organization News """
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.wmc import WMCSpider

wmc_spider = WMCSpider()

def test_parse_data_wmc():
    """
    Test the `parse_data` method of the `WMCSpider` spider.

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
        "category": "\n\t\t\t\t,ព័ត៌មានក្នុងប្រទេស,\t\t\t\t",
        "title": "ជាស្រ្តីតែកញ្ញា ឈិន ពុធដាលីចាប់អារម្មណ៍បើកអាជីវកម្មក្លឹបហាត់ប្រាណ និងគុនខ្មែរ",
        "content": (
            "រូបភាព៖ វត្តី  (កញ្ញា ឈិន ពុធដាលី) ភ្នំពេញ៖ កញ្ញា ឈិន ពុធដាលី "
            "ម្ចាស់អាជីវកម្មក្លឹបហាត់ប្រាណ និងគុនខ្មែរបែបសុខភាព ត្រូវបានស្ថានទូតអាមេរិកប្រចាំកម្ពុជាជ្រើសរើសជាសិក្ខាកាមមួយរូបក្នុងចំណោម៣០រូប "
            "ចូលរួមក្នុងវគ្គបណ្តុះបណ្តាលជំនាញអាជីវកម្មដល់សហគ្រិនស្ត្រី ហៅថា Academy of Women Entrepreneurs (AWE) រយៈពេល៩ខែ "
            "ដែលគម្រោងនេះផ្តល់ការកសាងសមត្ថភាពស្រ្តីដើម្បីធ្វើឱ្យអាជីវកម្មដែលដឹកនាំដោយស្រ្តីមានភាពរីកចម្រើន។ អ្នកស្រីវ៉ាយ វត្តីជូនសេចក្តីរាយការណ៍«មនុស្សប្រុសអាចដឹកនាំអាជីវកម្ម "
            "មនុស្សស្រីរឹតតែអាចដឹកនាំអាជីវកម្មដូចគ្នា ឬក៏បានល្អជាងបុរសថែមទៀត ជាពិសេសនៅគ្រប់វិស័យទាំងអស់ មនុស្សស្រីសុទ្ធតែអាចដើរតួនាទីធំនៅក្នុងការដឹកនាំគ្រួសារ អាជីវកម្ម និងសង្គមជាតិ!»នេះជាការលើកឡើងរបស់កញ្ញា "
            "ឈិន ពុធដាលី ម្ចាស់អាជីវកម្មក្លិបហាត់ប្រាណ និងគុនខ្មែរបែបសុខភាព Cambodian Top Team។ កញ្ញាត្រូវបានជ្រើសរើសជាសិក្ខាកាម រួមចូលក្នុងវគ្គបណ្តុះបណ្តាលជំនាញអាជីវកម្មដល់សហគ្រិនស្ត្រី ហៅថា Academy of Women Entrepreneurs (AWE) រយៈពេល៩ខែ ដែលរៀបចំដោយស្ថានទូតអាមេរិកប្រចាំកម្ពុជា។កញ្ញា ឈិន ពុធដាលី "
            "បានបញ្ជាក់ប្រាប់វិទ្យុស្ត្រីថា មូលហេតុដែលកញ្ញាបើកអាជីវកម្មក្លឹបហាត់ប្រាណ ប្រដាល់គុនខ្មែរបែបសុខភាពនេះ ដោយសារយល់ថា គុនខ្មែរជួយបានទាំងសុខភាព រាងកាយ ប្រាជ្ញា ធ្វើឱ្យគេងលក់ស្រួល រាងកាយមាំមួន និងអាចការពារខ្លួនឯងពេលមានអ្នកយាយី បានទៀតផង។ បច្ចុប្បន្នអាជីវកម្មរបស់កញ្ញា ដំណើរការល្អ ""និងមានទាំងភ្ញៀវជាតិនិងអន្តរជាតិ ចូលមកហាត់គុនខ្មែរដើម្បីសុខភាព។ ថ្វីបើមានដំណើរការល្អពិតមែន តែកញ្ញា នៅតែមកចូលរួមពង្រឹងសមត្ថភាពបន្ថែមក្នុងវគ្គបណ្តុះបណ្តាលជំនាញអាជីវកម្មដល់សហគ្រិនស្ត្រី (AWE)របស់ស្ថានទូតអាមេរិកនេះ ដោយសារតែកញ្ញាយល់ថា គ្រប់អាជីវកម្មទាំងអស់ត្រូវតែរៀនសូត្របន្ថែម នូវចំណេះដឹង "
            "ជំនាញរឹង ជំនាញទន់ ទាំងផ្នែកទីផ្សារឌីជីថល ផ្នែកគ្រប់គ្រងហិរញ្ញវត្ថុ គ្រប់គ្រងធនធានមនុស្ស ជាពិសេសការគ្រប់គ្រងបុគ្គលិករបស់កញ្ញាផ្ទាល់តែម្តង។ កញ្ញា ឈិន ពុធដាលី ៖ «អ្វីទាំងអស់ហ្នឹង ខ្ញុំគិតថា សហគ្រិនស្រ្តី និងម្ចាស់អាជីវកម្មទាំងអស់ ត្រូវការបន្ថែម ហើយខ្ញុំជឿជាក់ថា AWE "
            "នឹងជួយបំពេញនូវភាពខ្វះខាតឬបំពេញបន្ថែមនូវជំនាញរបស់យើងឱ្យកាន់តែល្អប្រសើរ»។កញ្ញា ឈិន ពុធដាលី សង្ឃឹមថា ក្រោយពីរៀនវគ្គបណ្តុះបណ្តាលជំនាញអាជីវកម្ម ជាមួយ AWE រួច "
            "កញ្ញានឹងអាចចេះច្រើនលើជំនាញដែលមានស្រាប់ ជាពិសេសជំនាញឌីជីថលម៉ាឃីតធីងឱ្យកាន់តែមានប្រសិទ្ធិភាពថែមទៀតសម្រាប់អាជីវកម្មរបស់កញ្ញាផ្ទាល់។ជាចុងក្រោយ កញ្ញា ឈិន ពុធដាលី ផ្តាំផ្ញើដល់បងប្អូននារីដែលមានបំណងចង់បើកអាជីវកម្ម "
            "មិនថាជាអាជីវកម្មអ្វីក៏ដោយ គឺកុំបោះបង់ខ្លួនឯង ទោះបីការចាប់ផ្តើមដំបូងវាមានភាពលំបាកបន្តិចមែន ប៉ុន្តែត្រូវចាំថា ការលំបាកនរណាក៏ជួបប្រទះដែរ គ្រាន់តែអ្នកខ្លះប្រើរយៈពេលខ្លី "
            "និងអ្នកខ្លះប្រើរយៈពេលយូរ។​ ធ្វើយ៉ាងណាកុំបោះបង់ក្តីស្រមៃខ្លួនឯង កុំភ្លេចរៀនបន្ថែម និងកុំភ្លេចអភិវឌ្ឍន៍ខ្លួនឯង៕@2023 WMC. All rights reserved. Powered by AsurRaa."),
    }

    article_url = "https://wmc.org.kh/article/120177/ជាស្រ្តីតែកញ្ញា-ឈិន-ពុធដ/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(wmc_spider.parse_data(article_response))

    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == "https://wmc.org.kh/article/120177/%E1%9E%87%E1%9E%B6%E1%9E%9F%E1%9F%92%E1%9E%9A%E1%9F%92%E1%9E%8F%E1%9E%B8%E1%9E%8F%E1%9F%82%E1%9E%80%E1%9E%89%E1%9F%92%E1%9E%89%E1%9E%B6-%E1%9E%88%E1%9E%B7%E1%9E%93-%E1%9E%96%E1%9E%BB%E1%9E%92%E1%9E%8A/"

def test_parse_wmc():
    """
    Test the `parse` method of the `WMCSpider` spider.

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
    current_url (str):
        The current category URL.
    next_page (str):
        The URL of the next page after pagination.
    """

    category_url = "https://wmc.org.kh/ព័ត៌មានជាតិ/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = wmc_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    next_page = category_response.css("nav.elementor-pagination .next::attr(href)").get()
    if next_page:
        next_page_url = category_response.urljoin(next_page)
    assert len(links) - 1 == 15
    assert links[15] == next_page_url
    assert links[15] == "https://wmc.org.kh/%e1%9e%96%e1%9f%90%e1%9e%8f%e1%9f%8c%e1%9e%98%e1%9e%b6%e1%9e%93%e1%9e%87%e1%9e%b6%e1%9e%8f%e1%9e%b7/2/"

