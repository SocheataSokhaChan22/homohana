"""Test Case For AMS Infotainment Website Cambodia"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.amsinfotainment import AMSinfotainmentSpider

amsinfotainment_spider = AMSinfotainmentSpider()

def test_parse_data_asminfotainment():
    """
    Test the parse_data method of AMSinfotainmentSpider.

    Attributes:
    -------------
    article_url (str):
        URL of the article to be tested.
    article_response (HtmlResponse):
        The response object for the article URL.
    article_result (list):
        Parsed data from the article page.
    expected_value (dict):
        Expected result of the parsed data. 

    Assertions:
        - The 'title' field of the parsed article is not empty.
        - The 'content' field of the parsed article is not empty.
        - The 'url' field of the parsed article is not empty.
    """
    expected_value = {
        "category": "ព័ត៌មានរសនិយម,ព្រឹត្តិការណ៍,សុខភាពនិងសម្រស់,ព័ត៌មានរសនិយម,ព្រឹត្តិការណ៍,សុខភាពនិងសម្រស់,តារាល្បីៗ,បទយកការណ៍,របាយការណ៍ព័ត៌មានកម្សាន្ត,ព័ត៌មានរសនិយម,ព្រឹត្តិការណ៍,សុខភាពនិងសម្រស់",
        "title": "Sooyoung ក្រុម Girls’ Generation ទម្លាយអារម្មណ៍លំបាកដោយសារចង់សម្រកទម្ងន់ ២ គីឡូ",
        "content" : (
                "Sooyoung សមាជិកក្រុម Girls’ Generation "
                "ថ្មីៗនេះបានបង្ហោះវីដេអូមួយដោយចែករំលែកអំពីភាពលំបាកនៃការសម្រកទម្ងន់ដើម្បីថតរូបផ្សព្វផ្សាយនៅពេលខាង"
                "មុខឆាប់ៗនេះ។ នៅក្នុងវីដេអូដែលបានចាក់ផ្សាយកាលពីថ្ងៃទី២៦ "
                "ខែសីហាថ្មីៗនេះនៅលើឆាណែលយូធូបផ្ទាល់ខ្លួនរបស់នាង “the sootory” "
                "នាងបាននិយាយថាប៉ុន្មានខែមុននេះនាងបានប្រឹងហាត់ប្រាណយ៉ាងខ្លាំងព្រោះចង់ស្រក ២ គីឡូ "
                "ប៉ុន្តែវាហាក់ដូចជាបរាជ័យ។នាងមានអារម្មណ៍ថាខ្លួនហាក់ឡើងទម្ងន់នៅតែដដែលដោយសារតែនាងបានឡើងម៉ាសសាច់ដុំ"
                " ប៉ុន្តែនាងមិនបានឡើងថ្លឹងលើជញ្ជីងនោះឡើយ។ "
                "នាងសន្មតតាមរយៈការឆ្លុះកញ្ចក់មើលភាពខុសគ្នានៃរាងកាយតែប៉ុណ្ណោះ "
                "ដូច្នេះហើយទើបគិតថាខ្លួនឯងបរាជ័យបែបនេះ។នៅក្នុងវីដេអូដដែលនោះ Sooyoung "
                "ក៏បានចែករំលែកនូវរបបអាហារដ៏តឹងតែងសម្រាប់នាងផងដែរដោយនាងបានញ៉ាំម្ទេសប្លោក "
                "និងព្យាយាមកាត់បន្ថយអាហារដែលសម្បូរកាបូអ៊ីដ្រាតឱ្យបានច្រើនតាមអាចធ្វើបាន។ "
                "នាងបានបន្ដថាពេលញ៉ាំម្ទេសប្លោគឺមិនចាំបាច់ជ្រលក់ក្នុងទឹកជ្រលក់នោះទេ ដោយសារតែវាមានរសជាតិផ្អែមឆ្ងាញ់ និងស្រួយឆ្ងាញ់ទៅហើយ។ ប៉ុន្តែនាងនៅតែធ្វើសម្រកទម្ងន់ ២ គីឡូនោះមិនបានដដែល។ជាពិសេសម្ទេសប្លោកនោះគឺជាកសិផលដែលមិត្តរួមក្រុម Yuri យកពីមកកសិដ្ឋានដោយផ្ទាល់។ Sooyoung បាននិយាយម្ទេសប្លោកទាំងនោះពិតជាមានរសជាតិផ្អែម និងស្រស់ល្អខ្លាំងណាស់។ "
                "នាងបានបន្ថែមថាមិនត្រឹមនាងម្នាក់នោះទេ ពោលគឺ Yuri ក៏បានយកម្ទេសប្លោកទៅផ្ញើសមាជិកដទៃទៀតផងដែរ។ ដូច្នេះហើយទើបសមាជិកទាំងអស់ហៅនាងថាជា “Kiki the Delivery Witch” ប៉ុន្តែ Sooyoung បានកែទៅជា "
                "“Beauty Delivery Witch” វិញ។ កំលុងពេលសម្រាកថ្ងៃត្រង់ Sooyoung បានជ្រើសរើសញ៉ាំនៅសាឡាដមួយចាន "
                "ហើយនាងក៏បានរំឮកទៅដល់កាលពីយប់គឺនាងពិតជាឃ្លានមែនទែនបន្ទាប់ពីញ៉ាំសាឡាដតែមួយចានហើយចូលគេង។ "
                "យ៉ាងណាក្ដី នៅចុងបញ្ចប់នាងក៏បានសម្ដែងនូវអារម្មណ៍ខកចិត្តថាហេតុអ្វីបានស្រក ២ គីឡូពិបាកម្លេះ? "
                "ប៉ុន្តែការស្រក ៥ គីឡួបែរជាមិនពិបាកទៅវិញ មិនថានាងខំប្រឹងកំណត់របបអាហារយ៉ាងណាក៏ដោយ។ "
                "នាងគិតថានេះមិនមែនមកពីកត្តាអ្វីផ្សេងនោះទេ "
                "ប៉ុន្តែគឺបណ្ដាលមកពីភាគរយនៃជាតិខ្លាញ់ក្នុងខ្លួនដែលជាបញ្ហាដ៏ពិតប្រាកដ៕"
            )
    }
    article_url = "https://infotainment.ams.com.kh/celebrity/news/sooyong-girls-generationreveals-her-dieting-journey-losing-2kg/"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(amsinfotainment_spider.parse_data(article_response))

    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_asminfotainment():
    """
    Test the parse method of AMSinfotainmentSpider.

    Attributes:
    ------------
    category_url (str): 
        URL of the category page to be tested.
    category_response (HtmlResponse):
        The response object for the category URL.
    category_result (list):
        Parsed data from the category page.
    links (list):
        List of article links extracted from the category page.
    next_page_url (str):
        Constructed URL for the next page.
    Assertions:
        - The number of article links (excluding the next page link) is 10.
        - The 11th link is the URL for the next page.
        - The next page URL matches the expected URL.
    """

    category_url = "https://infotainment.ams.com.kh/category/celebrity/news"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = amsinfotainment_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    next_page_url = category_response.css("nav.pagination a.next::attr(href)").get()

    assert len(links) - 1 == 10
    assert links[10] == next_page_url
    assert links[10] == "https://infotainment.ams.com.kh/category/celebrity/news/page/2/"
