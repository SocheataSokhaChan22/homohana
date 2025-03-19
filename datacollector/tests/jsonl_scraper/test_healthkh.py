"""Test Case For គេហទំព័រសុខភាព"""
import requests
from scrapy.http import HtmlResponse, Request, TextResponse
from url_khmer_scraping.jsonl_scraper.spiders.healthkh import HealthSpider
import json

healthSpider = HealthSpider()

def test_parse_health():
    """
    Test the `parse` method of HealthSpider.

    This test verifies that the correct number of article links are extracted
    from the "digestive" category page and ensures that the widget ID and post ID
    are correctly identified.

    Asserts:
        - The number of extracted links matches the expected count.
        - The widget ID matches the expected value.
        - The post ID matches the expected value.
    """
    category_url = "https://www.health.com.kh/archives/category/illness/digestive"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    items_result = healthSpider.parse(category_response)

    widget_id = category_response.css("a.infinite-scroll::attr(data-widget-id)").get()
    post_id = category_response.css("a.infinite-scroll::attr(data-post-id)").get()

    links = []
    for link in items_result:
        links.append(link.url)

    assert len(links) - 1 == 10
    assert widget_id == "7f5e22e0"
    assert post_id == "419674"

def test_parse_data_ajax():
    """
    Test the `parse_data_ajax` method of HealthSpider.

    This test sends a POST request to the AJAX endpoint, simulates an AJAX response,
    and verifies that the correct number of items is extracted by the spider.
    
    Attributes:
    ----------
    ajax_url (str):
        The URL for the AJAX request to fetch articles.
    meta (dict):
        The meta data for the AJAX request.
    form_data (dict):
        The query parameters for the AJAX request.
    ajax_response (Response):
        The HTTP response object from the AJAX request.
    ajax_json (dict):
        The JSON data parsed from the AJAX response.
    request (Request):
        The request object created for the AJAX URL.
    json_body (bytes):
        The JSON data encoded as bytes for the response.
    response (TextResponse):
        The response object to be passed to the spider's `parse_data` method.
    items_generator (generator):
        The generator returned by the spider's `parse_data` method.
    items_list (list):
        The list of articles extracted from the generator.
    Asserts:
        - The number of extracted items matches the expected count.
    """
    # Test on category : digestive
    # url = "https://www.health.com.kh/archives/category/illness/digestive"

    ajax_url = "https://www.health.com.kh/wp-admin/admin-ajax.php"
    
    meta = {
        "widget_id": "7f5e22e0",
        "post_id": "419674",
        "page_number": 2,
        "category_name": "digestive"
    }
    form_data = {
        "action": "rivax_get_load_more_posts",
        "widgetId": "7f5e22e0",
        "postId": "419674",
        "pageNumber": "2",
        "qVars[category_name]": "digestive"
    }

    ajax_response = requests.post(ajax_url, data=form_data)
    ajax_json = ajax_response.json()
    

    json_body = json.dumps(ajax_json).encode('utf-8')

    request = Request(url=ajax_url, meta=meta)
    response = TextResponse(url=ajax_url, body=json_body, request=request)

    # Call the parse_data_ajax
    items_generator = healthSpider.parse_data_ajax(response)

    items_list = list(items_generator)
    assert len(items_list)-1 == 10

