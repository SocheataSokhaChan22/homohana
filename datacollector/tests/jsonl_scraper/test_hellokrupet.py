""" Test Case Hello Krupet """
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.hellokrupet import HelloKrupetSpider

hellokrupetSpider = HelloKrupetSpider()


def test_parse_data_hellokrupet():
    """
    Test the `parse_data` method of the `HelloKrupetSpider` spider.

    This test checks the following:
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
        "category": ["លំហាត់ប្រាណ", "លំហាត់ជំនួយបេះដូង"],
        "title": "ហាត់ប្រាណមួយថ្ងៃ ១ម៉ោង ជួយកាត់បន្ថយហានិភ័យជំងឺបេះដូង",
        "content": ("ឲ្យបានច្រើនជាប្រចាំគឺជារឿងល្អសម្រាប់សុខភាពបេះដូង "
        "ក៏ប៉ុន្ដែចំពោះអ្នកមិនសូវមានពេលវេលាគ្រប់គ្រាន់បន្ទាប់ពីបំពេញការងារ "
        "នោះគឺជារឿងដែលចាំបាច់ត្រូវស្វែងយល់ឲ្យបានច្បាស់ ថាគួរត្រូវប្រើពេលប៉ុន្មានឲ្យបានគ្រប់គ្រាន់ "
        "ក្នុងការហាត់ប្រាណនេះ។ ជាក់ស្ដែងតាមការណែរនាំរបស់ក្រុមគ្រូពេទ្យ បានបង្ហាញថា ការហាត់ប្រាណ "
        "យ៉ាងហោចក៏ត្រូវចំណាយពេល ១ម៉ោង ក្នុងមួយថ្ងៃដើម្បីធ្វើឲ្យបេះដូងមានសុខភាពល្អ។ថ្វីត្បិតតែការលើកឡើងរបស់គ្រូពេទ្យបានបង្ហាញថា "
        "ការហាត់ប្រាណបាន១ម៉ោង ក្នុងមួយថ្ងៃក៏អាចផ្ដល់អត្ថប្រយោជន៍មែនសម្រាប់សុខភាពបេះដូង ប៉ុន្ដែក៏មានចំណុច​រួម​ផ្សំ​មួយ​ចំនួន​ទៀត​ដែរ​។ ក្នុងនោះរួម​មាន​ ឥរិយាបថប្រចាំថ្ងៃ របបនៃការញ៉ាំអាហារ និង "
        "លក្ខណៈការងារ ដែលសកម្មភាពខ្លះក៏អាចរួម​ចំណែកជាការហាត់ប្រាណ ដល់រាងកាយផងដែរ។បើគិតទៅលើពេលវេលាគោល "
        "ការហាត់ប្រាណ ១ម៉ោងគឺគ្រប់គ្រាន់ធ្វើឲ្យសុខភាពល្អ នោះផ្ដោតសំខាន់លើប្រភេទ នៃការហាត់ប្រាណ ដូចជា ការរត់ ការដើរ(ចន្លោះល្បឿន៤-៥គីឡូ/១ម៉ោង)  ការរាំំ  សុទ្ធសឹងជាការហាត់ប្រាណបែបសកម្មភាពងាយៗ។ "
        "ដូច្នេះយើងអាចធ្វើឲ្យ​បានយ៉ាងហោច ១ម៉ោង ក្នុងមួយថ្ងៃ ក៏អាចជួយកាត់​​បន្ថយហានិភ័យបាន ២០-៤០%។ ការហាត់ប្រាណ ប្រភេទផ្សេងទៀតក៏​មាន​ដែរ​ ដូចជាការហាត់ប្រាណបែបកាយសម្ពន្ធ ។ ការហាត់ប្រាណប្រភេទនេះអាចធ្វើបានយ៉ាងហោចចន្លោះ "
        "៣០ ទៅ ៤០នាទី ក្នុងមួយថ្ងៃជាប្រចាំ ក៏អាចជួយដល់សុខភាពបេះដូងបានដែរ។ សកម្មភាពការងារមួយចំនួនផ្សេងទៀត ក៏អាចចាត់ទុក ថា ការហាត់ប្រាណដូចគ្នា ដូចជាការងារ ត្រូវដើរថ្មើរជើងច្រើន ប្រើកាយវិការច្រើន "
        "ពោលសកម្មភាពដែលអាចធ្វើឲ្យមានចលនា សរសៃឈាម និងបេះដូងធ្វើការសកម្មគឺជារឿងល្អសម្រាប់សុខភាព។ការសង្កត់ធ្ងន់ទៅលើកត្ដាមួយចំនួនទៀត "
        "សម្រាប់អ្នកហាត់ប្រាណដែលមានមាឌ គីឡូ វ័យ មិនសមាត្រគ្នា ពោលអ្នក​ដែលមានមាឌធាត់   គួរតែចំណាយពេល ហាត់ប្រាណឲ្យបានយ៉ាងហោចណាស់ ១ម៉ោងកន្លះ ក្នុងមួយថ្ងៃជាប្រចាំ និងត្រូវកំណត់របបអាហារត្រូវ​ញ៉ាំផងដែរ។ "
        "ការសិក្សាបញ្ជាក់​ថា​ អ្នកមានបញ្ហាលើសគីឡូច្រើន ភាគច្រើនមានអត្រាភាគរយខ្ពស់ ប្រឈមនឹងជំងឺបេះដូង ជំងឺសរសៃឈាម ដោយមិនប្រកាន់ទៅ​លើវ័យនោះទេ។[embed-health-tool-heart-rate]"),
        "url": "https://hellokrupet.com/%E1%9E%9B%E1%9F%86%E1%9E%A0%E1%9E%B6%E1%9E%8F%E1%9F%8B%E1%9E%94%E1%9F%92%E1%9E%9A%E1%9E%B6%E1%9E%8E/%E1%9E%9B%E1%9F%86%E1%9E%A0%E1%9E%B6%E1%9E%8F%E1%9F%8B%E1%9E%87%E1%9F%86%E1%9E%93%E1%9E%BD%E1%9E%99%E1%9E%94%E1%9F%81%E1%9F%87%E1%9E%8A%E1%9E%BC%E1%9E%84/167618/"
    }

    article_url = "https://hellokrupet.com/លំហាត់ប្រាណ/លំហាត់ជំនួយបេះដូង/167618/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(hellokrupetSpider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == expected_value["url"]

def test_parse_hellokrupet():
    """
    Test the `parse` method of the `HelloKrupetSpider` spider.

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

    category_url = "https://hellokrupet.com/ជំងឺមហារីក/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = hellokrupetSpider.parse(category_response)

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
    if '?' in current_url:
        base_url, query_string = current_url.split('?', 1)
        query_params = query_string.split('&')
        new_query_params = []
    
        for param in query_params:
            if param.startswith('page='):
                page_num = int(param.split('=')[1]) + 1
                new_query_params.append(f'page={page_num}')
            else:
                new_query_params.append(param)
        next_page = base_url + '?' + '&'.join(new_query_params)
    else:
        next_page = current_url + "?page=2"

    assert len(links) - 1 == 10
    assert links[10] == next_page
    assert links[10] == "https://hellokrupet.com/%E1%9E%87%E1%9F%86%E1%9E%84%E1%9E%BA%E1%9E%98%E1%9E%A0%E1%9E%B6%E1%9E%9A%E1%9E%B8%E1%9E%80/?page=2"
