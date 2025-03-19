"""Test Case For AMS Khmer Civilization"""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.amskhmercivilization import AMSkhmercivilizationSpider

amskhmercivilization_spider = AMSkhmercivilizationSpider()

def test_parse_data_khmercivilization():
    """
    Test the parse_data method of AMSkhmercivilizationSpider.

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
        "category": "ទំនៀមទម្លាប់បុរាណ",
        "title": "ព្រះវិហារវត្តល្អក់",
        "content" : (
                "វត្តល្អក់ ឬ វត្ត​អរញ្ញរង្សី ស្ថិត​នៅ​ក្នុង​ឃុំ​គោក​សណ្តែក ស្រុក​ប្រាសាទ​បាគង ខេត្ត​សៀមរាប។ "
                "មកដល់សព្វថ្ងៃ វត្តនេះមានព្រះវិហារ​ពីរ ហើយ​បើ​ចូល​តាម​ខ្លោងទ្វារ​​មុខ​ "
                "គេឃើញ​​ព្រះវិហារ​បុរាណ​ស្ថិត​នៅ​ខាង​ស្តាំ​ រីឯព្រះវិហារសង់​ថ្មីស្ថិតនៅខាងឆ្វេង។ "
                "ចំពោះ​ព្រះវិហារ​បុរាណ​ គឺ​ជា​សំណង់​សក្ការៈដ៏ល្អឯកក្នុង​ព្រះពុទ្ធសាសនា "
                "ប្រកបដោយ​ក្បាច់​រចនា​​យ៉ាង​វិចិត្រក្រៃលែង។ ផ្អែក​លើ​ចំណារ​លើ​បល័ង្ក​ព្រះជីវ៍ "
                "និង​ការ​សិក្សា​កន្លង​មក​សន្និដ្ឋាន​​ថា ព្រះវិហារ​​បុរាណ​កសាង​ឡើង​នៅភាគ​ខាង​ដើម​នៃ​សតវត្សទី​១៩។ "
                "ចំណែក​​ព្រះ​​វិហារ​ថ្មីកសាងឡើង​​នៅរវាង​ដើមសតវត្សទី២១ "
                "ដោយ​​គេ​សង្កេត​ឃើញ​មាន​លក្ខណៈ​សិល្បៈ​ខ្លះ​ចម្លង​ពីវិហារ​បុរាណ។ព្រះវិហារ​បុរាណវត្ត​ល្អក់ "
                "មាន​រចនាសម្ព័ន្ធ​​​ទូទៅ​នៃសំណង់​ផ្នែក​ខាងក្រោម​ គឺជា​ឥដ្ឋ​បូក​កំបោរ​បាយ​អ​ "
                "រីឯគ្រឿង​បង្គុំនៅផ្នែក​ខាងលើ​គឺ​ជា​ឈើ។ ចំណែក​បរិវេណ​​ខាង​​ក្រៅ​ "
                "ដើម​ឡើយ​​ប្រហែល​​ព័ទ្ធ​ដោយ​​ប​ង្កាន់ដៃជុំវិញ "
                "ដ្បិត​សព្វថ្ងៃគេឃើញ​នៅ​សល់​​​តែ​​​ទ្វារបង្កាន់ដៃ​ទិស​ខាង​កើត ខាងលិច និង​ខាង​ជើង​។ "
                "ដោយ​​ឡែក​​នៅ​ផ្នែក​ខាង​ត្បូង បាន​រៀបចំ​ពង្រីក​ខឿន​​ព្រះវិហារ​ថ្មី "
                "ឱ្យទល់ដល់​នឹង​សសរ​ព្រះវិហារ​ចាស់។ លើស​ពីនេះ សសរ​បុរាណជុំវិញ​​បាំង​សាច គេសង្កេតឃើញ​ថា​ជាសសរឈើ "
                "​ហើយ​សព្វ​ថ្ងៃ​បាន​ជួស​​ជុល​​ប្តូរជា​សសរ​បេតុង​ជាបន្តបន្ទាប់។ព្រះវិហារបុរាណវត្តល្អក់ "
                "សង់ឡើង​មាន​លក្ខណៈ​ជា​​​វិហារដំបូល​កិង ប្រក់​ក្បឿង​​ស្រកាលេញ មាន​ជម្រាល​ជាថ្នាក់ៗសងខាង "
                "និងបំពាក់​​ជហ្វា​ពីរ​នៅ​ចុង​មេដំបូលខាង​មុខ និង​ជហ្វា​ពីរនៅ​ចុង​មេដំបូល​ខាងក្រោយ។ ​"
                "ចំពោះ​ហោ​ជាង​​ទាំង​សងខាងនៃព្រះវិហារ​​នេះ គឺ​ជា​ប្រភេទ​​ហោ​ជាង​​ឆ្លាក់​អំពី​ឈើ​។​ "
                "នៅលើហោជាង​ខាងកើត គេឆ្លាក់ជា​រូប​ព្រះចេតិយ ដែល​មាន​ដងទង់មួយ​គូ "
                "និង​ទេព្តាកាន់ផ្កាឈូកអង្គុយ​​ប្រណម្យ​សងខាង។ ចំណែក​នៅលើ​កំពូល​​ព្រះ​ចេតិយ​នោះ "
                "គេឆ្លាក់​រូបព្រះសិអារ្យមេត្រីគង់លើ​ផ្កាឈូក(?)។ ដោយ​ឡែក នៅលើ​ហោជាង​ទិស​ខាងកើត​នៃព្រះវិហារ​ថ្មីវត្ត​នេះ ​ប្រហែល​​​ឆ្លាក់​ចម្លង​រូប​​ព្រះ​​​ចេតិយ "
                "និង​ទិដ្ឋភាព​ជុំវិញនៅលើហោជាង​ខាងកើត​នៃ​ព្រះ​វិហារ​ចាស់។ចំពោះហោជាង​​ខាងលិចនៃព្រះវិហារ​បុរាណ "
                "ក៏ជា​ប្រភេទហោជាង​ឆ្លាក់​អំពីឈើ​​ដូច​ហោ​ជាង​ខាងកើតដែរ​។ ប៉ុន្តែ​គួរ​ឱ្យ​ស្តាយ ហោជាង​នេះ​បាន​ពុក​ផុយរលុប​បាត់​ខ្លឹមសារ​​ទាំងស្រុង ពុំ​អាច​មើល​យល់​ឡើយ។ ដូច្នេះ "
                "អ្វីដែល​គេ​អាច​សម្គាល់​ឃើញ​នៃ​ក្បាច់​​តុង​តែង​​លម្អលើ​​​ផ្នែក​ដំបូល គឺការជួស​ជុល​ និង​​ផ្លាស់​ប្តូរ​នាគដងក្តារថ្មី តែរក្សា​ទុក​ជហ្វា​​បុរាណ។ លក្ខណៈ​ពិសេសនៃជហ្វា​បុរាណ​ព្រះវិហារនេះ គឺជហ្វាមានគែ មានពុក​ចង្កា មានមាត់ មានចង្កូម (ពាំកែវ) និងមានភ្នែក ដែល​បង្ហាញ​ឱ្យឃើញ​ច្បាស់​ថា​ជហ្វា​គឺជា​នាគ។ ​មិន​តែ​ប៉ុណ្ណោះ នៅលើ​គែដែលជា​ទូទៅ​ឆ្លាក់ជារូបចក្រ ឬគេតែងហៅថាត្រា​នោះ គេ​​បាន​ច្នៃ​ឆ្លាក់​ជា​រូបមុខ​មនុស្ស "
                "ឯផ្នែកមូលខាងក្រោមជាត្រានាគ ក្លាយទៅជា​ស្រងក​មនុស្ស។ រូបលេខ​៧ គឺជា​ជហ្វា​ឈើ​មុន​ពេលជួសជុល និងរូបលេខ៨ ជា​ជហ្វា​​ចម្លង​ថ្មីតាម​លំអាន​ជហ្វា​ចាស់។រចនាសម្ព័ន្ធផ្នែក​ខាងក្នុង​ព្រះ​​វិហារ​មាន​​សសរឈើពីរជួរ"
                "អម​សង​ខាង​ល្វែង​គ្រឹះ និង​សសរ​​ឈើ​ពីរ​ជួរ​ទៀត​ជាប់​ជញ្ជាំង។ សសរទាំងអស់​ សុទ្ធសឹង​ជា​ប្រភេទ​សសរ​ឈើ​៨ជ្រុង ទ្រ​គ្រឿង​បង្គុំ​ឈើ​ផ្នែក​ខាងលើ "
                "ហើយ​ពុំ​មាន​​ក្បាច់​​លម្អ​អ្វី​ឡើយ។ រីឯ​ជញ្ជាំង​​ព្រះវិហារ​ គេ​បាន​រៀប​ឥដ្ឋ​ថ្មី​មួយ​ជាន់​ទៀត​ពី​ខាង​ក្នុង បំណង​ទប់​ជញ្ជាំង​ចាស់​កុំឱ្យ​រលំ។ ចំណែក​​ផ្ទៃ​កម្រាល​ព្រះវិហារ គេ​​ក្រាល​ប្រភេទ​​ការ៉ូ​បុរាណ ហើយគេ​​រៀប​​ផ្នែក​ចន្លោះ​ល្វែង​គ្រឹះ​ឱ្យ​ខ្ពស់​ជាង​របៀងសងខាង​បន្តិច​ ព្រម​ទាំង​មាន​ស្លាក​ស្នាម​ដាំ​សន្លឹក​សីមាជុំវិញផង។ ការរៀបចំ​បែបនេះ គេឃើញ​ដូច​គ្នា​ទៅនឹង​ល្វែង​គ្រឹះ​ព្រះវិហារ​វត្ត​រាជបូព៌​ដែលកសាងឡើងតាំងពីឆ្នាំ​១៩០៧។សូមបញ្ជាក់​ដែរថា ព្រះវិហារ​បុរាណ​នេះ​ពុំមាន​ពិតាន​ឡើយ។ នៅ​ផ្នែក​ខាង​លិច​នៃចុង​ល្វែង​គ្រឹះ គឺជាបល្ល័ង្ក​តម្កល់ព្រះជីវ៍។ បល្ល័ង្កព្រះជីវ៍នៃ​ព្រះ​វិហារ​នេះ ហាក់​ប្រកប​ដោយ​​លក្ខណៈសិល្បៈ​ប្លែក និងកម្រ​ ដ្បិតជា​ទម្រង់​បល្ល័ង្ក​ភ្ជាប់​បុស្បុក​ខ្ពស់​ស្ទើរ​​ទល់​​ដំបូល។ ​ផ្នែក​ខាងក្រោមនៃបល្ល័ង្កនេះមាន​រាង​បួនជ្រុង ​ខាងមុខ​គេរៀបឱ្យ​ចេញ​ជា​​បីថ្នាក់​ដាក់​គ្រឿង​សក្ការៈ​ និងផ្លា​ភ្ញីផ្សេងៗ។ ផ្នែក​ចំហៀង និងខាងក្រោយ​ គេរៀបឱ្យ​ចេញ​ជា​​ល្បាក់​ ហើយ​បិទលម្អក្បាច់​ត្របកឈូកជុំវិញ។ រីឯ​កំពូល​បុស្បុក​ គេរៀប​ឱ្យ​ចេញ​ជា​បីថ្នាក់។ តាមថ្នាក់នីមួយៗ លម្អដោយ​ក្បាច់រចនា​យ៉ាង​រស់វើក ព្រម​ទាំង​មាន​​ដាំ​កញ្ចក់​យ៉ាង​ភ្លឺផ្លេក​។សង្ខេបមក ព្រះវិហារវត្តល្អក់ជាស្ថាបត្យកម្មព្រះពុទ្ធសាសនាយ៉ាង​វិសេស​ ពុំធ្លាប់​ឃើញ​ពីមុនមក។ និងសន្និដ្ឋានថា​ព្រះវិហារ​នេះ​កសាង​នៅក្នុងឆ្នាំ​១៩២៩។ ផ្នែក​ខ្លះនៃការ​តុបតែង​លម្អ​ព្រះវិហារ​នេះ មានឥទ្ធិពល​​មួយ​ភាគ​លើសំណង់ព្រះវិហារ​ថ្មី ជាពិសេស​ខ្លឹមសា​រចម្លាក់ហោជាង​ខាងកើត ដែលមាន​រូប​ព្រះ​​សម្យមុនីចេតិយ៕អត្ថបទដើម៖ កញ្ញា ហៀន សុវណ្ណមរកតCOPYRIGHT © 2020-2022 BY APSARA MEDIA SERVICES (AMS) "
            )
    }
    article_url = "https://ams.com.kh/khmercivilization/detail/22519"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    article = next(amskhmercivilization_spider.parse_data(article_response, category="ទំនៀមទម្លាប់បុរាណ"))
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

def test_parse_khmercivilization():
    """
    Test the parse method of AMSkhmercivilizationSpider.

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

    category_url = "https://ams.com.kh/khmercivilization/history/archaeology"
    category = requests.get(category_url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = amskhmercivilization_spider.parse(category_response)

    """
    Testing the parsing category 
    """
    links = []
    for link in category_result:
        links.append(link.url)
    
    """
    Test for pagination
    """
    next_page_url = category_response.css(".page-nav a[aria-label='next-page']::attr(href)").get()

    assert len(links) - 1 == 9
    assert links[9] == next_page_url
    assert links[9] == "https://ams.com.kh/khmercivilization/history/archaeology/page/2"
