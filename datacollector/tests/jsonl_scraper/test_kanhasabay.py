"""Test Case For kanhasabay Cambodia Website"""
import requests
from scrapy.http import HtmlResponse, TextResponse, Request
from url_khmer_scraping.jsonl_scraper.spiders.kanhasabay import KanhasabaySpider

kanhasabay_spider = KanhasabaySpider()

def test_parse_kanhasabay():
    """
    Test the `parse` method of the KanhasabaySpider.

    Attributes
    ----------
    category_url : str
        The URL of the category page (healths) to be tested.
    category : requests.Response
        The HTTP response object obtained from making a GET request to the category URL.
    category_response : scrapy.http.HtmlResponse
        The response object to be passed to the spider's `parse` method, simulating
        the response from the website.
    category_result : generator
        The generator returned by the spider's `parse` method, yielding AJAX requests.
    """
    category_url = "https://kanha.sabay.com.kh/topics/healths"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = kanhasabay_spider.parse(category_response)

    """
    testing the parsing category 
    """
    form_request = next(category_result)
    assert form_request.meta["category"] == "healths"
    assert form_request.meta["page"] == 1
    assert form_request.method == "GET"

def test_parse_data_ajax_kanhasabay():
    """
    Test the `parse_data_ajax` method of kanhasabay_spider.
    
    Attributes
    ----------
    ajax_api : str
        The URL of the AJAX request fetching articles for the 'pregnancy' category.
    category : str
        The category of articles being tested ('pregnancy').
    ajax_response : requests.Response
        The HTTP response object returned from the AJAX request.
    request : scrapy.http.Request
        The request object used to simulate the spider's AJAX request.
    response : scrapy.http.TextResponse
        The response object used for testing the spider's `parse_data_ajax` method.
    items_generator : generator
        The generator returned by `parse_data_ajax`, yielding article links and further AJAX requests.
    items_list : list
        The list of articles and requests extracted from the generator.
    """

    ajax_api = "https://kanha.sabay.com.kh/ajax/topics/pregnancy/1"
    category = "pregnancy"

    ajax_response = requests.get(ajax_api)
    
    #assert ajax_response.status_code == 200
    request = Request(url=ajax_api, meta={"category": category, "page": 1})
    response = TextResponse(url=ajax_api, body=ajax_response.text, encoding='utf-8', request=request)

    items_generator = kanhasabay_spider.parse_data_ajax(response)
    items_list = list(items_generator)

    assert len(items_list) -1 == 14
    assert items_list[14].url == "https://kanha.sabay.com.kh/ajax/topics/pregnancy/2"

