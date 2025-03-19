"""Test Case For Khmer Food Recipes website."""
import requests
from scrapy.http import HtmlResponse
from url_khmer_scraping.jsonl_scraper.spiders.khmerfoodrecipes import KhmerfoodrecipesSpider

# Instantiate the spider
khmerfoodrecipes_spider = KhmerfoodrecipesSpider()

def test_parse_khmerfoodrecipes():
    """
    Test the `parse` method of the `KhmerfoodrecipesSpider`.

    This test performs the following checks:
    - Extracts all category URLs from the category page.
    - Verifies the total number of links extracted from the page.
    - Ensures the spider correctly parses the categories on the start page.

    Procedure:
    ----------
    - Sends a GET request to the main category page URL.
    - Converts the HTTP response into a Scrapy HtmlResponse object.
    - Calls the spider's `parse` method with the response.
    - Collects and stores the URLs returned by the `parse` method.

    Assertions:
    -----------
    - Asserts that the number of extracted category URLs matches the expected value.
    """

    url = "https://khmerfoodrecipes.blogspot.com"
    category = requests.get(url)
    category_response = HtmlResponse(url=category.url, body=category.text, encoding="utf-8")
    category_result = khmerfoodrecipes_spider.parse(category_response)

    # Collect links from the category result
    links = []
    for link in category_result:
        links.append(link.url)

    # Assert that the expected number of category links is found
    assert len(links) == 18


def test_parse_articles_khmerfoodrecipes():
    """
    Test the `parse_articles` method of the `KhmerfoodrecipesSpider`.

    This test performs the following checks:
    - Extracts article URLs from a specific category.
    - Verifies that the correct number of articles (max-results) is parsed.

    Procedure:
    ----------
    - Sends a GET request to a category page with a defined max-results limit.
    - Converts the HTTP response into a Scrapy HtmlResponse object.
    - Calls the spider's `parse_articles` method to retrieve the article URLs.
    - Collects and stores the article URLs returned by the `parse_articles` method.

    Assertions:
    -----------
    - Asserts that the number of extracted article URLs matches the max-results parameter.
    """

    max_results = 20
    categories_url = f"https://khmerfoodrecipes.blogspot.com/search/label/សាច់គោ?&max-results={max_results}"
    articles = requests.get(categories_url)
    articles_response = HtmlResponse(url=articles.url, body=articles.text, encoding="utf-8")
    articles_result = khmerfoodrecipes_spider.parse_articles(articles_response)

    # Collect article URLs
    articles_items = []
    for article in articles_result:
        articles_items.append(article.url)

    # Assert that the number of articles matches the expected max-results
    assert len(articles_items) == max_results


