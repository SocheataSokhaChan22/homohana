"""Test Case For Ohh Cambodia Website"""
import requests
from scrapy.http import HtmlResponse, Request, TextResponse
from url_khmer_scraping.jsonl_scraper.spiders.ohhcambodia import OhhcambodiaSpider
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle
import json

ohhcambodia_spider = OhhcambodiaSpider()
pagination_handle = PaginationHandle()

user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36"
headers = {
    'User-Agent': user_agent,
}

def test_parse_blog_ohhcambodia():

    category_url = "https://ohhcambodia.com/blog/"
    category = requests.get(category_url,headers=headers)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = ohhcambodia_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    next_page_url = pagination_handle.get_next_page_url(category_response.url)
    assert len(links) - 1 == 10
    assert links[10] == next_page_url
    assert links[10] == "https://ohhcambodia.com/blog/page/2"

def test_parse_listings_ohhcambodia():
    """
    Test of `parse` method of the `OhhcambodiaSpider`.
    
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
    category_url = "https://ohhcambodia.com/listings/"
    category = requests.get(category_url, headers=headers)
    response = TextResponse(url=category_url, body=category.text, encoding='utf-8')

    # Run the spider's parse method
    request = list(ohhcambodia_spider.parse(response))

    # Check if AJAX request is made
    assert len(request) == 1
    assert request[0].url == ohhcambodia_spider.ajax_url
    assert request[0].method == 'POST'
    assert request[0].body == b'per_page=50&orderby=featured&featured_first=false&order=DESC&page=1'

def test_parse_data_ajax_blogs_ohhcambodia():
    """
    Test of `parse` method of the `OhhcambodiaSpider`.
    
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
    category_url = "https://ohhcambodia.com/listings/"
    ajax_url = "https://ohhcambodia.com/jm-ajax/get_listings/"
    
    meta = {
        "page_number": 1,
    }
    form_data = {
        "per_page": "50",
        "orderby": "featured",
        "featured_first": "false",
        "order": "DESC",
        "page": "1"
    }

    ajax_response = requests.post(ajax_url, data=form_data, headers=headers)
    ajax_json = ajax_response.json()
    
    json_body = json.dumps(ajax_json).encode('utf-8')

    request = Request(url=ajax_url, meta=meta)
    response = TextResponse(url=ajax_url, body=json_body, request=request)

    items_generator = ohhcambodia_spider.parse_data_ajax(response)

    items_list = list(items_generator)
    assert len(items_list) == 51

def test_parse_data_with_listings_ohhcambodia():
    """
    This function is used to test the parse data method of `OhhcambodiaSpider`.
    This checks to see if the filtering works correctly.
    This test is conducted using live data from the website.

    Note: The filtering mainly focuses on the URL.

    Attribute
    ---------
    article_response:
        live response generated from article url
    article_result:
        list of article urls generated from article response
    article: dict
        desired output (should be parsed)
    expected_value: dict
        Expected result of the parsed data.
    """
    expected_value = {
        "category": "វិចិត្រសាលសិល្បៈ",
        "title": "វិចិត្រសាលទេពកោសល្យ Tep Kaosol Gallery\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t",
        "content": "\n\tអំពី\n\t\n\t\tនៅ​ក្នុងវិចិត្រសាលនេះ មាន​ដាក់បង្ហាញ​នូវរូប​ភាព​ស្នាម​ញញឹម​របស់ក្មេង​ ព្រះ​សង្ឃ​ អគារ​ដែល​បន្សល់​ពី​សម័យ​អាណានិគម​បារាំង​ និងរូបភាព​អប្សរា។\nបើក​ជារៀងរាល់ថ្ងៃ ចាប់ពីម៉ោង 9am-2pm\n\t\n",
        }
        
    article_url = "https://ohhcambodia.com/listings/tep-kaosol-gallery/"
    article = requests.get(article_url, headers=headers)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")
    category = "វិចិត្រសាលសិល្បៈ"
    article = next(ohhcambodia_spider.parse_data(article_response, category))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url


