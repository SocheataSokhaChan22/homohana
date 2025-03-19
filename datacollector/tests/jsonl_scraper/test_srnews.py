""" Test Case SR News """
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.srnews import SrnewsSpider

srnewsSpider = SrnewsSpider()


def test_parse_data_srnews():
    """
    Test the `parse_data` method of the `SrnewsSpider` spider.

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
        "category": "ទេសចរណ៍",
        "title": "«ភ្នំទឹកធំ» ឈរកណ្តាលទឹក ស្អាតខ្លាំងក្នុងរដូវវស្សា ជាប់ព្រំដែនវៀតណាម",
        "content": (
            "រមណីយដ្ឋាន ភ្នំ​ទឹកធំ គឺជា​កន្លែង​ទេសចរណ៍​ថ្មី​មួយ​ដ៏​ទាក់ទាញស្ថិត​នៅជាប់​ព្រំដែន កម្ពុជា និង​វៀតណាម មាន​ទេសភាព​ស្រស់ស្អាតមានទឹក​ព័ទ្ធជុំវិញ មាន​សត្វ​ស្លាប​ជាច្រើន​ព្រោងព្រាត​ហើយ​ភ្ញៀវទេសចរ "
            "អាច​ជិះទូក​លេង​តាម​រអាងភ្នំដើរ​លើ​ស្ពាន​គយគន់​សម្រស់​ផ្ទាំង​ថ្ម ធម្មជាតិ និង ឡើងទៅ​ភ្នំមើល​សត្វ​ប្រចៀវ​ជាច្រើន "
            "និង​អាច​ទស្សនា​សម្រស់​ទិដ្ឋភាព​នៅ​ជុំវិញ​តំបន់​ ​៣៦០​ដឺ​ក្រេ​។​រមណីយដ្ឋាន ភ្នំ​ទឹកធំកើតចេញពី​ការរៀបចំ​ឡើង​ដោយ ព្រះចៅអធិការ សុ​ត ដាវី ដែល​គង់នៅ វត្តភ្នំ​រាប "
            "ដោយសារព្រះអង្គ​មើលឃើញថា ភ្នំ​ទឹកធំ មាន​លក្ខណៈ​អំណោយផល មានទឹក​ជុំវិញ មាន​ល្អាងនិង​មាន​ទេសភាព​ស្រស់ស្អាត ម្យ៉ាង​មាន​ទីតាំង​ជាប់​ព្រះ​ដែន​ផង​នោះ "
            "ព្រោះ​អង្គក៏​ចាប់ផ្តើម​រៀបចំ​សាងសង់​នូវ​ទីតាំង​ភ្នំ​ទឹកធំ​នេះ​បន្តិច​ម្តងៗ ដែលមាន​ព្រះសង្ឃ​គង់នៅ​វត្តភ្នំ​រាប "
            "ទាំងអស់​ជា​អ្នក​ជួយ​ទៅលើ​ការកសាងនិង​ចំណាយ​ថវិកា​របស់​ព្រះអង្គ​ផ្ទាល់​។​ដើម្បី​ទៅកាន់​រមណីយដ្ឋាន ភ្នំ​ទឹកធំភ្ញៀវទេសចរ​អាចធ្វើ​ដំណើ​រ​តាមផ្លូវ​ទៅកាន់​ច្រកព្រំដែន ព្រែក​ចាកដោយ​បត់​ឆ្វេង​ជិះ​តាម​ផ្លូវលំ​ក្បែរ​ព្រំដែន "
            "ចម្ងាយ​ត្រឹមតែ ​៥០០​ម៉ែត្រ​ប៉ុណ្ណោះនឹង​ទៅដល់ គោលដៅ​។ បើក​ដំណើរ​ចាប់ពី​ម៉ោង​៧ ​ព្រឹក ដល់​ម៉ោង ​១០ ​យប់រមណីយដ្ឋាន​ភ្នំ​ទឹកធំ មាន​ចំណតរថយន្ត​ធំ​ទូលាយ ដែល​អាច​ចត​ឡាន​បាន​ជាង "
            "១០០​ ឡាន​​មាន​សន្តិសុខ​សុវត្ថិភាព និង​សណ្តាប់​ល្អ​។ ​រមណីយដ្ឋាន​ជាប់​ព្រំដែន​នេះមាន​កន្លែង​កម្សាន្ត​ជាច្រើន "
            "ដែល​រង់ចាំ​បម្រើ​អារម្មណ៍​ភ្ញៀវទេសចរតួយ៉ាង​ទេសចរ​អាច​ជិះទូក​លេង​តាម​រូងភ្នំ ឬ​រអាងភ្នំឆ្លង​ពី​ម្ខាង​ទៅ​ម្ខាង​ដែលជា​ចំណី​អារម្មណ៍​ថ្មី​ប្លែក "
            "ហើយ​អាច​និយាយបានថាមាន​តែមួយ​ប៉ុណ្ណោះ​នៅ​កម្ពុជា គឺ​ភ្នំ​ទឹកធំ​។ បន្ថែម​ពីនេះបងប្អូន​ក៏​អាច​ជិះទូក​លេង​ជុំវិញ​ភ្នំ ដែល​អាច​ស្រូបយក​ខ្យល់អាកាស​បរិសុទ្ធមើល​ទេសភាព តំបន់​ជាប់​ព្រំដែន "
            "ហើយ​ការ​ជិះទូក​នេះ​មិនត្រូវ​បានគិត​ប្រាក់​នោះទេ​។​​ចេញពី​ការ​ជិះទូកយើង​អាច​ដើរ​ថ្មើរ​ជើ​លើ​ស្ពាន​ឬ​ស្សី​ដ៏​វែង លូន​លើទឹក សសៀរ​តាម​ជើងភ្នំ ប្រវែង៧០០​ម៉ែត្រ ដោយ​អ្នក​ទាំងអស់គ្នា "
            "នឹង​បាន​មើល​សម្រស់​ផ្ទាំងសិលា​ឈរ​យ៉ាងរឹងមាំនិង​មាន​រុក្ខជាតិ ដុះ​ក្រសោប​យ៉ាង​ស្អាត​ក្រៃលែង​។ ​ក្រោយពី​ជិះទូក​រួចភ្ញៀវ​ក៏​អាច​ឡើង​ទៅលើ​ភ្នំ "
            "តាម​ជណ្តើរ​ដែល​រៀបចំ​បាន​យ៉ាង​ទាក់ទាញឆ្ពោះទៅកាន់​រូងភ្នំ​ប្រចៀវ ដែលមាន​សត្វ​ប្រចៀវ​ជាច្រើន កំពុង​ស​ង្ងំ​លាក់ខ្លួនត្រៀម​ចេញ​រក​ចំណី នាពេល​យប់ ហើយ​នៅតាម​ផ្លូវ​ឡើង​នេះ យើង​ក៏​អាច​ទស្សនា​នៅ​ដើមឈើ​ធំៗដែល​ដុះ​ជ្រែក "
            "តោង​តាង​លើ​ផ្ទាំងសិលា​។​​ឈរ​ទៅលើ​កំពូលភ្នំអ្នក​កម្សាន្ត​នឹង​បាន​គយគន់​ទេសភាព​ជួរ​ភ្នំ ដែនដី​ខ្មែរ ស្រុកស្រែ​ចម្ការ​នៅតំបន់​ព្រំដែន "
            "ក៏ដូចជា​មើល​ថ្ងៃ​លិច​ដ៏​ស្រស់ស្អាត​ផងដែរ​។សម្រាប់​ផ្នែក​កំពូលភ្នំ ព្រះចៅអធិការ សុ​ត ដាវី នឹងមាន​គម្រោង​ក្នុងការ​កសាង​ជា​កន្លែង​អង្គុយ​សម្រាក​លើ​កំពូលភ្នំដែល​យើង​អាច​គយគន់ "
            "សម្រស់​ធម្មជាតិ​នៅទីនេះ បាន ​៣៦០​ដឺ​ក្រេ​។ ​សម្រាប់​ពុទ្ធ​បរិ​ស័ត នៅទីនេះក៏មាន​ពុទ្ធបដិមា ដែល​ទុក​សម្រាប់​ឱ្យ​បងប្អូន​ដែល​មកលេង ធ្វើការ​រំលឹក​ដល់​គុណនិង​បូជា​ចំពោះ​ព្រះពុទ្ធសាសនា "
            "ដែលជា​សាសនា​របស់​រដ្ឋថែមទាំង​បានមក​ធ្វើបុណ្យ​ទៀតផង​។  នៅទីនេះ ក៏​ក្យូ​ស​ជាង ១០០សម្រាប់​ទទួលភ្ញៀវ​ទេសច​រណ៍ ដែលមាន​លក់​នូវ​ម្ហូបអាហារ ​នំនែក "
            "ក៏ដូចជា​ភេសជ្ជៈ​ជាច្រើន​ប្រភេទដែល​នេះ​គឺជា​ការបង្កើត​មុខរបរ​ជូន​ដល់​បងប្អូន​នៅ​មូលដ្ឋាន ​ហើយ​ក្យូ​ស​ទាំងនេះ​អ្នកទេសចរអាច​សម្រាក​អង្គុយលេង គេង​យោលអង្រឹង ស្តាប់​សត្វ​ស្លាប "
            "ជាច្រើន​ប្រភេទដែល​ហោះហើរ​ស្រែក​អឺ​កង​ស្រ​សង​គ្នា សក្តិសម​បំផុត​សម្រាប់អ្នក​ចូលចិត្ត​សត្វ​បក្សី​។ "
            "​សម្រាប់​ថ្ងៃ​ធម្មតាទីនេះ​ទទួលបាន​ភ្ញៀវទេសចរ​មកលេង​ជាង ១​ពាន់​នាក់ ក្នុង​មួយថ្ងៃ ចំណែក​ថ្ងៃ​ចុង​សប្ដាហ៍​វិញមាន​រហូត​ជិត ១​ម៉ឺន​នាក់ "
            "ហើយ​ទីនេះ​មាន​បុគ្គលិក​ជាច្រើន​នាក់សម្រាប់​បម្រើសេវា​ដល់​ភ្ញៀវ​។​​ព្រះចៅអធិការ សុ​ត ដាវីក៏​ស្នើឱ្យ​អ្នក​មក​កម្សាន្ត​នៅ​រមណីយដ្ឋាន ភ្នំ​ទឹកធំ "
            "ជួយ​ថែរក្សា​បរិស្ថាននិង​ជួយ​ទុកដាក់​សំរាម​ឱ្យបាន​ត្រឹមត្រូវ និង​និមន្ត​អញ្ជើញ​ភ្ញៀវទេសចរ​ទាំងអស់ដែល​មកលេង នៅ​រមណីយដ្ឋាន​ភ្នំ​ទឹកធំ "
            "ឱ្យចូល​ទៅធ្វើ​បុណ្យ​នៅ​វត្តភ្នំ​រាបដែល​ស្ថិតនៅ​ជិត​ភ្នំ​ទឹកធំ​នេះ ព្រោះ​ទីតាំង​ទាំង​២​នេះគឺជា​កន្លែង​ការពារ​ព្រំដែន​សីមានិង​ជា​កន្លែង​ថែរក្សា​នូវ​ព្រះពុទ្ធសាស"
            "នា​ផងដែរ​។ ​រមណី​ដ្ឋា​ន​ភ្នំ​ទឹកធំ​ស្ថិតនៅ​ក្នុងភូមិ​អន្លង់​ថ្ងាន់ឃុំ​ឬ​ស្ស៊ី​ស្រុក ស្រុក​កំពង់ត្រាច ខេត្តកំពតនិង​មាន​ចម្ងាយ​ត្រឹមតែ​៥០០​ម៉ែត្រ​ប៉ុណ្ណោះ​ពី​ព្រំដែន​។​ទំនាក់ទំនង​គេហទំព័រ​ហ្វេ​ស​"
            "ប៊ុ​កវត្តភ្នំ​រាប ទឹកដី​ទល់ដែន​វៀតណាម ឬ​ទំនាក់ទំនង​លេខ​ទូរ​សព្ទ​៖ ០១២ ៤២៩ ៨១៧៕​ ទីតាំង​៖ ‍")
    }

    article_url = "https://www.srdigitalmedia.com.kh/articles/phnom-teuk-thom-stands-in-the-middle-of-very-clean-water-during-the-rainy-season-near-the-vietnamese-border"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.content)

    article = next(srnewsSpider.parse_data(article_response))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_srnews():
    """
    Test the `parse` method of the `SrnewsSpider` spider.

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
    current_url (str):
        The current category URL.
    next_page (str):
        The URL of the next page after pagination.
    """

    category_url = "https://www.srdigitalmedia.com.kh/technology"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = srnewsSpider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    """
    Test for pagination
    """
    next_page = category_response.css("a[aria-label='Next Page']::attr(href)").get()
    if next_page:
        next_page_url = category_response.urljoin(next_page)
    assert len(links) - 1 == 6
    assert links[6] == next_page_url
    assert links[6] == "https://www.srdigitalmedia.com.kh/technology?fe30cbae_page=2"

