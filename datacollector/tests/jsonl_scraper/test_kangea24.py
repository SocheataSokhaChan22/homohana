"""Test Case For Kangea24 website"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.kangea24 import Kangea24Spider
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle

knagea24_spider = Kangea24Spider()
pagination_handle = PaginationHandle()


def test_parse_data_kangea24():
    """
    Test the `parse_data` method of the `Kangea24Spider` spider.

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
        "category": "ព័ត៌មានជាតិ",
        "title": "រឿងភ្នំពេញលិចទឹក៖ តើគួរដោះស្រាយដោយរបៀបណា?",
        "content": "\n                            រឿង​លិច​រាជធានី និង​ទីក្រុង​នៅ​ពេល​ភ្លៀង​ធ្លាក់​ខ្លាំង គឺជា​រឿង​ធម្មតា​នៅ​អាស៊ាន ។ រឿង​ទីក្រុង មួយ​លិច​ទឹក​វា​មិន​សាមញ្ញ​ដូច​យើង​គិត​ឡើយ ។ "
        "គម្រោង​អភិ​វ​ឌ្ឈ​ន៍​ហេដ្ឋារចនាសម្ព័ន្ធ​ធ្វើ​អោយ​រាជធានី​ភ្នំពេញ​លែង​លិច​នៅ​ពេល​ភ្លៀង​ខ្លាំង​នៅ​ក្នុង​រយៈពេល​ខ្លី​គឺ​ពិតជា​ពិបាក​នឹង​ធ្វើ​អោយ​សម្រេច ទោះបីជា​អាជ្ញាធរ​មានការ​តាំងចិត្ត​ដោះ​ស្រា​យ​ក្តី​ ។\n\n                        ថ្មីៗ​នេះ "
        "មានការ​លើក​ឡើង​នូវ​ការ​ប្តេជ្ញា​ចិត្ត​ដាក់​ចេញ​នូវ​ផែនការ​ផ្សេង​ៗ​សំដៅ​ធ្វើ​យ៉ាងណា​លែងអោយ​រាជធានី​ភ្នំពេញ ស្ថិត​នៅ​ក្នុង​ស្ថានភាព​លិចលង់​ជា​បន្ត​ទៀត ហើយ​ពលរដ្ឋ​ក៏​បាន​ចេញ​មក​សាទរ "
        "និង​អបអរ​ហើយ​លើកទឹកចិត្ត​អោយ​គម្រោង​នេះ​អនុវត្ត​អោយ​បាន​លឿន​តាម​ដែល​អាច​ធ្វើ​ទៅ​បាន ពីព្រោះ​នៅ​ពេល​នេះ អោយ​តែ​ភ្លៀង​ធ្លាក់​មក​នរណា​ក៏​បារម្ភ​ពី​រឿង​លិច​ផ្លូវ លិច​ផ្ទះ​ផង​ដែរ "
        "។នៅ​ពេល​នេះ​អ្នក​នៅ​រាជធានី​សុទ្ធតែ​មាន​អារម្មណ៍​ដូច​ៗ​គ្នា​ថា «​ផ្ទះ​អញ​មិនដឹង​យ៉ាងណា​ទេ​? ឫ​អញ​ត្រូវធ្វើ​ដំណើរ​តាម​ផ្លូវ​ណា​កុំអោយ​ស្ទះ​ហើយ​លិច​ទឹក​? » នៅ​ពេល​ដែល​ឃើញ​មេឃងងឹត "
        "ទោះជា​ពេល​កំពុង​តែ​ធ្វើការ​ក៏​បែក​អារម្មណ៍​ដែរ​ដោយសារ​ភ័យ​ខ្លាច​ការ​លិច​ផ្ទះ ការ​លិច​ផ្លូវ និង​ការ​កកស្ទះ​ចរាចរណ៍ ។ដូច្នេះ​ហើយ​នៅ​ពេល​ដែល​បាន​ឭ​គម្រោង​ទាំងនេះ យើង​ក៏​រីករាយ "
        "និង​រង់ចាំ​ទទួល​យ​ផង​ដែរ ។ ពីព្រោះ​នរណា​មិន​សប្បាយ បើ​រាជធានី​លែង​លិច​ទឹក ដូច្នេះ​យានយន្ត​ក៏​លែង​ខូច​ផ្ទះ​ក៏​លែង​លិច លែង​បោស​លែង​សំអាត​អត់​ដេក​អត់​ពួន ។ "
        "ប៉ុន្តែ​យើង​ទាំងអស់​គ្នា​ត្រូវ​តែ​ត្រៀម​ចិត្ត​ទុក​អោយ​ហើយ​ថា វា​មិនមែន​ងាយស្រួល​ដូច​ថា នោះ​ឡើយ ។មក​ដល់​ពេល​នេះ រាជធានី​ភ្នំពេញ​អាច​ចាត់​ចូល​ជា "
        "រាជធានី​ចំណាស់​មួយ​នៅ​ក្នុង​តំបន់​ដែល​មាន​ប្រព័ន្ធ​លូ​ទ្រុឌ​ទ្រាម​ច្រើន​ដូច​ជាទី​ក្រុង​នានា​នៅ​ក្នុង​តំបន់​ដែល​រួម​មាន ហាណូយ ហូ​ជី​មិ​ញ បាងកក ហ្សា​កា​តា ហើយ​សូ​ម្បី​តែ​ទីក្រុង​សាំង​ហ្គា​ពួរ ជាដើម​ដែល​មាន "
        "ហេ​ដ្ឋា​រ ច​នា​ស​ម្ពូ័​ន្ធ គ្រប់គ្រង​បញ្ហា​នេះ​បាន​ល្អ​ជាងគេ និង​ទំនើប​ជាងគេ​នោះ ក៏​បាន​លិច​ទឹក ជា​បន្តបន្ទាប់​មក​ដែរ​នៅ​ប៉ុន្មាន​ឆ្នាំ​ចុង​ក្រោយ​នេះ ។នៅ​កម្ពុជា​យើង សម្រាប់​រាជធានី "
        "បើ​តាម​របាយការណ៍​ពី​មន្ទីរ​សាធារណការ និង​ដឹក​ជញ្ជូន រាជធានី​ភ្នំពេញ​គឺ​ត្រូវធ្វើ​ការងារ​ច្រើន​ណាស់ ដើម្បី​ដោះស្រាយ​បញ្ហា​លិចលង់ ដោយ​ជំនន់​ទឹកភ្លៀង ។ គិត​មក​ដល់​ពេល​នេះ "
        "ប្រព័ន្ធ​លូ​ជាង​៩២៤​គីឡូម៉ែត្រ​ត្រូវ​បាន​ស្ថាបនា ហើយ​ការ​ស្ថាបនា​នេះ​នឹង​ត្រូវធ្វើ​ឡើងជា​បន្តបន្ទាប់​ទៀត ដោយសារ​តែ​ទីក្រុង​រីក ហើយ​កន្លែង​ខ្លះ​គ្មាន​ប្រព័ន្ធ​លូ​នៅឡើយ រីឯ​លូ​ខ្លះ​ទៀត​តូច ហើយ​បែក​ដោយ​កន្លែង​ថែម​ទៀត "
        "។ មាន​របាយការណ៍​ថា រាជធានី​បាន​ដោះស្រាយ​បញ្ហា​លិចលង់​បាន​ចំនួន​៣២​កន្លែង​ហើយ ប៉ុន្តែ​មិនមែន​មិន​អោយ​លិច​ទេ គឺ​លិច​ដែរ​តែ​លិច​រយៈពេល​ខ្លី​ដោយ​សម្រួលការ​ហូរ​ចេញ​វិញ​លឿន​ប៉ុណ្ណោះ "
        "ជាក់ស្តែង​ដូច​ជា​នៅ​ផ្សារ​កណ្តាល​ជាដើម ក៏​នៅ​តែ​លិច​ដដែល​ទេ ទោះជា​ជប៉ុន​បាន​ជួយ​កសាង​ប្រព័ន្ធ​លូ​ជា​បន្តបន្ទាប់​ក៏​ដោយ គ្រាន់តែ​ក្រោយ​ពេល​ភ្លៀង "
        "វា​ស្រក​លឿន​ជាង​មុន​ប៉ុណ្ណោះ ។នៅ​ពេល​នេះ បើ​តាម​សេចក្តីរាយការណ៍​មួយ​ចំនួន​បានអោយ​ដឹង​ថា អ្នកជំនាញ​កម្ពុជា​បាន​កំពុង​តែ​ធ្វើ​កិច្ចការ​នេះ​ហើយ ដោយ​ក្រសួង​ធនធានទឹក "
        "និង​ឧតុនិយម​កំពុង​តែ​សហការ​ជាមួយនឹង​ក្រសួង​សេដ្ឋកិច្ច និង​ហិរញ្ញវត្ថុ ព្រមទាំង​បណ្តា​ដៃគូ​អភិវឌ្ឍន៍​ជា​ច្រើន​ទៀត "
        "និង​អ្នក​ដែល​ពាក់ព័ន្ធ​ដោយ​រួម​ទាំង​អាជ្ញាធរ​រាជធានី​ភ្នំពេញ​ផ្ទាល់​ស្តី​ពី​ការងារ​រំដោះ​ទឹកជំនន់ ដែល​ជា​ជំនន់​ទឹកភ្លៀង​ក្នុងភូមិ​សាស្ត្រ​រាជធានី​ភ្នំពេញ​។ អ្នកជំនាញ​កម្ពុជា​បាន​កំពុង​តែ​ជំរុញ​ផែនការ​រយៈពេល​មធ្យម ដើម្បី​ធ្វើ​ទំនើប​កម្ម​វិស្វកម្ម​លើ​ប្រព័ន្ធ​រំដោះ​ទឹក​ទាំងឡាយ "
        "ដើម្បី​ធ្វើ​ឱ្យ​ធូរស្រាល​នូវ​ទឹកជំនន់​គ្រប់​ប្រភេទ​ក្នុង​រាជធានី​ភ្នំពេញ និង​ទីក្រុង​រណប​បាន​នៅ​ក្នុង​រយៈពេល​ពី​១៥​ទៅ​២០​ឆ្នាំ ។ "
        "តាម​ការ​លើក​ឡើង​ពី​សំណាក់​ក្រុម​មន្ត្រី​ដែល​ពាក់ព័ន្ធ​នឹង​គម្រោង​បាន​ឲ្យ​ដឹង​ថា គម្រោង​នេះ គឺ​អាច​នឹង​ដំណើរការ​នៅ​ក្នុង​ពេល​ឆាប់​ៗ ហើយ​បញ្ហា​នេះ គឺជា​បញ្ហា​អាទិភាព​មួយ "
        "ប៉ុន្តែ​ទន្ទឹម​នេះ​ប្រជាពលរដ្ឋ​ក៏​កុំ​សុទិដ្ឋិនិយម​ពេក​ដែរ ។ដរាបណា​ប្រជាពលរដ្ឋ​នៅ​តែ​មាន​កំណើន ទីក្រុង​នៅ​តែ​រីក ហើយ​ការ​ប្រែប្រួល​អាកាសធាតុ នៅ​តែ​ចោទ ក្រៅពី​អាជ្ញាធរ​គិត "
        "យើង​ខ្លូ​ន​យើង​ក៏​ត្រូវ​តែ​គិត​ខ្លួនឯង​ហើយ​ក៏​ត្រូវ​ចូលរួម ពីព្រោះ​វា​មិនមែន​ជា​បញ្ហា​តែ​អាជ្ញាធរ​ដែរ ។ ដើម្បី​គេច​ចេញពី​បញ្ហា​លិចលង់​នេះ រាល់​គម្រោង​សង់ផ្ទះ "
        "ឬ​អភិ​វ​ឌ្ឈ​ន៍​នានា​ត្រូវ​រិះគិត​អំពី​បញ្ហា​ប្រព័ន្ធ​លូ នេះ​អោយ​ច្បាស់លាស់ ហើយ​ម្យ៉ាងវិញទៀត​ក៏​កុំ​ភ្លេច​គិត​អំពី​កម្រិត​នី​វូ​ត្រូវ​លិចលង់​នេះ​អោយ​ខ្ពស់​អោយ​ហើយ "
        "ដើម្បី​បង្ការ​បញ្ហា​ទុកជា​មុន ៕ ដោយៈ ហេង ចេស្តារដកស្រង់ពី៖  ",
        }

    article_url = "https://kangea24.com/news-details/164"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(knagea24_spider.parse_data(article_response, category="ព័ត៌មានជាតិ"))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_kangea():
    """
    Test the `parse` method of the `Kangea24Spider` spider.

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

    category_url = "https://kangea24.com/categories/6"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = knagea24_spider.parse(category_response)

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
    assert len(links) - 1 == 20
    assert links[20] == next_page
    assert links[20] == "https://kangea24.com/categories/6?page=2"