def test_parse_data_with_blogs_ohhcambodia():
    """
    This function is used to test the parse data method of `OhhcambodiaSpider`.
    This checks to see if the filtering works correctly.
    This test is conducted using live data from the website.

    Note: The filtering mainly focuses on the URL.

    Attribute
    ---------
    article_response:
        live response generated from article url
    article_result:
        list of article urls generated from article response
    article: dict
        desired output (should be parsed)
    """

    expected_value = {
        "category": "ចែករំលែកបទពិសោធន៍ដើរ,ណែនាំកន្លែងដើរ,បាត់ដំបង",
        "title": "\n                    មូលហេតុដែលអ្នកគួរបញ្ចូលខេត្តបាត់ដំបងក្នុងបញ្ជីដើរលេងរបស់អ្នក                ",
        "content": ("\n            \n​For English version, click here. \n\n\n\nខ្ញុំធ្លាប់សន្យាជាមួយនឹងខ្លួនឯងថាខ្ញុំនឹងទៅលេងខេត្តបាត់ដំបងម្តងទៀត "
                    "បន្ទាប់ពីខ្ញុំត្រឡប់មកពីចូលរួមពិធីមង្គលការរបស់មិត្តភក្តិខ្ញុំម្នាក់នៅទីនោះ។ ខ្ញុំក៏ចាំបានដែរថាខ្ញុំភ្ញាក់ផ្អើលនឹងទស្សនីយភាពរបស់ខេត្តមួយនេះជាខ្លាំងពេលដែលបានទៅលេងនៅទីនោះជាលើកទីមួយ។ មិនថាយ៉ាងម៉េចយ៉ាងម៉ាទេ "
                    "ខ្ញុំដឹងតែថាត្រូវទៅលេងខេត្តនេះម្តងទៀតអោយបាន។\n\n\n\nបន្ទាប់ពីរយៈពេលប្រមាណមួយឆ្នាំកន្លងផុតទៅ ខ្ញុំក៏ឃើញគេរៀបចំកម្មវិធីមួយនៅខេត្តបាត់ដំបងនេះដែលមានឈ្មោះថា S’Art Urban Art Festival មិនបង្អង់យូរ "
                    "ខ្ញុំក៏សម្រេចចិត្តវេចកាតាបរត់ទៅភ្លាមតែម្តង។\n\n\n\nខ្ញុំនិងមិត្តភក្តិរបស់ខ្ញុំបានចំណាយពេល ២ថ្ងៃ នៅខេត្តបាត់ដំបងនេះ។ គោលបំណងសំខាន់របស់ដំណើរកម្សាន្តយើងលើកនេះគឺដើម្បីចូលរួមក្នុងកម្មវិធី S’Art Urban Art Festival នេះឯង "
                    "តែបើទោះបីជាអ្នកទាំងអស់គ្នាមិនអាចមើលឃើញទស្សនីយភាពផ្សេងៗដែលរៀបចំក្នុងកម្មវិធីនេះនៅពេលដែលអ្នកទៅលេងខេត្តបាត់ដំបងក៏ដោយ ក៏ខ្ញុំនៅតែចែករំលែកពីបទពិសោធន៍របស់​ខ្ញុំទាំងមូលនៅក្នុងអត្ថបទនេះដែរ។ \n\n\n\nអ្វីដែលអ្នកទាំងអស់គ្នានឹងអាននៅប៉ុន្មាននាទីខាងមុខនេះអាចជាមូលហេតុដែលនាំអោយអ្នកទាំងអស់គ្នាបញ្ចូលខេត្តបាត់ដំបងក្នុងបញ្ជីដើរលេងរបស់អ្នកបាន។ ប៉ុន្តែមុននឹងអ្នកទាំងអស់គ្នាអានបន្ត ខ្ញុំចង់បញ្ជាក់ថា ​៖\n\n\n\n១. អ្នកនឹងមិនឃើញពីកម្មវិធីពិសេសៗមួយចំនួនដែលនឹងរៀបរាប់ក្នុងអត្ថបទនេះទេ "
                    "ដោយសារតែកម្មវិធីទាំងអស់នោះត្រូវបានគេរៀបចំឡើងសម្រាប់កម្មវិធី  S’Art Urban Art Festival តែមួយពេលប៉ុណ្ណោះ។ ប៉ុន្តែប្រសិនបើអ្នកចង់ចូលរួមក្នុងកម្មវិធីនេះដែរ "
                    "ខ្ញុំឮថាគេនឹងរៀបចំវាឡើងជាថ្មីម្តងទៀតនៅឆ្នាំក្រោយៗ អញ្ចឹងតាមដានហ្វេសប៊ុកមើលហើយសេវថ្ងៃទុកអោយហើយទៅ។២. "
                    "អត្ថបទនេះមិនមែនសរសេរឡើងសម្រាប់ដែលអ្នកមិនធ្លាប់ទៅខេត្តបាត់ដំបងសោះនោះទេ។ តែប្រសិនបើអ្នកមិនធ្លាប់ទៅទាល់តែសោះ "
                    "អ្នកគួរតែបន្ថែមកន្លែងទាំងអស់នេះចូលទៅក្នុងគម្រោងដើរលេងរបស់អ្នក ៖– ភ្នំសំពៅ– ល្អាងប្រចៀវ– ភ្នំបាណន់– ជិះណូរី– មើលការសម្តែងសៀករហ័ស្សកម្មនៅ ហ្វាពន្លឺសិល្បៈ– ញ៉ាំមីកូឡាម្ចាស់ដើម\n\n\n\nថ្ងៃទី ១\n\n\n\nពួកយើងចំណាយពេលជិះឡាន ៥ម៉ោង ពីភ្នំពេញ-បាត់ដំបង។ "
                    "យើងរំពឹងថាទៅដល់នោះម៉ោងប្រហែល ២ៈ០០ថ្ងៃ តែទៅដល់នោះលឿនជាងការរំពឹងទុកដល់ទៅ២ម៉ោង ដូច្នោះហើយយើងក៏សម្រាកសិនមុននៅអូតែលសិនមុននឹងចេញទៅដើរលេង។ ដើម្បីឆែកនិងទិញសំបុត្រឡាន "
                    "អ្នកអាចចុច ទីនេះ បាន។ \n\n\n\nបន្ទាប់ពីសម្រាកយកកម្លាំងរួច យើងក៏ដើររកកន្លែងជួលម៉ូតូ។\n\n\n\nជួលម៉ូតូពីហាង The Gecko\n\n\n\nម៉ូតូជាមធ្យោបាយធ្វើដំណើរដ៏ងាយស្រួលនិងថោកបំផុតនៅបាត់ដំបង "
                    "ប៉ុន្តែបើអ្នកអត់ចេះជិះម៉ូតូទេ អ្នកក៏អាចជិះតុកតុកបានដែរ។\n\n\n\nពួកយើងជួលម៉ូតូ ២គ្រឿង ពីហាង The Gecko។ ម៉ូតូអូតូមានតម្លៃ ២៨០០០រៀល/ថ្ងៃ (៧ដុល្លារ) ចំណែកឯម៉ូតូដាក់លេខវិញតែ ២៤០០០រៀល/ថ្ងៃ (៦ដុល្លារ) ប៉ុណ្នោះ។ អ្នកទាំងអស់គ្នាត្រូវយកម៉ូតូមកសងគេវិញក្នុងរយៈពេល ២៤ម៉ោង បន្ទាប់ពីយើងជួល "
                    "ហើយត្រូវទុកសាំងអោយគេវិញប៉ុនបរិមាណសាំងពេលដែលយើងជួលដំបូង ហើយកុំភ្លេចសួររកមួកការពារផង។ \n\n\n\nដើម្បីជួលម៉ូតូបាន អ្នកត្រូវ ៖១. ទុកអត្តសញ្ញាណប័ណ្ណ រឺ លិខិតឆ្លងដែន "
                    "នៅហាងជួលម៉ូតូនោះរហូតដល់ពេលដែលអ្នកយកម៉ូតូសងគេវិញ។២. អានលក្ខខណ្ឌអោយបានច្បាស់លាស់ រួចចុះហត្ថលេខាបែបបទជួលម៉ូតូ។ \n\n\n\nក្រៅពីជួលម៉ូតូ នៅហាងនេះក៏មានលក់វត្ថុអនុស្សាវរីយ៍និងរបស់របរតិចតួចដែរ។\n\n\n\n\n\n\n\nទីតាំង៖ ផ្លូវលេខ ១ "
                    "ក្រុងបាត់ដំបងម៉ោងធ្វើការ៖ ៨ៈ០០ព្រឹក – ១០ៈ០០យប់\n\n\n\nផឹកកាហ្វេនៅហាង Forest Coffee and Bakery\n\n\n\nពួកយើងបានជួបមិត្តភក្តិម្នាក់ដោយចៃដន្យពេលយើងជិះឡានពីភ្នំពេញទៅបាត់ដំបង ហើយគេបានណែនាំយើងអោយទៅញ៉ាំកាហ្វេនៅហាង Forest Coffee and Bakery។ "
                    "ដោយសារតែមេឃវានៅក្តៅនៅឡើយបន្ទាប់ពីយើងជួលម៉ូតូ ពួកយើងក៏សម្រេចចិត្តថាទៅសាកកាហ្វេនៅហាងនេះតែម្តង។ \n\n\n\nដូចដែលឈ្មោះគេដាក់អញ្ចឹង "
                    "ហាងនេះគេតុបតែងលក្ខណៈជាព្រៃតែម្តង ពួកយើងរកមើលឈ្មោះហាងសឹងតែមិនឃើញ។ \n\n\n\n\n\n\n\nសំខាន់គាត់ប្រាប់យើងថាតែរក Pizza Company ឃើញ​ រកហាងកាហ្វេនោះឃើញហើយ "
                    "ព្រោះវាទល់មុខគ្នា។ មានអី គាត់ប្រាប់ត្រូវតើ ហាងពីរនេះនៅទល់មុខគ្នាមែន គ្រាន់តែមានស្ទឹងសង្កែនៅកណ្តាលប៉ុណ្ណាប៉ុណ្ណីតើ ទាល់តែជិះ U-turn បានកើត។ \n\n\n\nកុំរំពឹងថានៅទីនេះមានម្ហូបញ៉ាំណា មានតែភេសជ្ជៈ នំក្រ័រសង់ និងមីកំប៉ុង តែប៉ុណ្ណោះ។ "
                    "ខ្ញុំកម៉្មង់តែបៃតងទឹកដោះគោ ហើយតម្លៃរបស់វាគឺ ៨៦០០រៀល (២.១៥ដុល្លារ)។\n\n\n\n\n\n\n\nបើនិយាយពីរសជាតិវិញ ខ្ញុំគិតថាវាមិនឆ្ងាញ់ណាស់ណាទេតែក៏មិនមែនអត់ឆ្ងាញ់សោះដែរ ប៉ុន្តែបើអ្នកទាំងអស់គ្នារកកន្លែងដើម្បីគេចពីអាកាសធាតុក្តៅ អាចទៅហាងកាហ្វេនេះបាន។ ហាងគេធំទូលាយ កន្លែងអង្គុយស្រួល ហើយការតុបតែងលក្ខណៈជាព្រៃនោះក៏មើលទៅឃើញស្អាតម៉្យាង។\n\n\n\nនេះគឺការតុបតែងខ្លះៗនៅក្នុងហាង។\n\n\n\n\n\n\n\nទីតាំង៖ ផ្ទះលេខ ៣៣​ ផ្លូវ ១៥៩D បាត់ដំបងម៉ោងធ្វើការ៖ ៦ៈ០០ព្រឹក – "
                    "៨ៈ០០យប់\n\n\n\nថតរូបមុខសាលាខេត្ត\n\n\n\nបន្ទាប់ពីចេញពីហាងកាហ្វេមក យើងក៏ចាប់ផ្តើមជិះដើរលេងជុំវិញខេត្ត។ ពួកយើងជិះកាត់សាលាខេត្តបាត់ដំបង ហើយឃើញអគារស្អាត "
                    "ពួកយើងថតរូបនៅមុខនោះពីរបីប៉ុស្តិ៍។\n\n\n\n\n\n\n\nលំហែអារម្មណ៍នៅ Baha’i House of Worship \n\n\n\nខ្ញុំរកឃើញ Baha’i House of Worship នេះនៅពេលដែលខ្ញុំដាក់ #battambang ក្នុងអុីនស្តាក្រាម។ ខ្ញុំសឹងតែអត់ជឿថាមានកន្លែងបែបនេះនៅខេត្តបាត់ដំបងសោះ "
                    "ព្រោះមើលទៅអត់មានស្ទាយ៍ខ្មែរអីបន្តិច គិតថាគេដាក់ hashtag ខុសទៀតហ្នឹង។ អាគារស្អាតព័ទ្ធជុំវិញដោយសួនពណ៌បៃតងហើយបរិវេណជុំវិញស្ងប់ស្ងាត់ល្អទៀត "
                    "ប្រសិនបើអ្នកកំពុងរកកន្លែងស្ងប់ស្ងាត់ដើម្បីសមាធិ ទៅ Baha’i នេះទៅអត់ខុសទេ។ \n\n\n\n\n\n\n\n\n\n\n\nទីតាំង៖ ផ្លូវបោះពោធ៍ អូស្រឡៅម៉ោងធ្វើការ៖ ៩ៈ០០ព្រឹក – ៧ៈ០០យប់\n\n\n\nញ៉ាំស្តេកសាច់គោអូស្រ្តាលីតម្លៃ ២០,០០០រៀល នៅភោជនីយដ្ឋាន Delicious (Delicious Restaurant)\n\n\n\nបន្ទាប់ពីចេញពី Baha’i មក វារៀងល្ងាចបន្តិចហើយ ពោះនោះក៏វាកូរទៀត។ "
                    "ពួកយើងជិះដើររកកន្លែងញ៉ាំ ហើយបានឈប់ត្រឹងនៅភោជនីយដ្ឋាន Delicious។ នេះមិនមែនជាកន្លែងដ៏ល្អបំផុតសម្រាប់ញ៉ាំអាហារនៅខេត្តបាត់ដំបងទេ "
                    "ប៉ុន្តែប្រសិនបើខ្ចិលរកកន្លែងញ៉ាំដូចពួកយើងដែរ​ អ្នកអាចសាកល្បងញ៉ាំនៅហាងនេះបាន។ \n\n\n\nតាមពិតទៅដំបូងឡើយពួកយើងអត់ចង់ញ៉ាំនៅហាងនេះទេ ប៉ុន្តែមិត្តប្រុសរបស់ខ្ញុំគាត់ឃើញមីនុយអាហារថាស្តេកសាច់គោអូស្ត្រាលីតម្លៃ ២០០០០រៀល "
                    "ពួកយើងអត់គិតយូរក៏ចូលទៅតែម្តង។ \n\n\n\nចាញ់បោក marketing គេសោះ។ ពួកយើងកម៉្មង់ស្តេកសាច់គោអូស្ត្រាលីនេះទាំងអស់គ្នា សាច់អូស្ត្រាលីអី សាច់គោខ្មែរអោយសុទ្ធ។ "
                    "ហាហាហា តែទៅរំពឹងអីស្តេក ២០០០០រៀល ត្រូវអត់? តែមានអី រសជាតិគេគ្រាន់បើតើ។\n\n\n\n\n\n\n\nទីតាំង៖ ផ្លូវលេខ ១២១​ បាត់ដំបងម៉ោងធ្វើការ៖ ៧ៈ០០ព្រឹក – ៩ៈ០០យប់\n\n\n\nមើលការប្រគួតរាំហុីបហប់នៅហ្វាពន្លឺសិល្បៈ\n\n\n\nការប្រកួតរាំហុីបហប់នេះ "
                    "មិនមែនជាអ្វីដែលអ្នកទាំងអស់គ្នាអាចមើលបានរាល់ពេលដែលទៅលេងខេត្តបាត់ដំបងនោះទេ។ \n\n\n\n\n\n\n\nការប្រកួតរាំហុីបហប់នេះ គឺជាកម្មវិធីមួយក្នុងចំណោមកម្មវិធីផ្សេងៗទៀតក្នុង S’Art Urban Art Festival។ "
                    "ពួកយើងពិតជារីករាយមែនទែនដែលបានទស្សនាអ្វីដែលយើងមិនធ្លាប់ឃើញផ្ទាល់ពីមុន។ បើអ្នកទាំងអស់គ្នាចង់មើលដែរ ចាំប្រហែល ២ឆ្នាំ ទៀតទៅ។ ហាហាហា\n\n\n\n\n\n\n\nអត់បានមើលគេប្រកួតរាំហុីបហប់មែន "
                    "តែអាចទិញសំបុត្រមើលការសម្តែងសៀករហ័ស្សកម្មនៅហ្វាពន្លឺសិល្បៈនេះបានណា៎។ តម្លៃសំបុត្រ ៥៦០០០រៀល/ម្នាក់ (១៤ដុល្លារ)។ អ្នកអាចទិញសំបុត្រដោយផ្ទាល់នៅហ្វាពន្លឺសិល្បៈរឺក៏ទិញនៅអូតែលនៅបាត់ដំបងក៏បាន។ "
                    "ការសម្តែងចាប់ផ្តើមនៅម៉ោង ៧ៈ០០យប់ ដូច្នេះហើយអ្នកត្រូវទៅដល់ទីនោះមុនម៉ោង៧។\n\n\n\nនៅហ្វាពន្លឺសិល្បៈនេះស្អាតទៀត គេមានគំនូរលើជញ្ជាំងនិងការតុបតែងប្លែកៗមួយចំនួន។ \n\n\n\n\n\n\n\nនៅក្នុងនោះផងដែរក៏មានហាងលក់គំនូរ អាវយឺត "
                    "និងរបស់របរផ្សេងៗផងដែរ។\n\n\n\n\n\n\n\nទីតាំង៖ ភូមិអញ្ចាញ បាត់ដំបង\n\n\n\nថតរូបស្អាតៗនៅ Miss Wong ទុកផុសលើអុីនស្តាក្រាម\n\n\n\nខ្ញុំដូចជាមិនសូវត្រូវធាតុជាមួយហាង​ Miss Wong នេះយ៉ាងម៉េចមិនដឹងទេ រកទៅប៉ុន្មានដងហើយតែទៅដល់ចេះតែបិទរហូត ទាំងនៅសៀមរាបនិងបាត់ដំបង។ "
                    "លើកនេះលើកទី ៤ ហើយទើបបានស្គាល់ជាតិ Miss Wong។\n\n\n\n\n\n\n\nស្រឡាញ់ការតុបតែងនៅ Miss Wong នេះមែនទែន នៅជ្រុងណាក៏ថតរូបស្អាតដែរ។ \n\n\n\n\n\n\n\nសូម្បីតែនៅបន្ទប់ទឹកក៏ស្អាតដែរ។\n\n\n\n\n\n\n\nពួកយើងអត់បានអាន review "
                    "មុនពេលមក Miss Wong នេះទេ ហើយពួកយើងរំពឹងថានឹងទៅញ៉ាំអីនៅកន្លែងនោះរួចទៅអូតែលគេងវិញ។ ស្រាប់តែពេលទៅដល់អត់មានអីញ៉ាំក្រៅពីឌីមសាំផង។\n\n\n\nខ្ញុំកម៉្មង់ភេសជ្ជៈប្រចាំហាងរបស់គេដែលមានឈ្មោះថា Miss Wong Punch ហើយតម្លៃរបស់វា​ ២០,០០០រៀល​(៥ដុល្លារ)។ "
                    "រសជាតិស្រាក្រឡុកដែលខ្ញុំបានញ៉ាំហ្នឹងដូចអត់មានឆ្ងាញ់លើសកន្លែងផ្សេងៗដែលខ្ញុំធ្លាប់ញ៉ាំផង។\n\n\n\n\n\n\n\nទីតាំង៖ ផ្លូវលេខ ២ ផ្សារណាត់ បាត់ដំបង (ជិតចានបាយ Jaan Bai)ម៉ោងធ្វើការ៖ ៤ៈ០០ល្ងាច – ១២ៈ០០យប់\n\n\n\nថ្ងៃទី ២\n\n\n\nញ៉ាំមីគាវនៅ​ មីគាវបីល្វែង\n\n\n\nប្រសិនបើអ្នកទាំងអស់គ្នាសួរអ្នកស្រុកបាត់ដំបងរកកន្លែងញ៉ាំអី "
                    "ខ្ញុំច្បាស់ថាគេនឹងណែនាំអោយអ្នកទៅញ៉ាំមីគាវនៅ មីគាវបីល្វែង គ្រប់គ្នាម៉្មង។\n\n\n\n\n\n\n\nមានអី ឆ្ងាញ់មែនតើ។ សរសៃមីគេឡើងទន់ ហើយគាវនោះឆ្ងាញ់ទៀត ខ្ញុំជឿថាអ្នកទាំងអស់គ្នាប្រាកដជាចង់ញ៉ាំថែមមួយចានពីរចានទៀតម៉្មង បើយល់ល្អ ដាក់មីឌុបអោយហើយទៅ។ "
                    "ឆ្ងាញ់ហើយ តម្លៃសមរម្យទៀត។\n\n\n\n\n\n\n\nទីតាំង៖ ផ្លូវ ១២១ បាត់ដំបង​\n\n\n\nដើរមើលអាគារចាស់ៗស្អាតៗ\n\n\n\nប្រសិនបើអ្នកទាំងអស់គ្នាធ្លាប់មើលរឿង ដំបូងគេសម្លាប់ឪពុករបស់ខ្ញុំ អ្នកប្រាកដជាមានរូបភាពនៅក្នុងចិត្តហើយថាបាត់ដំបងហ្នឹងវាយ៉ាងម៉េច។ \n\n\n\n\n\n\n\nខ្ញុំនិងមិត្តភក្តិខ្ញុំបានចំណាយពេលមួយព្រឹកពេញគ្រាន់តែដើរមើលអាគារចាស់ៗហ្នឹង។សំណង់ពីមួយច្រកទៅមួយច្រកសុទ្ធតែមានលក្ខណៈខុសគ្នាទាំងអស់ "
                    "ហើយខ្ញុំនេះវិញគិតតែពីថតយកៗឡើងអស់ថ្មកាមេរ៉ា។ \n\n\n\n\n\n\n\nកំពុងតែឆ្ងល់ថាគួរចាប់ផ្តើមដើរពីកន្លែងណាមកមែនអត់? ចាប់ផ្តើមដើរពីផ្លូវលេខ១ "
                    "នៅម្តុំផ្សារណាត់មក។ ផ្លូវដែលខ្ញុំចូលចិត្តជាងគេគឺផ្លូវ ២.៥។ \n\n\n\nប្រមាញ់គំនូរលើជញ្ជាំង\n\n\n\nខ្ញុំចាំបានថាខ្ញុំធ្លាប់ឃើញគំនូរលើជញ្ជាំងតែពីរបីកន្លែងប៉ុណ្ណោះពេលដែលខ្ញុំទៅលេងខេត្តបាត់ដំបងកាលពីលើកទីមួយ។ ក្នុងរយៈពេលតែ ១ឆ្នាំកន្លះប៉ុណ្ណោះ "
                    "សិល្បៈគំនូរលើជញ្ជាំងនេះក៏កើនឡើងយ៉ាងខ្លាំង។\n\n\n\n\n\n\n\nអរគុណដល់ S’Art Urban Festival ដែលរួមចំណែកក្នុងការបន្ថែមគំនូរលើជញ្ជាំងនៅបាត់ដំបងនេះ។\n\n\n\n\n\n\n\nប្រសិនបើអ្នកទាំងអស់គ្នា"
                    "ចូលចិត្តគំនូរលើជញ្ជាំងដូចខ្ញុំដែរ ប្រមូលមិត្តភក្តិហើយលេងប្រមាញ់គំនូរទាំងនេះទាំងអស់គ្នា! ខ្ញុំអត់ប្រាប់កន្លែងជាក់លាក់ថាគំនូរទាំងអស់នេះនៅកន្លែងណាទេ ប្រាប់អស់ម៉េចសប្បាយត្រូវអត់? គ្រាន់តែដឹងថាគំនូរទាំងអស់នេះនៅម្តុំផ្សារណាត់ទៅរកឃើញហើយ។ \n\n\n\nផ្សារណាត់បាត់ដំបង\n\n\n\nញ៉ាំទឹកផ្លែឈើក្រឡុកស្រស់ៗនៅ The Lonely Tree Cafe\n\n\n\nបន្ទាប់ពីដើរប្រមាញ់អាគារនិងគំនូរលើជញ្ជាំងអស់មួយព្រឹកមក "
                    "ពួកយើងអស់ខ្យល់រលីងតែម្តង។ បើបានទឹកផ្លែឈើស្រស់ៗត្រជាក់ៗចូលមាត់មិនដឹងជាសប្បាយចិត្តប៉ុណ្ណា។ កំពុងតែគិតៗស្រាប់តែដើរដល់ហាងកាហ្វេមួយដែលមានឈ្មោះថា The Lonely Tree Cafe។ "
                    "ផ្លាកហាងដាក់ហាងកាហ្វេ ប៉ុន្តែអ្វីដែលពួកយើងឃើញគឺហាងលក់វត្ថុអនុស្សាវរីយ៍និងគ្រឿងតុបតែងខ្លួន ទាល់តែពួកយើងសួរគេទៅបានដឹងថាហាងកាហ្វេនៅជាន់ខាងលើ។\n\n\n\n\n\n\n\nខ្ញុំបានកម៉្មង់ទឹកឪឡឹកក្រឡុក"
                    "មួយកែវ ហើយពេលផឹកមួយកែវហើយមិនស្កប់ស្កល់ចង់ផឹកមួយកែវទៀត តែវាស៊យអីគេអស់់ឪឡឹកបាត់។ ទឹកឪឡឹកមួយកែវ ៦០០០រៀល (១.៥ដុល្លារ)។\n\n\n\n\n\n\n\nក្រៅពីភេសជ្ជៈ "
                    "អ្នកទាំងអស់គ្នាក៏អាចញ៉ាំអាហារថ្ងៃត្រង់នៅទីនេះបានដែរ គេមានមុខម្ហូបប្រហែល១០មុខអីដែរ។ ខ្ញុំហៅបាយឆាឡុកឡាក់ ហើយតម្លៃវា ១៦០០០រៀល (៤ដុល្លារ) ចំណែករសជាតិម្ហូបវិញ ខ្ញុំអោយ ៦.៥/១០។\n\n\n\n\n\n\n\nហាងកាហ្វេ The Lonely Tree Cafe "
                    "នេះក៏ជាកន្លែងមួយដែលថតរូបស្អាតៗបានដែរ។\n\n\n\n\n\n\n\nហើយនេះគឺជាហាងលក់របស់របរផ្សេងៗនៅជាន់ក្រោម។\n\n\n\n\n\n\n\nទីតាំង៖ ផ្លូវលេខ ២.៥ បាត់ដំបង (ជាន់ទី​ ១)ម៉ោងធ្វើការ៖ ១០ៈ០០ព្រឹក រហូតដល់ម៉ោងប៉ុន្មានក៏មិនដឹង \n\n\n\nញាំប្រហិតចែមុី\n\n\n\nប្រហិតឆ្ងាញ់ ទឹកជ្រលក់ឆ្ងាញ់ "
                    "តម្លៃក៏មិនថ្លៃ។ ប្រហិតសាច់គោមួយចង្កាក់ ២០០០រៀល ហើយនំប័ុងមួយដើមក៏ ២០០០រៀល​ ដូចគ្នា។ ពេលទៅបាត់ដំបងកុំភ្លេចចូលញ៉ាំផង!\n\n\n\n\n\n\n\nទីតាំង៖ ផ្លូវ ១២១ បាត់ដំបង (ជិតសាលាចិន លាន ហ័រ)\n\n\n\nដើរជាមួយក្បួនដង្ហែទីងមោងធំៗក្នុងកម្មវិធី S’Art Urban Festival\n\n\n\nខ្ញុំអត់ដែលចូលរួមកម្មវិធីអីគួរអោយរំភើបដូចកម្មវិធីនេះទេ។\n\n\n\n\n\n\n\nទំរាំ"
                    "តែគេចេញក្បួនដង្ហែហ្នឹង គេរៀបចំមុនមិនចេះតិចម៉ោង។\n\n\n\n\n\n\n\nសូមសរសើរបុិនេះម៉្មង គាត់ពាក់អាជើងហ្នឹងដើរបានឡើងឆ្ងាយ។\n\n\n\n\n\n\n\nអីយ៉ាស់ ចាប់បានយក្សជិះម៉ូតូ!\n\n\n\n\n\n\n\nក្បួនដង្ហែនេះចាប់ផ្តើមពីវត្តពិភិទ្ធារាមដល់សួននាគបាញ់ទឹក។\n\n\n\n\n\n\n\nសង្ឃឹមថានឹងមាន S’Art Urban Festival ម្តងទៀតឆាប់ៗ។ "
                    "សូមបញ្ជាក់ម្តងទៀតផងដែរថាក្បួនដង្ហែនេះមានតែក្នុងកម្មវិធី S’Art Urban Festival ប៉ុណ្ណោះ។\n\n\n\nតោះ ទៅលេងបាត់ដំបងទាំងអស់គ្នាហ្ហី? កក់សំបុត្រឡាននៅ ទីនេះ។\n\n\n\nAvyTravel គឺជាគេហទំព័រអំពីដំណើរកម្សាន្តនិងបទពិសោធន៍ដើរលេងរបស់អេវីផ្ទាល់ទាំងនៅក្នុងប្រទេសកម្ពុជានិងនៅប្រទេសជិតខាង។ នៅក្នុងអត្ថបទនីមួយៗ អេវីតែងតែបង្ហាញពីកន្លែងដើរលេងផ្សេងៗ "
                    "អ្វីដែលគួរអោយចាប់អារម្មណ៍បំផុតនៅកន្លែងនោះ ការវាយតម្លៃកន្លែងគេង (hotel review) "
                    "បទពិសោធន៍ទាំងល្អនិងអាក្រក់។ «ចង់ប្រាប់ថាអេវីមិនមែនសាវ៉ាទេណា គ្រាន់តែលង់ស្នេហ៍ជាមួយគ្រប់កន្លែងដែលបានទៅលេងតើ!»\n        ")}

    article_url = "https://ohhcambodia.com/why-battambang-should-be-in-your-bucket-list/"
    article = requests.get(article_url, headers=headers)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")
    article = next(ohhcambodia_spider.parse_data(article_response, category=None))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url