def test_parse_data_khmerfoodrecipes():
    """
    Test the `parse_data` method of the `KhmerfoodrecipesSpider`.

    This test checks the following:
    - The category of the article is correctly extracted.
    - The title of the article is correctly extracted.
    - The content of the article is correctly parsed.
    - The URL of the article is correctly set.

    Attributes:
    ----------
    article_url (str):
        The URL of the article to be tested.
    article (Response):
        The HTTP response object for the article URL.
    article_response (HtmlResponse):
        The response object to be passed to the spider's `parse_data` method.
    article_result (list):
        The list of results returned by the spider's `parse_data` method.
    expected_value (dict):
        Expected result of the parsed data.

    Assertions:
    -----------
    - Asserts that the extracted category contains expected keywords.
    - Asserts that the title is correctly parsed.
    - Asserts that the content is not empty.
    - Asserts that the URL is correctly set to the article's URL.
    """
    expected_value = {
        "category": "\n,ញាំ,,\n,សាច់គោ,\n",
        "title": "\nរបៀបធ្វើ ភ្លារតនៈគីរី\n",
        "content": (
            "\n\n\n\nគ្រឿងផ្សំ៖\n1- សាច់គោ យកសាច់គោល្អខ្ចី ហេីយផុយ ( លាងទឹកអោយស្អាត ហាន់ជាបន្ទះស្ដេីងៗ )"
            "\n2- ម្ទេសប្លោកលឿង . ម្ទេសប្លោកក្រហម （ លាងទឹកអោយស្អាត ហាន់ជាសសៃតូចៗ )\n3- ខ្ទឹមបារាំង （លាងទឹកអោយស្អាត ហាន់ជាបន្ទះស្ដេីងៗ ）\n4- ត្រប់ស្រួយ (លាងទឹកអោយស្អាត ហាន់ជាបន្ទះស្ដេីងៗ )\n5- សណ្ដែកកួរ （លាងទឹកអោយស្អាត កាត់ជាកង់ៗ ខ្លីល្មម ）\n6- ជីរអង្កាម ( បេះអោយស្អាត "
            "រួចយកទៅលាងទឹក )\n7- សាឡាត់ . នឹងសាឡាត់ពណ៌ស្វាយ （ បេះលាងទឹកអោយស្អាត កាត់ជាកង់ខ្លីៗ ល្មម ）\n8- ប៉េងប៉ោះ ( លាងទឹកអោយស្អាតពុុះជាបួន )\n9- អង្ករលីង\n10- អំបិល\n11- បីចេង\n12- ស្ករស\n13- ក្រូចឆ្មារ ឬ ទឹកក្រូចឆ្មារ\n14- ប្រហុកឆៅ ( ចិញ្ច្រាំអោយម៉ត់ )\n15- រំដេង . "
            "គល់ស្លឹកគ្រៃ . ស្លឹកក្រូចសេីច （ លាងទឹកអោយស្អាត ហាន់បញ្ឈិតស្ដេីងៗ ）\n16- ខ្ទឹមស . ខ្ទឹមក្រហម . ម្ទេស ( លាងទឹកអោយស្អាត ចិញ្ច្រាំចូលគ្នាអោយម៉ត់ )\n\n\n\n\n\n\n\nវិធីធ្វើ៖\n1- \nយេីងដាំទឹកបន្តិចសំរាប់ យកមកធ្វេីជាទឹកប្រហុក ទឹកពុះរួចយកប្រហុកចិញ្ច្រាំ \nដាក់ចូលចានល្មម "
            "ចាក់ទឹកដាំពុះចូលរួចចាក់ ខ្ទឹមស ខ្ទឹមក្រហម ម្ទេសចិញ្ច្រាំ \nស្ករស អំបិល ទឹកក្រូចឆ្មារ បីចេង ចូលកូរអោយសព្វដាក់សាច់គោចូល រំដេង \nគល់ស្លឹកគ្រៃ\nស្លឹកក្រូចសេីច ភ្លក់រស់ជាតីតាមចំណូលចិត្ត "
            "រួចទុកមួយអន្លេីរ\n2-\n យកបន្លែដែលហាន់រួច ដាក់ចូលចានដែលធំមួយ យកសាច់គោដែលត្រាំទឹក ប្រហុក មកចាក់ \nចូលជាមួយបន្លែរ ច្របល់ថ្នមៗ រួចដាក់អង្ករលីង ជីរអង្កាម ចូលច្របល់ម្ដងទៀត \nថ្នមៗ\n3- "
            "រួចបន្ថែមម្ដងទៀត អង្ករលីង ជាការស្រេច\n អាហារមួយមុខនេះសំរាប់រីករាយជួបជុំគ្រួសារ មិត្តភក្ដិ បងប្អូន នឹងក្រុមការងារចុងសប្ដាហ៌\n\n\n\n\n\n\n\nប្រភព​ពី ​៖ Reasey Sovan Chea\n")
    }

    article_url = "https://khmerfoodrecipes.blogspot.com/2017/02/vi-ty-tver-plear-ratanakiri.html"
    article = requests.get(article_url)
    article_response = HtmlResponse(url=article.url, body=article.text, encoding="utf-8")

    # Call the spider's parse_data method
    article = next(khmerfoodrecipes_spider.parse_data(article_response))

    # Assert the correctness of the extracted data
    assert article["category"] == expected_value["category"]
    assert article["title"] == expected_value["title"]
    assert article["content"] == expected_value["content"]
    assert article["url"] == article_url

