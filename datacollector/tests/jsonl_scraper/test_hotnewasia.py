"""Test Case For Hot New Asia"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.hotnewsasia import HotnewsasiaSpider

hotnewasiaSpider = HotnewsasiaSpider()

def test_parse_data_hotnewasia():
    """
    This function is used to test the parse data method of HotnewsasiaSpider.
    This checks to see if the filtering works correctly.
    This test is conducted using live data from the website.

    Note: The filtering mainly focuses on the URL.

    Attribute
    ---------
    article_url:
        The URL of the article to be scraped.
    article_response:
        live response generated from article url
    article: dict
        desired output (should be parsed)
    expected_value (dict):
        Expected result of the parsed data.
    """
    expected_value = {
        "category": ["ព័ត៌មានជាតិ"],
        "title": "រដ្ឋមន្ត្រី អ៊ាង សុផល្លែត៖ ថ្នាក់ដឹកនាំជាអ្នកស្នេហាជាតិ យកជីវិតទៅលះបង់ ដើម្បីសុខសន្តិភាព ការពារបូរណភាពទឹកដី និងអភិវឌ្ឍប្រទេសឲ្យរីកចម្រើន",
        "content": " នៅក្នុងជំនួបជាមួយថ្នាក់ដឹកនាំនិងមន្រ្តីរាជការនៃមន្ទីរបរិស្ថានខេត្តតាកែវ កាលពីថ្ងៃទី១៤ ខែសីហា ឆ្នាំ២០២៤ ឯកឧត្តមបណ្ឌិត អ៊ាង សុផល្លែត រដ្ឋមន្រ្តីក្រសួងបរិស្ថាន "
        "បានថ្លែងថាទង្វើជ្រុលនិយមរបស់ក្រុមប្រឆាំងក្រៅច្បាប់ គឺបង្ហាញពីការក្បត់ជាតិ ក្បត់ប្រជាជនខ្មែរយើង ដោយធ្វើវិច្ឆេទកម្មសេដ្ឋកិច្ចរបស់កម្ពុជាយើង។ជាមួយគ្នានេះ ឯកឧត្តម បានលើកឡើងថាឯកឧត្តម គឺជាសាក្សីរស់ "
        "ធ្លាប់បំពេញការងារជូនសម្តេចអគ្គមហាសេនាបតីតេជោ ហ៊ុន សែន ប្រធានព្រឹទ្ធសភា និងជាប្រធានគណបក្សប្រជាជនកម្ពុជា ប្រមាណ២៦ឆ្នាំ ហើយបានកត់ត្រារឿងរ៉ាវទាំងអស់ ទុកជាប្រវត្តិសាស្រ្តថែមទៀតផង។ ឯកឧត្តមបណ្ឌិត អ៊ាង សុផល្លែត "
        "បានបញ្ជាក់ថា ទឹកចិត្តរបស់សម្តេចតេជោ គឺ ការតស៊ូ ការលះបង់ ដើម្បីកម្ពុជាយើង។កុំថាឡើយដីទៅ៤ខេត្ត សូម្បីមូសទៅមណ្ឌលគីរី ក៏មិនឱ្យទៅខាំប្រជាជនយើងផង។ យើងចែកមុងនៅទីនោះ "
        "មិនមែនត្រឹមតែការពារគាត់ពីជំងឺគ្រុនចាញ់នោះទេ គឺការពារគាត់ មានសុខភាពល្អ ត្រៀមទទួលការអភិវឌ្ឍនៅតំបន់នោះ ចូលរួមចំណែកកសាង ពង្រឹងតំបន់នោះ ការពារតំបន់នោះ ។ "
        "នេះជាការលើកឡើងបន្ថែមរបស់ឯកឧត្តមរដ្ឋមន្រ្តីក្រសួងបរិស្ថាន។សូមបញ្ជាក់ថា នៅប៉ុន្មានថ្ងៃខាងមុខ ក្រសយងបរិស្ថាន បានទទយលអំណោយពីលោកជំទាវបណ្ឌិត ពេជ ច័ន្ទមុន្នី ហ៊ុនម៉ាណែត ដើម្បី "
        "ចែកជូនប្រជាពលរដ្ឋនៅខេត្តមណ្ឌលគីរី ធ្វើយ៉ាងណាឱ្យពួកគាត់ មានសុខភាពល្អ ធ្វើយ៉ាងណា ឱ្យកូនចៅគាត់ បានរៀនសូត្រមានចំណេះដឹង ចំណេះធ្វើ ត្រៀមទទួលការវិនិយោគមកដល់តំបន់នោះ។ឯកឧត្តមរដ្ឋមន្រ្តីបានបន្ថែមថា "
        "ពួកអគតិក្រៅច្បាប់ កំពុងចង់ឱ្យប្រទេសយើងធ្លាក់ចុះ ពួកអគតិទាំងនោះ ចង់ឱ្យយើងបាត់បង់សេដ្ឋកិច្ច ឱ្យយើងបាត់បង់ការប្រកួតប្រជែង ដើម្បីកុំឱ្យមានការអភិវឌ្ឍនៅតាមតំបន់ពជាប់ព្រំដែនទាំងនោះ។ "
        "ពួកគាត់ចង់ឱ្យគេយកដីរបស់ខ្មែរយើងនេះឯង។\n«តាមពិត ពួកគាត់មានការស៊ុមគ្រលុំគ្នា ដើម្បីបង្កបញ្ហានៅក្នុងសង្គមកម្ពុជា ពួកគាត់ទាំងអស់នោះទេ ដែលចង់ឱ្យមានការបាត់បង់ទឹកដីនោះ។ ពួកគាត់ទេ "
        "ដែលបានចុះហត្ថលេខា ជាមួយ កុក ស ប្រគល់ដីឱ្យគេ។»ឯកឧត្តម បណ្ឌិត អ៊ាងសុផល្លែតមានប្រសាសន៍បន្ថែម។ក្នុងឱកាសនោះដែរ ឯកឧត្តមរដ្ឋមន្រ្តី បានអំពាវនាវដល់មន្រ្តី "
        "ក្រុមគ្រួសារបរិស្ថាន គិតឱ្យបានស៊ីជម្រៅមែនទែន កន្លងមកក្រសួងបរិស្ថានមិនមែនធ្វើការការពារធនធានធម្មជាតិតែមួយនោះទេ យើងបានការពារនិងអភិរក្សធនធានធម្មជាតិ "
        "គឺយើងបានការពារទឹកដីរបស់យើង ដូចគ្នាដែរ។ ឯកឧត្តមបាន បានប្រកាសគាំទ្រចំពោះកិច្ចសហប្រតិបត្តិការតំបន់អភិវឌ្ឍន៍ត្រីកោណ ដែលជាកិច្ចសហប្រតិបត្តិការមួយដ៏ល្អ "
        "សម្រាប់ការអភិវឌ្ឍតំបន់ជាប់ព្រំដែន និងសេដ្ឋកិច្ចជាតិ ហើយគ្មានការគំរាមកំហែងសម្រាប់បូរណភាពទឹក ឬអធិបតេយ្យជាតិនោះឡើយ៕    ",
    }
    article_url = "https://www.hotnews-asia.com/detail/362274"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(hotnewasiaSpider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_pressocm():
    """
    This function is used to test the parse_pressocm method of HotnewsasiaSpider.
    This checks to see if the filtering works correctly.
    
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
    url_parts:
        A list of URL parts extracted from the category page.
    next_page_url (str):
        The URL of the next page after pagination.
    """
    category_url = "https://www.hotnews-asia.com/detail/category/national"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = hotnewasiaSpider.parse(category_response)

    """
    testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    url_parts = category_response.url.rstrip("/").split("/")

    if url_parts[-1].isdigit():
        url_parts[-1] = str(int(url_parts[-1]) + 1)
    else:
        url_parts.append("page/2")

    next_page_url = "/".join(url_parts)

    assert len(links) - 1 == 15
    assert links[15] == next_page_url
    assert links[15] == "https://www.hotnews-asia.com/detail/category/national/page/2"
