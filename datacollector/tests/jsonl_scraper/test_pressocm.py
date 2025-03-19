"""Test Case For Pressocm"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.pressocm import PressocmSpider

pressocm_spider = PressocmSpider()

def test_parse_pressocm():
    """
    Test of `parse` method of the pressocm spider.
    
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
    category_url = "https://pressocm.gov.kh/archives/category/general-information-km/news-km/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = pressocm_spider.parse(category_response)

    """
    testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    next_page = category_response.url.rstrip("/").split("/")

    if next_page[-1].isdigit():
        next_page[-1] = str(int(next_page[-1]) + 1)
    else:
        next_page.append("page/2")
    
    next_page_url = "/".join(next_page)
    cat = category_response.css("h1[class='entry-title td-page-title']::text").get()
    
    assert cat == "ព័ត៌មាន"
    assert len(links) - 1 == 10
    assert links[10] == next_page_url
    assert links[10] == "https://pressocm.gov.kh/archives/category/general-information-km/news-km/page/2"

def test_parse_data_pressocm():
    """
    This function is used to test the parse data method of PressocmSpider.
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
        "category": "ទស្សនៈ-នយោបាយ",
        "title": "២០មិថុនា កំណត់ត្រាអំពីតម្លៃនៃការលះបង់ដើម្បីសិទ្ធិរស់រានមានជីវិតរបស់ពលរដ្ឋខ្មែរ",
        "content": (
            "ថ្ងៃទី២០ មិថុនា កាលពី៤៧ឆ្នាំមុន នៅលើទឹកដីជាយដែននៃកម្ពុជា មានយុវជនខ្មែរមួយរូបទើបតែអាយុ ២៥ឆ្នាំ "
            "បានសម្រេចចិត្តប្រកបដោយការលះបង់ខ្ពស់បំផុតជាមួយយុទ្ធមិត្តដ៏ស្មោះស្ម័គ្រ៤រូបផ្សេងទៀតដើម្បីទាមទារសិទ្ធិរស់រានមានជីវិតរបស់ពលរដ្ឋខ្មែរ។ រឿងដែលគេឧស្សាហ៍ធ្លាប់ឃើញក្នុងខ្សែភាពយន្ត "
            "បានកើតឡើងពិតៗនៅកម្ពុជាក្នុងទឹកដីនៃតំបន់ x-១៦ ក្នុងឃុំទន្លូង ស្រុកមេមត់ ខេត្តត្បូងឃ្មុំ នាថ្ងៃទី២០ មិថុនា ឆ្នាំ១៩៧៧ ដែលជាការចាប់ផ្តើមបេសកកម្មដាក់ជីវិតផ្ទាល់ខ្លួនធ្វើជាដើមទុន "
            "ដើម្បីប្តូរយកជីវិតខ្មែរមួយនគរដែលកំពុងឈរនៅពីមុខជ្រោះមរណៈនិងកំពុងបួងសួងរកអ្នកជួយសង្គ្រោះ។សម្តេចតេជោ ហ៊ុន សែន គឺជាតួអង្គពិតក្នុងបេសកកម្ម «សំណាងមួយក្នុងមួយម៉ឺនគ្រោះថ្នាក់» នេះ។ នៅម្ខាង គឺជាវាលពិឃាដនៃរបបប្រល័យពូជសាសន៍ដែលកាប់សម្លាប់មនុស្សគ្មានត្រាប្រណី រីឯនៅម្ខាងទៀត "
            "គឺជាព្រំដែនប្រទេសជិតខាងដែលកងទ័ពខ្មែរក្រហមធ្លាប់បើកការវាយប្រហារជារឿយៗ។ ស្ថានភាពនេះ មិនខុសពី «ចុះទឹកក្រពើឡើងលើខ្លា» នោះឡើយ។ ប៉ុន្តែ ដោយអំណាចនៃទឹកចិត្តស្នេហាជាតិដ៏មោះមុត "
            "កុលបុត្រខ្មែរដ៏ឆ្នើមរូបនេះ មិនញញើតឡើយក្នុងការប្រថុយជីវិតដើម្បីបុព្វហេតុរំដោះជាតិពីក្រញាំបិសាចអាវខ្មៅ។ក្រោយឆ្លងកាត់ឧបសគ្"
            "គរាប់សែនលានជំពូក ចលនាតស៊ូរំដោះជាតិក៏ត្រូវបានបង្កើតឡើងនៅថ្ងៃទី១២ ឧសភា ១៩៧៨។ បន្ទាប់មក រណសិរ្ស២ធ្នូ ក៏បានកកើតឡើងក្នុងឆ្នាំដដែលរហូតឈានដល់ជ័យជំនះថ្ងៃ៧ មករា ឆ្នាំ១៩៧៩ "
            "ដែលបានសង្គ្រោះជីវិតខ្មែរគ្រប់គ្នាឱ្យរស់រានមានជីវិតដូចក្តីប្រាថ្នា។ ទោះបីបេសកកម្មទាមទារសិទ្ធិរស់រានមានជីវិតបានទទួលជោគជ័យ ប៉ុន្តែ សម្តេចតេជោ ហ៊ុន សែន "
            "និងឥស្សរជនគណបក្សប្រជាជនកម្ពុជាបន្តរែកពន់នូវអម្រែកដ៏សែនធ្ងន់នៅលើស្មា ពីព្រោះប្រទេសជាតិទាំងមូលត្រូវបានបំផ្លាញខ្ទេចខ្ទាំទាំងហេដ្ឋារចនាសម្ព័ន្ធសង្គម ទាំងធនធានមនុស្ស។ ដៃម្ខាងខំប្រឹងកសាងប្រទេសពីគំនរផេះផង់ "
            "រីឯដៃម្ខាងទៀតប្រឹងទប់កុំឱ្យរបបប្រល័យពូជសាសន៍វិលវិញ។ដូច្នេះ បើយើងក្រឡេកថយក្រោយដើម្បីរំលឹកអំពីដំណើរឆ្ពោះទៅការរំដោះជាតិ "
            "និងដំណើរការកសាងជាតិឡើងវិញក្រោយរបបខ្មែរក្រហម រហូតសម្រេចបានសមិទ្ធផលជូនប្រទេសជាតិដូចសព្វថ្ងៃ យើងប្រាកដជាស្គាល់ច្បាស់ថា តើនរណាជាវីរជនសិទ្ធិមនុស្សពិតប្រាកដរបស់កម្ពុជា "
            "នរណាជាមហាវីរបុរសជាតិខ្មែរ នរណាជាបិតាស្ថាបនិកនិងប្រតិបត្តិករសន្តិភាព និងនរណាជាអ្នកសាងសមិទ្ធផលធំធេងអស្ចារ្យសម្រាប់ប្រទេសនេះដែលមិនធ្លាប់មានក្នុងប្រវត្តិសាស្ត្រសម័យ"
            "ទំនើបរយៈពេល៥០០ឆ្នាំចុងក្រោយ។ ទោះបីជាមានអ្នកខ្លះភ្លេច ឬធ្វើជាភ្លេចដោយសារតែហេតុផលនយោបាយងប់ងល់ជ្រុលនិយម ប៉ុន្តែ "
            "ពលរដ្ឋខ្មែរភាគច្រើនលើសលប់នៅចងចាំគ្មានថ្ងៃភ្លេចឡើយនូវព្រឹត្តិការណ៍ជាប្រវត្តិសាស្ត្រនេះ។សន្តិភាពនិងសមិទ្ធផលគ្រប់បែបយ៉ាងដែលកើតមានលើទឹកដីកម្ពុជាសព្វថ្ងៃ "
            "គឺជាស្នាដៃដឹកនាំរបស់រាជរដ្ឋាភិបាលគណបក្សប្រជាជនកម្ពុជាដែលមានសម្តេចតេជោ ហ៊ុន សែន ជាអតីតនាយករដ្ឋមន្ត្រី ដោយគ្មានអ្នកណាអាចកាឡៃបានឡើយ។ សមិទ្ធផលទាំងនេះ "
            "ត្រូវបានធានាការពារយ៉ាងគត់មុតដោយសម្តេចធិបតី ហ៊ុន ម៉ាណែត នាយករដ្ឋមន្ត្រីបច្ចុប្បន្ន ដែលកំពុងដឹកនាំប្រទេសឈានទៅសម្រេចចក្ខុវិស័យកម្ពុជាឆ្នាំ២០៥០ ក្លាយជាប្រទេសមានចំណូលខ្ពស់ "
            "ដែលនឹងក្លាយជាកំណត់ត្រាប្រវត្តិសាស្ត្រថ្មីមួយទៀតសម្រាប់កម្ពុជាសម័យទំនើប៕អត្ថបទដោយ ឯកឧត្តម ប៉ែន បូណា អ្នកនាំពាក្យរាជរដ្ឋាភិបាល     "),
    }

    article_url = "https://pressocm.gov.kh/archives/98694"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")
    category = "ទស្សនៈ-នយោបាយ"
    article = next(pressocm_spider.parse_data(article_response, category))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url