def test_parse_data_kanhasabay():
    """
    Test the `parse_data` method of the `KanhasabaySpider`.

    This test checks the following:
    - The category of the article is not empty
    - The title of the article is not empty.
    - The content of the article is not an empty dictionary.
    - The URL of the article is not an empty dictionary.

    Attributes
    ----------
    article_url : str
        The URL of the article to be tested.
    article : requests.Response
        The HTTP response object obtained from making a GET request to the article URL.
    article_response : scrapy.http.HtmlResponse
        The response object passed to the spider's `parse_data` method, simulating
        the response from the article page.
    article_result : generator
        The generator returned by the spider's `parse_data` method, yielding Scrapy items.
    expected_value : dict
        Expected result of the parsed data.
    """
    expected_value = {
        "category": "អប់រំ,Knowledge",
        "title": "បើចង់មានទំនាក់ទំនងល្អជាមួយមនុស្សជុំវិញខ្លួន ត្រូវប្រកាន់៤ចំណុចនេះ",
        "content": "មិនថាបងប្អូន ស្នេហា មិត្តភក្ក័ ទោះបីស្រលាញ់គ្នាប៉ុណ្ណាក៏ដោយក៏ត្រូវតែប្រកាន់រឿង៤ចំណុចនេះ "
        "ដើម្បីកុំឲ្យលំបាកមើលមុខគ្នាទៅថ្ងៃខាងមុខ នោះគឺ ៖១ រឿងទ្រព្យសម្បត្តិvar gammatag = gammatag || {};gammatag.cmd = gammatag.cmd || [];gammatag.cmd.push(function() {gammatag.defineZone"
        "({code:'gax-inpage-async-1700714493',size:[640,1386],params:{siteId:'1700713118',zoneId:'1700714493',zoneType:'Inpage'}});gammatag.sendRequest();});"
        "រឿងទ្រព្យសម្បត្តិគឺជារឿងដែលចាំបាច់ក្នុងការបិតបាំងពីមនុស្សនៅជុំវិញខ្លួន បើទោះបីជាបងប្អូនក៏ដោយ ព្រោះពេលខ្លះអាចមានការច្រណែនគ្នាដោយសាររឿងបន្តិចបន្តួចធ្វើឲ្យឈ្លោះគ្នា។មនុស្សខ្លះអាចបោះបង់គ្នាចោលព្រោះតែភា"
        "ពលោភលន់ ដោយមិនឲ្យតំលៃទៅលើ មិត្តភាព។ តាមពិតទៅ មនុស្សគ្រប់គ្នាសុទ្ធតែលោភលន់ ប៉ុន្តែយើងត្រូវមានភាពក្លាហាន និងការយល់ដឹង ដើម្បីយល់ថា លុយណាគួរទទួលយក ហើយលុយណាគួរទុកចោល។var gammatag = ""gammatag || {};gammatag.cmd = gammatag.cmd || [];gammatag.cmd.push(function() { gammatag.defineZone({code:'gax-inpage-async-1706848615',size:[640,1386],params:{siteId:'1700713118',zoneId:'1706848615',zoneType:'Inpage'}});gammatag.sendRequest();});២ បើចង់រក្សាទំនាក់ទំនងល្អ កុំខ្ចីលុយគ្នាមិនថាបងប្អូន "
        "មិត្តភក្ក័ ឬស្នេហា ពេលខ្លះមានភាពលំបាកជាច្រើននិងមានលក្ខខណ្ឌសេដ្ឋកិច្ចខុសគ្នា ពេលខ្លះក៏លំបាករាងៗខ្លួន "
        "ដូចនេះដើម្បីកុំឲ្យមើលមុខគ្នាមិនចំទៅថ្ងៃ សូមកុំខ្ចីលុយគ្នា ព្រោះពេលខ្លះមិនបានដូចចិត្ត។ ពេលពិបាកពេក យើងអាចពឹងលើការជួយពីបងប្អូនមិត្តភក្ក័ បាន ប៉ុន្តែយើងត្រូវចាំថា លុយអាចខ្ចី និងសងវិញបាន "
        "មិនត្រូវពឹងផ្អែកលើការស្រលាញ់ និងជំនួយពីអ្នកដ៏ទៃ ដោយមិនទទួលខុសត្រូវក្នុងកិច្ចការសងត្រឡប់របស់យើងនោះទេ។៣ កុំភ្លេចជួយក្នុងនាមជាមនុស្សត្រូវចេះជួយនិងដឹងគុណគ្នាទៅវិញទៅមក នោះហើយគឺជាភាពស្រស់ស្អាតនៃចិត្តមនុស្ស។៤ "
        "មិនជ្រៀតជ្រែកចូលក្នុងជីវិតផ្ទាល់ខ្លួនរបស់មនុស្សម្នាក់ៗមនុស្សម្នាក់ៗតែងមានរឿងឯកជនផ្ទាល់ខ្លួន មានការលាក់បាំង មិនសូវចង់ឲ្យនរណាម្នាក់ចង់ដឹងរឿងរបស់ខ្លួនឡើយ ព្រោះអាចធ្វើឲ្យទំនាក់ទំនងមានការធ្លាក់ចុះ៕",
    }

    article_url = "https://kanha.sabay.com.kh/article/1357208"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(kanhasabay_spider.parse_data(article_response))

    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url