"""Test Case For Dersabay website"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.dersabay import DersabaySpider

dersabay_spider = DersabaySpider()

def test_parse_data_dersabay():
    """
    Test the `parse_data` method of the `DersabaySpider` spider.

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
    expected_value (dict):
        Expected result of the parsed data.
    """
    expected_value = {
        "category": "កន្លែង​កម្សាន្ត,សិង្ហបុរី,Travel and Fun",
        "title": "កុំឲ្យស្តាយ! ពេលទៅលេងសិង្ហបុរី មិនគួររំលងកន្លែងថតរូបស្អាតៗ ដោយមិនបាច់ចំណាយលុយ",
        "content": (
            "ដោយសារ​តែ​ភាព​ជឿន​លឿន ស្រស់​ស្អាត និង​មាន​សុវត្ថិភាព​ បាន​ធ្វើ​ឲ្យ​សិង្ហបុរី ក្លាយ​ជា​ប្រទេស​មួយ ដែល​អាច​​ទាក់ទាញ​ភ្ញៀវ​ទេសចរ​​បាន​យ៉ាង​ច្រើន​កុះករ។ ថ្វី​ដ្បិត​តែ​ប្រទេស​នេះ "
            "ផ្ញើ​ខ្លួន​នៅ​លើ​ដី​កោះ និង​មាន​ទំហំ​តូច​ត្រឹម ៧១៩,៩ គម២ ពិត​មែន ប៉ុន្តែ​​​វា​បាន​គ្រប​ដណ្តប់​ទៅ​ដោយ​រុក្ខជាតិ​បៃតង​ធម្មជាតិ​ ដល់​ទៅ​​ជាង​​​​​ ៥០​% ឯណោះ​។ "
            "ក្រៅ​ពី​នេះ នៅ​មាន​អាគារ​ទំនើប​ខ្ពស់​ៗ​ និង​កន្លែង​ជា​ច្រើន​ទៀត ដែល​​អ្នក​គួរ​ទៅ​លេង ដើម្បី​ទទួល​​បាន​នូវ​​ទិដ្ឋភាព​​ថ្មី​ប្លែក​ អាច​ថត​រូប​លេង​យ៉ាង​សប្បាយ "
            "ដោយ​ពុំ​ចាំ​បាច់​​ចំណាយ​លុយ​ទិញ​សំបុត្រ​​ចូល។ ​១ . Haji Laneកន្លែង​​នេះ​​ស្ថិត​នៅ​ក្នុង​តំបន់​មួយ​មាន​ឈ្មោះ​ថា Kampong Glam។ វា​គឺ​ជា​ផ្លូវ​តូច​ចង្អៀត​​បំផុត​​ហើយ​ក៏​ទាក់​ទាញ​បំផុត​ដែរ​នៅ​ក្នុង​ប្រទេស​សិង្ហបុរី​។ "
            "នៅ​លើ​ជញ្ជាំង​​ពោរពេញ​ទៅ​ដោយ​​សិល្បៈ​គំនូរ​ស្រស់​ស្អាត​ចម្រុះ​ពណ៌​ ចំណែក​ឯ​​នៅ​ជុំ​វិញ​ មាន​​ហាង​កាហ្វេ ម្ហូប​អាហារ និង​ហាង​ទំនិញ​ជា​ដើម ដែល​ជា​ទីតាំង​ដ៏​មាន​ប្រជាប្រិយភាព សម្រាប់​យុវវ័យ​នៃ​ប្រទេស​នេះ "
            "ជួប​ជុំ​គ្នា​ផង​ដែរ​។ ​​២ . Arab Streetនៅ​មិន​ឆ្ងាយ​ពី​គ្នា​ប៉ុន្មាន អ្នក​នឹង​​មក​ដល់​ Arab Street ដែល​ជា​ផ្លូវ​សម្បូរ​ទៅ​ដោយ ហាង​លក់​សម្លៀកបំពាក់ ម្ហូបអាហារ "
            "និង​ហាង​ទំនិញ​ផ្សេងៗ ស្ថិត​នៅ​ក្នុង​អាគារ​មាន​​​ពណ៌​ផ្សេង​ៗ​គ្នា​​។ ជាពិសេស​ វា​ជា​កន្លែង មួយ​ស័ក្តិសម​បំផុត​សម្រាប់​អ្នក​ដែល​ស្វែង​រក​​ម្ហូប​បែប​អិស្លាម (Halal food )។​៣​. Sultan Mosqueនេះ​គឺ​ជា​"
            "វិហារ​អិស្លាម​​ធំ​ជាង​គេ​បង្អស់​នៅ​ក្នុង​ប្រទេស​សិង្ហបុរី ដែល​មាន​ទីតាំង​ស្ថិត​នៅ​លើ​ផ្លូវ North Bridge ក្បែរ​ជាមួយ​​នឹង​ Arab Street។ វិហារ Sultan "
            "ដ៏​លេច​ធ្លោ ក្នុង​​​ទីប្រជុំជន ត្រូវ​បាន​សាង​សង់​ឡើង ចាប់​តាំង​ពី​ឆ្នាំ ១៨២៤ មក​ម្ល៉េះ។​៤. Bugis Streetមិន​ត្រឹម​តែ​ជា​កន្លែង​ថត​រូប​ពេលរាត្រី ​ Bugis Street ក៏​ជា​តំបន់​ពេញ​និយម​​មួយ ដែល​មាន​ផ្សារ​ទំនើប រួម​ទាំង​ផ្សារ​លក់​ទំនិញ​ធូរ​ថ្លៃ​សម​រម្យ​ផង​ដែរ។ ​៥. "
            "Library@Orchardlibrary@orchard បាន​បង្កើត​​ឡើង​​ដោយ​រដ្ឋមន្ត្រីក្រសួងព័ត៌មាននិងសិល្បៈ​ ក្រោម​ការ​គ្រប់គ្រង​របស់​ក្រុមប្រឹក្សាភិបាលបណ្ណាល័យជាតិនៃ​ប្រទេស​សិង្ហបុរី។ នេះ​ជា​បណ្ណាល័យ​សាធារណៈ ដែល​បើក​ទទួល​ស្វាគមន៍​ដល់​ទាំង​ភ្ញៀវ​ជាតិ​​​និង​អន្តរជាតិ។ ក្រៅ​ពី​មាន​សៀវភៅ ដល់​ទៅ​ជាង​៤៥០០០ក្បាល "
            "សម្រាប់​អាន ភ្ញៀវ​ជា​ច្រើន​ក៏​បាន​ទៅ​ថត​រូប​ដោយ​ភាព​ស្ងៀមស្ងាត់ ព្រោះ​បណ្ណាល័យ​នេះ​ មាន​ការ​រចនា​​ច្នៃប្រឌិត​ដ៏​ទាក់ទាញ​បំផុត។៦. សារមន្ទីរជាតិជ្រុល​ទៅ​ដល់​ប្រទេស​សិង្ហបុរី​ហើយ "
            "គួរ​ឆ្លៀត​ពេល​​ចូល​លេង​សារមន្ទីរជាតិ ដែល​​ដាក់​បង្ហាញ​​ពី​ប្រវត្តិសាស្ត្រ​អស្ចារ្យ​​ជា​ច្រើន​នៃ​ប្រទេស​នេះ។ ប្រសិន​បើ​​ទៅ​ដល់​មុន​ម៉ោង "
            "១០​ព្រឹក​ អ្នក​ក៏​​អាច​ថត​រូប​លេង​នៅ​បរិវេណ​ខាង​ក្រៅ​សិន មុន​នឹង​សារមន្ទីរ​បើក។ ​Fort Canningធ្វើ​ដំណើរ​​ចេញ​ពី​សារមន្ទីរជាតិ​បន្តិច អ្នក​នឹង​មក​ដល់​ Fort Canning។ នៅ​កន្លែង​នេះ​ដែរ មិន​ត្រឹម​តែ​ជា​សួន​ច្បារ​ស្រស់​ស្អាត​ និង​ខ្យល់​អាកាស​បរិសុទ្ធ​ប៉ុណ្ណោះ​ទេ "
            "ថែម​ទាំង​​មាន​លាយ​ឡំ​ជាមួយ​នឹង​ប្រវត្តិសាស្ត្រ​ និង​ទីតាំង​ថត​រូប​ទាក់ទាញ​ផង​ដែរ។​៧. Garden by the Bayមិន​គួរ​រំលង​ទេ ព្រោះ​​វា​​ជា​កន្លែង​ទេសចរណ៍​ដ៏​មាន​ប្រជាប្រិយភាព​។ បើ​​បាន​ទៅ​លេង​ពេល​យប់​ កាន់​តែ​ស្អាត​ប្លែក​ភ្នែក​មួយ​កម្រិត​ទៀត ជាមួយ​នឹង​ភ្លើង​ចែងចាំង​ "
            "ហ៊ុមព័ទ្ធ​លាយឡំ​នឹង​ធម្មជាតិ​ស្រស់​បំព្រង។​៨. Jewel  Changi Airport​នៅ​ក្នុង​ព្រលាន Changi ស្ថិត​នៅ​ស្ថានីយ​លេខ​៤ គឺ​ជា​ទីតាំង​ដែល​អ្នក​អាច​ចូល​ទៅ​ដល់ Jewel មុន​គេ។ "
            "សម្រាប់​អ្នក​ដែល​មាន​ជើង​ហោះហើរ​​នៅ​ស្ថានីយ​​លេខ ១ ២ និង​៣ ក៏​អាច​​ចំណាយ​ពេល​ចូល​លេង​បាន​ដែរ ជាពិសេស​វា​​ធំ​ទូលាយ មាន​​រុក្ខជាតិ​តូច​ធំ ​ទឹក​ធ្លាក់ និង​កន្លែង​ជា​ច្រើន​ទៀត "
            "ដែល​​អាច​ផ្តិត​យក​រូប​ស្អាតៗ​រាប់​មិន​អស់​ និង​មិន​ធ្វើ​ឲ្យ​ធុញ​​ទ្រាន់​ ក្នុង​ការ​រង់​ចាំ​ជើង​ហោះ​ហើរ​​​។ចុចអានបន្ត៖ របៀប​​ចាយ​លុយ​ "
            "កុំ​​ឲ្យ​ក្រ​ខ្សត់​ទៅ​ថ្ងៃ​មុខ\n            អត្ថបទ៖  ដេត ឈុនអ៉ី\n          "
        )
    }
    article_url = "https://der.sabay.com.kh/article/1175397#utm_campaign=onpage"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(dersabay_spider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_without_numpage_dersabay():
    """
    Test the `parse` method of the `DersabaySpider` spider.

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

    category_url = "https://der.sabay.com.kh/topics/hang-out"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = dersabay_spider.parse(category_response)

    """
    Testing the parsing category
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    assert len(links) - 1 == 20
    assert links[20] == "https://der.sabay.com.kh/ajax/topics/hang-out/2"


def test_parse_with_numpage_dersabay():
    """
    Test the `parse` method of the `DersabaySpider` spider.

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

    category_url = "https://der.sabay.com.kh/ajax/topics/hang-out/2"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = dersabay_spider.parse(category_response)

    """
    Testing the parsing category
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    assert len(links) - 1 == 14
    assert links[14] == "https://der.sabay.com.kh/ajax/topics/hang-out/3"
