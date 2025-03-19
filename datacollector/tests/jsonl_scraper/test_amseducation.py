"""Test Case For AMS Education Website Cambodia"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.amseducation import AMSEducationSpider

amseducation_spider = AMSEducationSpider()

def test_parse_data_asmeducation():
    """
    Test the parse_data method of ASMEducationSpider.

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
        "title": "យុវជន ប៊ិន ស៊ិនពុទ្ធិវង្ស ចាប់យកជំនាញវិទ្យាសាស្ត្រដំណាំ ដើម្បីជួយដោះស្រាយបញ្ហារបស់កសិករ​នៅសហគមន៍",
        "content" : ("ធំធាត់ឡើងដោយបានឃើញគំរូពីម្ដាយចូលចិត្តដាំដំណាំ "
                     "បង្កាត់ពូជកូនផ្កាអគីដេ រុក្ខជាតិលម្អ និងផ្កាផ្សេងៗដែលធ្វើយុវជនម្នាក់មកពីខេត្តពោធិ៍សាត់សម្រេចចិត្តជ្រើសរើសជំនាញវិទ្យាសាស្ត្រដំណាំដើម្បីសិក្សា "
                     "និងស្វែងយល់បន្ថែមអំពីដំណាំ។ នេះជាដំណើរដើមទង នៃការសិក្សាជំនាញវិទ្យាសាស្ត្រដំណាំរបស់យុវជន ប៊ិន ស៊ិនពុទ្ធិវង្ស និស្សិតកំពុងសិក្សាឆ្នាំទី៣ "
                     "នៃវិទ្យាស្ថានបច្ចេកវិទ្យាកំពង់ស្ពឺ។យុវជន ប៊ិន ស៉ិនពុទ្ធិវង្ស បានប្រាប់ AMS ថា ជំនាញវិទ្យាសាស្ត្រដំណាំនេះ គឺគេសិក្សាអំពី សត្រូវដំណាំដូចជា សត្វល្អិតចង្រៃ "
                     "ពពួកមេរោគ (ផ្សិត បាក់តេរី​វីសុស) និងសិក្សាលើការធ្វើរបាយការផ្សិត ការបង្កាត់ពូជ ការបណ្ដុះជាលិកាជាដើម។ ស៉ិនពុទ្ធិវង្ស បន្ថែមថា ការដែល​ខ្លួន​សម្រេចចិត្តរៀនជំនាញនេះ "
                     "ព្រោះខ្លួនបានឃើញម្ដាយដាំដំណាំនៅផ្ទះ និងបង្កាត់ពូជរុក្ខជាតិជាច្រើននៅផ្ទះដែលធ្វើឱ្យខ្លួនចង់ចេះ ចង់ដឹងអំពីជំនាញនេះបន្ថែម ហើយក៏យល់ឃើញថា "
                     "បើមានចំណេះជំនាញមួយនេះច្បាស់លាស់ នឹងអាចជួយដល់កសិករនៅក្នុងសហគមន៍ ដោះស្រាយបញ្ហាដែលពួកគាត់ជួបប្រទះ។ចំពោះការសម្រេចចិត្តរៀននៅវិទ្យាស្ថានបច្ចេកវិទ្យាកំពង់ស្ពឺ "
                     "យុវជនអាយុ២១ឆ្នាំរូបនេះ បានរៀបរាប់ថា ក្រោយទទួលបានលទ្ធផលមិនល្អក្នុងការ​ប្រឡង​សញ្ញាបត្រមធ្យមសិក្សា​ទុតិយភូមិ ខ្លួនបានស្វែងរកសាលារៀនជំនាញផ្នែកកសិកម្មដែលជាក្ដីស្រមៃរបស់ខ្លួនតាំងពីតូច "
                     "ប៉ុន្តែសាលាកសិកម្មនៅក្នុងខេត្តពោធិ៍សាត់មិនមានជំនាញនេះ ក៏បន្តស្វែងរកនៅភ្នំពេញនិងតាមបណ្ដាខេត្តមួយចំនួន។ ជាចៃដន្យ ពុទ្ធិវង្ស "
                     "បានឃើញពីការផ្សព្វផ្សាយសិក្សាជំនាញវិទ្យាសាស្ត្រដំណាំនៅវិទ្យាស្ថានបច្ចេកវិទ្យាកំពង់ស្ពឺ និងកំពុងផ្ដល់អាហារូបករណ៍១០០%ផងនោះ ខ្លួនក៏សម្រេចចិត្តដាក់ពាក្យស្នើសុំអាហារូបករណ៍ដើម្បីសិក្សា។ "
                     "ក្នុងអំឡុងពេលសិក្សាឆ្នាំទី១ និងទី២ ពុទ្ធិវង្ស បានរៀនថ្នាក់បរិញ្ញាបត្ររង និងបានដាក់ពាក្យស្វ័យរិនប្រឡងថ្នាក់ទី១២។ នៅពេលសិក្សាដល់ឆ្នាំទី២ ពុទ្ធិវង្ស បានចុះហាត់ការងារនៅខេត្តត្បូងឃ្មុំ "
                     "ដែលការងារភាគច្រើន សិក្សាទៅលើការថែទាំដំណាំហូបផ្លែ ការថែទាំដំណាំត្រសក់ផ្អែម ដំណាំស្លឹក ដំណាំជលព្រឹក្ស ដូចជាប៉េងប៉ោះ ម្ទេសប្លោកជាដើម។ក្រោយចប់ឆ្នាំទី២ លទ្ធផលប្រឡងស្វ័យរិនក៏ជាប់ យុវជន "
                     "ពុទ្ធិវង្ស បានសម្រេចបន្តសិក្សា​ទៅថ្នាក់បរិញ្ញាបត្រវិទ្យាដំណាំនេះបន្ថែម។ មកដល់ពេលនេះ ត្រឹមឆ្នាំទី៣ ពុទ្ធិវង្ស ក៏ធ្លាប់ទទួលលឺពាក្យអ្នកជិតខាងគេលើកឡើងថា «រៀនកសិកម្មធ្វើអី បើរៀនចប់ធ្វើស្រែចម្ការដដែលហ្នឹង "
                     "គួរណាតែទៅរៀនជំនាញផ្សេងៗដែលមានលើទីផ្សារនានា» ប៉ុន្តែមតិទាំងនោះមិនបានបង្អាក់ចិត្តឱ្យ វង្ស បោះបង់រៀនជំនាញនេះឡើយ ព្រោះ វង្ស នៅតែបន្តសិក្សាជំនាញនេះដោយសារក្ដីស្រលាញ់ "
                     "និងមើលឃើញពីសារប្រយោជន៍នៃជំនាញនេះ។យុវជន ប៊ិន ស៉ិនពុទ្ធិវង្ស បានលើកឡើងបន្ថែមថា ការរៀនជំនាញវិទ្យាសាស្រ្តដំណាំកាលពីដំបូងៗ គឺធ្លាប់យល់ឃើញថា រៀនជំនាញនេះហត់ ក្ដៅ "
                     "និងពិបាកក្នុងការរៀន ព្រោះត្រូវ ប្រើប្រាជ្ញាផង ប្រើកម្លាំងច្រើនផង ប៉ុន្តែយ៉ាងណា ស៉ិនពុទ្ធិវង្ស អាចសម្របខ្លួនបានក្រោយសិក្សាបានកន្លះឆ្នាំ។ ជាក់ស្ដែងការរៀនជំនាញនេះ "
                     "ប្រើកម្លាំងតែតាមមុខជំនាញមួយចំនួនតែប៉ុណ្ណោះដែលត្រូវកាប់ដីសម្រាប់អនុវត្ត ឬពិសោធន៍ ចំណែកមុខវិជ្ជាផ្សេងៗត្រូវសិក្សាចំណេះដឹងទូទៅដូចជំនាញដទៃដែរ។បច្ចុប្បន្ននេះ យុវជន "
                     "ពុទ្ធិវង្ស កំពុងសិក្សាឆ្នាំទី៣ និងមានតួនាទីជាប្រធាន និងជាអ្នកមើលការខុសត្រូវកន្លែងស្នាក់នៅខាងអន្តេវាសិកដ្ឋាន។ ពុទ្ធិវង្ស បន្ថែមថា ក្រោយបញ្ចប់ជំនាញនេះ អ្នកសិក្សាអាចចេញទៅខាង "
                     "Lap ក្នុងការពិសោធន៍ទាក់ទងទៅនឹងផ្នែកគុណភាពផ្សេងៗ អាចធ្វើការតាមដេប៉ូផ្នែកលក់ជីកសិកម្ម ឬថ្នាំកសិកម្ម និងការប្រឡងដាក់ពាក្យធ្វើជាគ្រូកសិកម្ម ឬមន្ត្រីកសិកម្ម។ជារួមយុវជន ប៊ិន ស៉ិនពុទ្ធិវង្ស "
                     "យល់ឃើញថា សម្រាប់អ្នកដែលចង់សិក្សាជំនាញផ្សេងៗដែលទាក់ទងនឹងផ្នែកកសិកម្ម ឬជំនាញវិទ្យាសាស្ត្រកសិកម្ម សូមតាំងចិត្តសិក្សាឱ្យបានជាប់លាប់ និងច្បាស់លាស់ព្រោះអាចជួយឱ្យអ្នករៀនមានជំនាញច្បាស់លាស់ "
                     "ជួយខ្លួនឯងឱ្យមានការងារច្បាស់លាស់ និងត្រឹមត្រូវសម្រាប់ផ្គត់ផ្គងខ្លួនឯង និងគ្រួសារនាពេលអនាគត៕")
    }

    article_url = "https://education.ams.com.kh/skills-project/news/bankrupt-but-young-bin-sin-puthivong-still-embraces-crop-science-skills-to-achieve-his-dream-of-agricultural-skills"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(amseducation_spider.parse_data(article_response))

    assert "ជំនាញ" in article["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_asmeducation():
    """
    Test the parse method of ASMEducationSpider.

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
        - The number of article links (excluding the next page link) is 9.
        - The 10th link is the URL for the next page.
        - The next page URL matches the expected URL.
    """

    category_url = "https://education.ams.com.kh/category/all-news/news-skill-project/"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = amseducation_spider.parse(category_response)

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
    assert links[10] == "https://education.ams.com.kh/category/all-news/news-skill-project/page/2"