def test_parse_data():
    """
    Test the `parse_data` method of HealthSpider.

    This test verifies that the title, content, and URL are correctly extracted
    from an article page.
    
    Attributes:
    ----------
    article_url (str):
        URL of the article to be tested.
    article_response (HtmlResponse):
        The response object for the article URL.
    article_result (list):
        Parsed data from the article page.
    expected_value (dict):
        Expected result of the parsed data.
    
    Asserts:
        - The title is not empty.
        - The content is not empty.
        - The URL is not empty.
    """
    expected_value = {
        "category": "ជំងឹក្រពះ ពោះវៀន",
        "title": "កុំ​ព្រងើយកន្តើយ​! ផឹកទឹក​ខុសពេល​ក៏​ឈឺក្រពះ​ដែរ​",
        "content":["\n                                    \n", "\r\n", "\r\n", "\r\n", "\r\nnew innity_adZone"
                   "(\"fc0cc602ce843b5393684a7fc1b566bc\", \"99630\", {\"width\": \"300\", \"height\": \"250\"}); \r\n", "​ចូរ​យកចិត្តទុកដាក់​លើ​ពេលវេលា​ដែល​អ្នក​ផឹកទឹក "
                   "ដែល​អាចជួយ​សម្រួល​ដ​ល់​ដំណើរការ​ក្រពះ​របស់លោក​អ្នក​បាន​យ៉ាង​ប្រសើរ​។​", "\r\n", "\n\n\n\n", "​ពេល​ភ្ញាក់​ពី​គេង​", "\n\n\n\n", "​ពេលវេលា​មួយ​ដែល​អ្នក​គួរ​ផឹកទឹក "
                   "គឺ​នៅពេលដែល​អ្នក​ក្រោក​ពី​គេង​។ ទន្ទឹមនឹងនេះ "
                   "កែវ​ទឹក​ដំបូង​នៅពេល​ព្រឹក​គួរតែ​ជា​ទឹក​ក្តៅ​ឧណ្ហៗ ដើម្បី​លាង​សម្អាត​ពោះវៀន​។ ការផឹក​ទឹក​ក្តៅ​មួយ​កែវ​ធ្វើឱ្យ​មុខងារ​រាងកាយ​សកម្ម ជួយ​កម្ចាត់​កាកសំណល់​ក្នុង​ក្រពះ "
                   "និង​ចាប់ផ្តើម​ថ្ងៃ​ថ្មី​ដែល​សម្បូរ​ទៅដោយ​ថាមពល​។​", "\n\n\n\n", "​ម៉ោង 12 ថ្ងៃត្រង់​", "\n\n\n\n", "​ពេល​មួយ​ដែល​អ្នក​គួរ​ផឹកទឹក គឺ​មុនពេល​អាហារ​ថ្ងៃត្រង់ "
                   "ដើម្បី​បំពេញ​ក្រពះ​របស់​អ្នក និង​ធ្វើឱ្យ​អ្នកមាន​អារម្មណ៍​ឆ្អែត​។ នេះ​នឹង​កាត់បន្ថយ​លទ្ធភាព​នៃ​ការ​ញ៉ាំ​ច្រើនពេក​អំឡុងពេល​អាហារ "
                   "និង​បង្កើន​ការ​បន្សាប​ជាតិពុល​។ ជាមួយគ្នានេះ នៅពេលដែល​អ្នក​ផឹកទឹក​នៅពេលនេះ វា​ជួយ​បន្សាប​ជាតិពុល​ក្នុង​រាងកាយ​បាន​យ៉ាង​ល្អ​។​", "\n\n\n\n", "​ម៉ោង 3 រសៀល​", "\n\n\n\n", "​ពេលណា​ក៏បាន​នៅ​ចន្លោះ​ម៉ោង​នេះ អ្នក​គួរតែ​ផឹកទឹក​មួយ​កែវ​។ ទន្ទឹមនឹងនេះ "
                   "នៅពេលដែល​អ្នក​ផឹកទឹក​នៅពេលនេះ វា​នឹង​ជួយ​ឱ្យ​ការរំលាយ​អាហារ​របស់​អ្នក​កាន់តែ​ប្រសើរឡើង​។ ជាមួយគ្នានេះ នេះ​មិន​ត្រឹមតែ​រំលឹក​អ្នក​ឱ្យ​ក្រោក​ឡើង "
                   "ហើយ​ធ្វើ​ចលនា​បន្ទាប់ពី​អង្គុយ​យូរ​ប៉ុណ្ណោះ​ទេ ប៉ុន្តែ​ថែមទាំង​ជួយ​ឱ្យ​អ្នក​នៅ​ឱ្យ​ឆ្ងាយ​ពី​អាហារ និង​ភេសជ្ជៈ​ដែលមាន​ជាតិ​ស្ករ​… "
                   "អ្វីៗ​ទាំងអស់​ដែល​នឹងធ្វើ​ឱ្យ​អ្នក​ឡើង​ទម្ងន់​។ ទន្ទឹមនឹងនេះ ការ​លើស​ទម្ងន់​នឹង​នាំឱ្យមាន​ជំងឺ​រ៉ាំរ៉ៃ​ដ៏​គ្រោះថ្នាក់​ជាច្រើន​ទៀត​៕", "\n\n\n\n", "​", "\n                                                                                                        "]
    }
    article_url = "https://www.health.com.kh/archives/425671"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(healthSpider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url
  
