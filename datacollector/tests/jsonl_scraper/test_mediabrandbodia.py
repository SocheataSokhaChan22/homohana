"""Test Case For Media BrandBodia website"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.mediabrandbodia import MediabrandbodiaSpider

brandbodia_spider = MediabrandbodiaSpider()


def test_parse_data_brandbodia():
    """
    Test the `parse_data` method of the `MediabrandbodiaSpider` spider.

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
        "category": "ព័ត៌មានអន្តរជាតិ,របៀបរស់នៅ,សង្គម",
        "title": "អំពើហិង្សាដ៏អាក្រក់នៅប្រទេសមីយ៉ាន់ម៉ា ជំរុញឱ្យជនជាតិរ៉ូហ៊ីងយ៉ារាប់ពាន់នាក់បានភៀសខ្លួនទៅកាន់ប្រទេសបង់ក្លាដែស ខណៈដែលបង់ក្លាដែសស្រែកថាលែងមានលទ្ធភាពផ្ដល់ជម្រកទៀតហើយ",
        "content": (
            "ជនមូស្លីមរ៉ូហ៊ីងយ៉ាប្រហែល ៨ ០០០ នាក់បានភៀសខ្លួនទៅកាន់ប្រទេសបង់ក្លាដែសក្នុងរយៈពេលប៉ុន្មានខែថ្មីៗនេះ "
            "ដោយបានរត់គេចពីអំពើហឹង្សាកាន់តែខ្លាំងឡើងនៅក្នុងរដ្ឋរ៉ាឃីនភាគខាងលិចនៃប្រទេសមីយ៉ាន់ម៉ា នេះបើយោងតាមមន្ត្រីបង់ក្លាដែស។អំពើហឹង្សាបានកាន់តែខ្លាំងឡើង "
            "នៅពេលដែលការប្រយុទ្ធគ្នារវាងរបបយោធាដែលកំពុងកាន់អំណាចរបស់ប្រទេសមីយ៉ាន់ម៉ា និងកងទ័ពអារ៉ាកាន ដែលជាកងជីវពលជនជាតិភាគតិចដ៏មានឥទ្ធិពលដែលទាញចេញពីពុទ្ធសាសនិកភាគច្រើននៅតែបន្តកាន់តែអាក្រក់ទៅៗ។លោក Mohammad ""Shamsud Douza មន្ត្រីជាន់ខ្ពស់ទទួលបន្ទុកជនភៀសខ្លួនសម្រាប់រដ្ឋាភិបាលបង់ក្លាដែសបាននិយាយថា “យើងមានព័ត៌មានថាជនជាតិរ៉ូហ៊ីងយ៉ាប្រហែល ៨,០០០ នាក់បានឆ្លងចូលទៅក្នុងប្រទេសបង់ក្លាដែសនាពេលថ្មីៗនេះ "
            "ដែលភាគច្រើនក្នុងរយៈពេលពីរខែចុងក្រោយនេះ”។ លោកបានបន្តថា “ប្រទេសបង់ក្លាដែសមានបន្ទុកលើសហើយមិនអាចផ្ទុកជនជាតិរ៉ូហ៊ីងយ៉ាបានទៀតទេ” ។រដ្ឋមន្ត្រីការបរទេសបង់ក្លាដែស លោក Mohammad Touhid Hossain បានប្រាប់អ្នកយកព័ត៌មានកាលពីយប់ថ្ងៃទី៣ ខែកញ្ញា ថា រដ្ឋាភិបាលនឹងរៀបចំ "
            "“ការពិភាក្សាដ៏ធ្ងន់ធ្ងរមួយនៅគណៈរដ្ឋមន្ត្រី” ក្នុងរយៈពេលពីរទៅបីថ្ងៃខាងមុខ ដើម្បីដោះស្រាយវិបត្តិនេះ។ខណៈពេលដែលសម្តែងការអាណិតអាសូរចំពោះជនជាតិរ៉ូហ៊ីងយ៉ា លោក Hossain បាននិយាយថា "
            "ប្រទេសនេះលែងមានលទ្ធភាពផ្តល់ជម្រកមនុស្សធម៌ដល់ជនភៀសខ្លួនបន្ថែមទៀតហើយ។ជនភៀសខ្លួនរ៉ូហ៊ីងយ៉ារាប់ម៉ឺននាក់នៅក្នុងប្រទេសបង់ក្លាដែសបានប្រមូលផ្តុំគ្នានៅក្នុងជំរុំកាលពីថ្ងៃទី២៥ ខែសីហា ជាការប្រារព្ធខួបលើកទី ៧ "
            "នៃការបង្រ្កាបដោយយោធាឆ្នាំ២០១៧ ដែលបានបង្ខំឱ្យពួកគេភៀសខ្លួនចេញពីប្រទេសមីយ៉ាន់ម៉ា ដោយទាមទារឱ្យបញ្ចប់អំពើហិង្សា "
            "និងការវិលត្រឡប់ទៅកាន់ស្រុកកំណើតរបស់ពួកគេវិញដោយសុវត្ថិភាព។បច្ចុប្បន្នជនជាតិរ៉ូហ៊ីងយ៉ាជាងមួយលាននាក់រស់នៅក្នុងជំរុំចង្អៀតនៅភាគខាងត្បូងប្រទេសបង់ក្លាដែស "
            "ដោយមានក្តីសង្ឃឹមតិចតួចក្នុងការត្រឡប់ទៅប្រទេសមីយ៉ាន់ម៉ា ជាកន្លែងដែលពួកគេភាគច្រើនត្រូវបានបដិសេធពីភាពជាពលរដ្ឋ "
            "និងសិទ្ធិជាមូលដ្ឋានផ្សេងទៀត។ការកើនឡើងនៃអំពើហិង្សានាពេលថ្មីៗនេះ គឺជារឿងដ៏អាក្រក់បំផុតដែលជនជាតិរ៉ូហ៊ីងយ៉ាបានជួបប្រទះចាប់តាំងពីយុទ្ធនាការដឹកនាំដោយយោធាមីយ៉ាន់ម៉ាឆ្នាំ២០១៧ ដែលអង្គការសហប្រជាជាតិបានពិពណ៌នាថាមានចេតនាប្រល័យពូជសាសន៍។ប្រភព៖ The straits times")
        }

    article_url = "https://media.brandbodia.com/article/15502/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(brandbodia_spider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_brandbodia():
    """
    Test the `parse` method of the `MediabrandbodiaSpider` spider.

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

    category_url = "https://media.brandbodia.com/article/category/ព័ត៌មានទូទៅ/របៀបរស់នៅ/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = brandbodia_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    next_page = category_response.css("div.nav-links .next::attr(href)").get()
    assert len(links) - 1 == 9
    assert links[9] == next_page