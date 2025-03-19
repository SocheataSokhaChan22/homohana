"""Test Case For Biz Cambodia News"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.bizcambodia import BizcambodiaSpider
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle

bizcambo_spider = BizcambodiaSpider()
pagination_handle = PaginationHandle()

def test_parse_data_bizcambodia():
    """
    Test the parse_data method of `BizcambodiaSpider`.

    Attributes:
    -------------
    article_url (str):
        URL of the article to be tested.
    article_response (HtmlResponse):
        The response object for the article URL.
    article_result (list):
        Parsed data from the article page.
    expected_value (dic):
        Expected result of the parsed data.

    Assertions:
        - The 'title' field of the parsed article is not empty.
        - The 'content' field of the parsed article is not empty.
        - The 'url' field of the parsed article is not empty.
    """
    expected_value = {
        "category": "\n                            ការងារ\n                        ",
        "title": "បុគ្គលិក ៣៤ លាន​នាក់​ប្រាប់​ហេតុផល ៤​ដែល​អ្នក​ត្រូវ​លាឈប់​ពី​ការងារ​នៅ​ពេល​ឥឡូវ​នេះ​",
        "content": (
            "តើ​អ្នក​ធ្លាប់​លា​ឈប់​​ពី​ការងារ​ដែរ​ទេ? ប្រសិន​បើ​​ធ្លាប់ នោះ​មានន័យ​ថា មិនមែន​មានតែ​អ្នក​ម្នាក់​ឯង​នោះ​ឡើយ។ បើ​យោង​តាម​​"
            "ការ​ស្រាវជ្រាវ​របស់​ក្រុមហ៊ុន​ប្រឹក្សា​ផ្នែក​ធនធាន​មនុស្ស Mercer ​កាល​ពី​ឆ្នាំ ២០១៩ កន្លង​ទៅ​បាន​រក​ឃើញ ថា មាន​បុគ្គលិក "
            "១ភាគ៣​មាន​គម្រោង​លាឈប់​ពី​ការងារ​នៅ​ក្នុង​រយៈពេល ១២ ខែ​ខាងមុខ។ ចំនួន​នេះ​ពិត​ជា​មិន​ធម្មតា​ទេ។តើ​នេះ​បណ្តាល​មក​ពី​"
            "អ្វី? ហេតុ​អ្វី​បាន​ជា​ពួកគេ​មាន​គម្រោង​​លា​ឈប់ ពី​ក្រុមហ៊ុន​យ៉ាង​ច្រើន​បែប​នេះ? ក្រុមហ៊ុន Peakon បាន​បកស្រាយ​ចម្ងល់​នេះ​ដោយ​បាន​សិក្សា​"
            "ស្រាវជ្រាវ​លើ​បុគ្គលិក ៣២ លាន​នាក់ ហើយ​លទ្ធផល​បាន​បង្ហាញ​មូលហេតុ ៤ សំខាន់ៗ​ខាងក្រោម​នេះ​​ដែល​ធ្វើ​ឲ្យ​ពួកគេ​លាឈប់ ពី​ការងារ​។១.ការងារ​មិន​មាន​ការ​ប្រកួតប្រជែង​ខ្លាំងគ្មាន​នរណា​ម្នាក់​ចង់​ចំណាយ​ពេល​ ៨ ទៅ​ ៩​ម៉ោង​ក្នុង​មួយ​ថ្ងៃ​នៅ​​កន្លែង​ការ​ដោយ​មាន​អារម្មណ៍​"
            "ធុញថប់ គ្មាន​ការ​ខិតខំ​ប្រឹងប្រែង ហើយ​ការងារ​មិន​សូវ​មាន​ការ​ប្រកួតប្រជែង​ខ្លាំង​​នោះ​ឡើយ។ អ្នក​ត្រូវ​​សកម្ម​​ក្នុង​ការងារ ត្រូវការ​ប្រកួតប្រជែង ហើយ​ត្រូវ​ការ​សមិទ្ធផល​ដែល​កើត​ចេញ​ពី​ការ​ខិតខំ​ប្រឹងប្រែង​របស់​អ្នក។ បើ​យោង​តាម​របាយការណ៍ Peakon  បាន​លើកឡើង​ថា​ ការ​ធ្វើ​ឲ្យ​បុគ្គលិក​មាន​អារម្មណ៍​ថា ពួកគេ​​បាន​រួមចំណែក​ដល់​សមិទ្ធផល​ការងារ គឺ​ជា​កូនសោ​ដ៏​សំខាន់​ធ្វើ​ឲ្យ​បុគ្គលិក​ខិតខំ​បំពេញ​ការងារ​កាន់តែ​ខ្លាំង "
            "និង​មាន​អារម្មណ៍​កក់ក្ដៅ។ ២.ការ​​ចរចា​រឿង​ដំឡើង​​ប្រាក់ខែ​ជាមួយ​ថ្នាក់​លើ​វា​មិន​អាច​ទៅ​រួចទោះបី​ជា​​អ្នក​មិន​ត្រូវការ​លុយ​នៅ​​ក្នុង​ស្ថានភាព​ខ្លះ​ក៏ដោយ ក៏​ប៉ុន្តែ​វា​នៅ​តែ​សំខាន់​ខ្លាំង​ណាស់​សម្រាប់​មនុស្ស​គ្រប់​រូប​។អ្នក​មិន​មែន​ត្រូវការ​វា​ដើម្បី​តែ​បង់​ថ្លៃ​ការ​ចំណាយ​ប្រចាំ​ថ្ងៃ​របស់​អ្នក​ប៉ុណ្ណោះ​ទេ ក៏"
            "ប៉ុន្តែ​អ្នក​ក៏​ត្រូវ​ធ្វើ​ឲ្យ​ខ្លួន​ឯង​មាន​តម្លៃ និង​មាន​ឥទ្ធិពល​នៅ​ក្នុង​ក្រុមហ៊ុន​របស់​អ្នក​ដែរ។ ដើម្បី​ធ្វើ​ឲ្យ​មាន​ភាព​យុត្តិធម៌​ទៅ នឹង​អ្វី​ដែល​អ្នក​បាន​ធ្វើ​ចំពោះ​ក្រុមហ៊ុន ការ​ចរចា​រឿង​ដំឡើង​ប្រាក់ខែ​ជា​មួយ​ថ្នាក់​លើ​គួរ​តែ​ត្រូវ​បាន​ធ្វើ​ឡើង​ដោយ​បើកចំហ។ ក៏ប៉ុន្តែ​រឿង​នេះ ​ពេល​ខ្លះ​វា​មិនមែន​សុទ្ធតែ​អាច​"
            "ធ្វើ​បាន​នោះ​ទេ។ នេះ​ហើយ​ជា​មូលហេតុ​ដែល​ធ្វើ​ឲ្យ​របាយការណ៍ Peakon លើកឡើង​ថា វា​ជា​រូបភាព​មួយ​ធ្វើ​ឲ្យ​បុគ្គលិក​កាន់តែ​ឃ្លាតឆ្ងាយ និង​មាន​អារម្មណ៍​ចង់​លាឈប់​ពី​ក្រុមហ៊ុន។៣.​មិន​មាន​​អារម្មណ៍​​ល្អ​ជាមួយ​​អ្នក​គ្រប់គ្រងការ​ទំនាក់ទំនង​ល្អ​បំផុត​របស់​នៅ​ក្នុង​ចំណោម​ការ​ទំនាក់"
            "ទំនង​ផ្សេងៗ​ទៀត​នៅ​កន្លែង​ការងារ គឺ​​ការ​ទំនាក់ទំនង​រវាង​អ្នក​ និង​អ្នក​គ្រប់គ្រង​របស់​អ្នក។ ដូច្នេះ​ប្រសិន​បើ​ទំនាក់ទំនង​មួយ​នេះ វា​មិន​រលូន​ទេ​នោះ សញ្ញាណ​ភ្លើង​​ខៀវ​នៃ​ការ​ដើរ​ចេញ​របស់​បុគ្គលិក​មាន​កាន់តែ​ច្រើន​ឡើង។ បើ​​យោង​តាម​របាយការណ៍ Peakon ប្រសិន​បើ ​បុគ្គលិក​មិន​"
            "មាន​អារម្មណ៍​ល្អ​ជាមួយ​អ្នក​គ្រប់គ្រង​របស់​ខ្លួន​ទេ ពួកគេ​នឹង​​​ចាប់​ផ្តើម​ដក​ខ្លួន​កាន់តែ​ឆ្ងាយ​បន្តិចម្តងៗ​ពី​​អ្នក​គ្រប់គ្រង​នោះ។ ទន្ទឹម​នឹង​នេះ​ប្រសិន​បើ​​អ្នក​គ្រប់គ្រង​មិន​ព្យាយាម​ដោះស្រាយ​បញ្ហា​នេះ​ទេ ​បុគ្គលិក​របស់​ខ្លួន​នឹង​ស្វែង​រក​ឱកាស​ការងារ​ថ្មី​នៅ​កន្លែង​ផ្សេង។ ៤.មើល​មិន​ឃើញ​​"
            "ឱកាស​អភិវឌ្ឍ​សមត្ថភាព​របស់​ខ្លួនវា​ជា​រឿង​ធម្មតា​ទៅ​ហើយ​សម្រាប់​អ្នក​ដើម្បី​ធ្វើ​ការ​មិន​ត្រឹមតែ​យក​ប្រាក់​ខែ​មួយ​មុខ​ប៉ុណ្ណោះ​ទេ។ "
            "អ្នក​ត្រូវ​ការ​ភាព​លូតលាស់​នៅ​កន្លែង​ការងារ ចង់​បាន​បទពិសោធន៍​កាន់តែ​ច្រើន ចង់​ឲ្យ​សមត្ថភាព​កាន់តែ​​រីកចម្រើន​​ទៅ​មុខ "
            "ហើយ​ក៏​ចង់​ឲ្យ​ក្រុមហ៊ុន​កាន់តែ​រក​ចំណូល​បាន​ច្រើន។ ប៉ុន្តែ​នឹង​មាន​អ្វី​កើត​ឡើង​ប្រសិន​បើ​​សមត្ថភាព​របស់​​អ្នក​គ្មាន​ការ​អភិវឌ្ឍ​​? "
            "ចម្លើយ ការ​ចាកចេញ​គឺ​ជា​ជម្រើស​ដ៏​ល្អ​បំផុត​របស់​អ្នក៕អត្ថបទទាក់ទង៖ដោយ៖ ខេវិនប្រភព៖ Inc ​​​ ")
    }

    article_url = "https://www.bizkhmer.com/articles/76517"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(bizcambo_spider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_bizcambodia():
    """
    Test the parse method of `BizcambodiaSpider`.

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
    next_page (list):
        URL segments for constructing the next page URL.
    next_page_url (str):
        Constructed URL for the next page.

    Assertions:
        - The number of article links (excluding the next page link) is 20.
        - The 10th link is the URL for the next page.
        - The next page URL matches the expected URL.
    """

    category_url = "https://www.bizkhmer.com/categories/startup?page=2"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = bizcambo_spider.parse(category_response)

    """
    testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    next_page_url = pagination_handle.get_next_page_url_with_param(category_response.url)

    assert len(links) - 1 == 20
    assert links[20] == next_page_url
    assert links[20] == "https://www.bizkhmer.com/categories/startup?page=3"
