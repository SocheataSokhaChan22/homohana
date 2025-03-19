"""Test Case For Karpit Website"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.karpit import KarpitSpider

karpit_spider = KarpitSpider()

def test_parse_karpit():
    """
    Test of `parse` method of the KarpitSpider.
    
    This test checks the following:
    - The title of the article is not empty.
    - The content of the article is not an empty dictionary.
    - The URL of the article is not an empty dictionary.

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
    category_url = "https://www.karpit.news/category/opinion"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = karpit_spider.parse(category_response)

    """
    testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    next_page = category_response.css(".nav-links .next::attr(href)").get()
    category = category_response.css(".post-categories a::text").get()
    
    assert category == "ទស្សនៈ"
    assert len(links) - 1 == 10
    assert links[10] == next_page
    assert links[10] == "https://www.karpit.news/category/opinion/page/2"

def test_parse_data_karpit():
    """
    This function is used to test the parse data method of KarpitSpider.
    This checks to see if the filtering works correctly.
    This test is conducted using live data from the website.

    Note: The filtering mainly focuses on the URL.

    Attribute
    ---------
    article_response:
        live response generated from article url
    category:
        live response generated from category url
    article_result:
        list of article urls generated from article response
    article: dict
        desired output (should be parsed)
    expected_value: dict
        Expected result of the parsed data.
    """
    expected_value = {
        "category": "ទស្សនៈ",
        "title": "ផ្តាំទៅលោក គឹម សុខ «សុខ ត្រូវចាំថា ឆ្កែដែលខាំគេមិនរើសមុខ គេហៅថា ឆ្កែឆ្កួត!»",
        "content": ["ជាដំបូង ខ្ញុំសុំការអធ្យាស្រ័យពីបងបងប្អូនខ្មែរទាំងក្នុង និងក្រៅប្រទេសដែលខ្ញុំប្រើប្រាស់ពាក្យពេជន៍អសុរោះ និងធ្ងន់ៗបែបនេះ។ នេះ "
                    "គឺដោយសារតែខ្ញុំមិនអាចរកពាក្យពេជន៍ឯណាដែលល្អជាងនេះទេសម្រាប់ប្រៀបប្រដូចអ្នកវិភាគចេះគ្រប់រឿង គឹម សុខ នេះ។ "
                    "អ្នកវិភាគរូបនេះ អាក្រក់អាក្រី ជូរជាតិរកអ្នកណាប្រៀបផ្ទឹមមិនបាន ខ្លួននៅឯជើងមេឃឯណោះ តែធ្វើដូចដឹងច្បាស់ណាស់រឿងនៅក្នុងប្រទេស ដឹងជាងខ្ញុំនៅក្នុងស្រុកឯណេះទៅទៀត។ ", "នៅថ្ងៃនេះ "
                    "ក្រុមអ្នកនាំពាក្យនាយករដ្ឋមន្រ្តីកម្ពុជា បានចេញមកទាត់ចោលហើយនូវការចោទប្រកាន់ទាំងងងើលរបស់អ្នកវិភាគក្បាលទំពែករូបនេះលើលោកជំទាវ ពេជ ចន្ទមុន្នី "
                    "ភរិយារបស់សម្តេចធិបតី ហ៊ុន ម៉ាណែត ថា បានជាប់ពាក់ព័ន្ធនឹងក្រុមហ៊ុន CIC ក្រោយលោក គុយ វ៉ាត ទើបត្រូវបានចាប់ខ្លួន។ ខ្ញុំគិតថា ប្រជាពលរដ្ឋខ្មែរទាំងក្នុង និងក្រៅប្រទេស រួមទាំងរូបខ្ញុំផង "
                    "សុទ្ធតែបានដឹងហើយថា លោកជំទាវ ជាមនុស្សស្លូតបូត សុភាពរាបសារ មិនពាក់ព័ន្ធនឹងរឿងរកស៊ី និងមិនជាប់ពាក់ព័ន្ធក្នុងបញ្ហានយោបាយឡើយ។ អ្វីដែលលោកជំទាវបានធ្វើ និងកំពុងធ្វើ គឺក្នុងគោលបំណង "
                    "ដើម្បីប្រជាជនកម្ពុជាទាំងអស់។ តើអ្នកវិភាគចោលម្សៀតនេះ យកស្អីមកគិត ទើបបានចោទប្រកាន់លោកជំទាវខុសពីការពិតយ៉ាងនេះ? ", "ក្នុងនាមជាប្រជាពលរដ្ឋម្នាក់ "
                    "ខ្ញុំពិតជាឈឺចាប់ណាស់ដែលកម្ពុជាដ៏ផូរផង់របស់យើងមានមនុស្សថោកទាបដូចលោក គឹម សុខ នេះ។ ពូជពង្សខ្មែរយើងល្អណាស់តាំងពីដូនតាមក ប៉ុន្តែ បែរជាប់ឈាមមនុស្សអាក្រក់ ចិត្តសាហាវ ឃោរឃៅបែបនេះ "
                    "និយាយឱ្យខ្លីទៅ លោក គឹម សុខ មិនសមកើតជាកូនខ្មែរសោះ ព្រោះកូនខ្មែរ គ្មានភាពអាក្រក់ជួរជាតិក្នុងខ្លួនដូចលោកឯងឡើយ។ ដើម្បីតែបានជ្រកប្រទេសគេបន្តទៀត ដើម្បីតែបានលុយចិញ្ចឹមខ្លួន "
                    "សុខចិត្តធ្វើគ្រប់យ៉ាង តើលោកឯងស័ក្តិសមជាមនុស្សទេ? លោកមិនចេះខ្មាសគេទេឬ? ", "លោកមើលទៅប្រហែលជាមានអាយុមិនច្រើនជាងខ្ញុំទេ អ៉ីចឹង យើងអាចនិយាយស្មើគ្នាបាន។ គឹម សុខ "
                    "ក្នុងនាមជាខ្មែរដូចគ្នា ខ្ញុំសូមផ្តាំទៅ គឺម សុខ ឯងថា គួរភ្ញាក់រឮកហើយ មុននិយាយអ្វី ឬធ្វើអ្វី សូមយកខួរមកគិតផង ចេះស្រឡាញ់ជាតិផង កុំចូលចិត្តបំផ្លាញជាតិឯងពេក។ ខ្ញុំក៏សូមប្រាប់ទៅ គឹម សុខ ឯងផងដែរថា "
                    "សុខហា! ឆ្កែ បើខាំគេមិនរើសមុខទេ គេហៅឆ្កែនោះថា ជាឆ្កែឆ្កួត ហើយខ្ញុំសង្ឃឹមថា សុខឯង មិនស្ថិតក្នុងទម្រង់បែបនេះទៅចុះ៕ ", "(ពីពលរដ្ឋម្នាក់នៅក្នុងខេត្តកំពង់ចាម)"
                    ],
        }


    article_url = "https://www.karpit.news/opinion/28176"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")
    category = "ទស្សនៈ"
    article = next(karpit_spider.parse_data(article_response, category))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url