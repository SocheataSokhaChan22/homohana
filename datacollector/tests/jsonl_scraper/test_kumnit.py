import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.kumnit import KumnitSpider

kumnit_spider = KumnitSpider()


def test_parse_data_kumnit():
    """
    Test the `parse_data` method of the `KumnitSpider` spider.

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
        "category": "ហិរញ្ញវត្ថុ",
        "title": "7 យ៉ាង ដើម្បីសម្រេចបានជោគជ័យផ្នែកហិរញ្ញវត្ថុ",
        "content": ("សុខភាពហរិញ្ញវត្ថុផ្ទាល់ខ្លួនគឺពិតជាសំខាន់ណាស់សម្រាប់ខ្លួនឯង គ្រួសារ និងសង្គមជាតិ។ "
        "ហេតុដូចនេះហើយ ចំណេះដឹងហរិញ្ញវត្ថុគឺជាចំណេះដឹងមួយដែលមិនខ្វះបានដើម្បីអាចកសាងទ្រព្យ គ្រប់គ្រងហានិភ័យបំណុល ប្រឡូក្នុងការវិនិយោគ។ ហេតុដូចនេះហើយ "
        "ខ្ញុំសូមណែនាំវិធីសាស្ត្រសាមញ្ញ7យ៉ាងដើម្បីធ្វើឲ្យអ្នកជោគជ័យនៅក្នុងស្ថានភាពហិរញ្ញវត្ថុរបស់អ្នក។1. កំណត់កញ្ចប់ថវិកា និងតាមដានការចំណាយ៖ ការបង្កើត និងការប្រកាន់ខ្ជាប់ការចាយតាមចំនួនកំណត់មួយ "
        "អនុញ្ញាតឱ្យអ្នកតាមដានចំណូល និងការចំណាយរបស់អ្នកបានល្អ ដែលធានាថាអ្នករស់នៅតាមស្តង់ដារលទ្ធភាពរបស់អ្នក និងអាចធ្វើការសម្រេចចិត្តផ្នែកហិរញ្ញវត្ថុប្រកបដោយការយល់ដឹង។2. ការសន្សំ និងការវិនិយោគ៖ ការសន្សំ "
        "និងការវិនិយោគជាប្រចាំពីចំណូលរបស់អ្នក នឹងជួយឲ្យអ្នកអាចកសាងទ្រព្យកាន់តែយូរកាន់តែកើនឡើង ដែលអនុញ្ញាតឱ្យអ្នកសម្រេចបាននូវគោលដៅហិរញ្ញវត្ថុ និងធានាពីអនាគតរបស់អ្នក។3. ការគ្រប់គ្រងបំណុល៖ "
        "ការកាត់បន្ថយ និងលុបបំណុល ជាពិសេសបំណុលដែលមានការប្រាក់ខ្ពស់។ បន្ថែមពីលើនេះ អ្នកអាចបង្កើនចំនួនប្រាក់សន្សំ និងការវិនិយោគឲ្យបានកាន់តែច្រើនចេញពីចំណូលការបស់អ្នក ""ដែលសកម្មភាពនេះនឹងជំរុញការរីកចម្រើនរបស់អ្នក នឹងជួយឲ្យអ្នកឆ្ពោះទៅរកសេរីភាពផ្នែកហិរញ្ញវត្ថុ។4. ការយល់ដឹងផ្នែកហិរញ្ញវត្ថុ៖ "
        "រៀនអំពីហិរញ្ញវត្ថុផ្ទាល់ខ្លួនឲ្យបានច្រើនអាចនឹងជួយឲ្យអ្នកធ្វើការសម្រេចចិត្តប្រកបដោយការយល់ដឹងអំពីការចំណាយថវិកា ការសន្សំ ការវិនិយោគ និងការគ្រប់គ្រងបំណុល។5. ការកំណត់គោលដៅ៖ ការកំណត់គោលដៅហិរញ្ញវត្ថុដែលច្បាស់លាស់ "
        "និងជាក់លាក់ ផ្តល់នូវទិសដៅ និងការលើកទឹកចិត្ត ជួយអ្នកឱ្យផ្តោតអារម្មណ៍ និងធ្វើឱ្យមានវឌ្ឍនភាពឆ្ពោះទៅរកលទ្ធផលដែលអ្នកចង់បាន។6. ការគ្រប់គ្រងហានិភ័យ៖ ការការពារខ្លួនអ្នក "
        "និងទ្រព្យសម្បត្តិរបស់អ្នក តាមរយៈការមានផែនការច្បាស់លាស់ មានការត្រៀមទុក ទិញធានារ៉ាប់រង និងប្រើយុទ្ធសាស្ត្រគ្រប់គ្រងហានិភ័យផ្សេងទៀត "
        "ដើម្បីការពារសុខុមាលភាពហិរញ្ញវត្ថុរបស់អ្នកពីព្រឹត្តិការណ៍អាចកើតឡើងដែលមិននឹកស្មានដល់។7. វិន័យ និងការអត់ធ្មត់៖ ការសម្រេចបានជោគជ័យផ្នែកហិរញ្ញវត្ថុ ទាមទារឱ្យមានវិន័យ និងការអត់ធ្មត់។ "
        "វាជាការរត់ម៉ារ៉ាតុង មិនមែនជាការរត់ប្រណាំងទេ ហើយការប្តេជ្ញាចិត្តចំពោះផែនការរបស់អ្នកក្នុងរយៈពេលយូរគឺមានសារៈសំខាន់។ "),
        }

    article_url = "https://kumnit.com/7-steps-for-personal-finance-success/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(kumnit_spider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_kumnit():
    """
    Test the `parse` method of the `KumnitSpider` spider.

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

    category_url = "https://kumnit.com/Topic/real_estate/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = kumnit_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    next_page = category_response.css(".page-nav a[aria-label='next-page']::attr(href)").get()
    if next_page:
        next_page_url = category_response.urljoin(next_page)
    assert len(links) - 1 == 10
    assert links[10] == next_page_url
    assert links[10] == "https://kumnit.com/Topic/real_estate/page/2/"

