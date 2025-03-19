"""
Test Case for PaginationHandle Class with the following functions.
"""
from url_khmer_scraping.jsonl_scraper.utils.pagination_handle import PaginationHandle

pagination_handle = PaginationHandle()

def test_get_next_page_url_with_param_no_query_params():
    current_url = "https://example.com"
    expected_url = "https://example.com?page=2"
    next_page_url = pagination_handle.get_next_page_url_with_param(current_url)
    
    assert next_page_url == expected_url

def test_get_next_page_url_with_param_existing_page_param():
    current_url = "https://example.com?page=3"
    expected_url = "https://example.com?page=4"
    next_page_url = pagination_handle.get_next_page_url_with_param(current_url)
    
    assert next_page_url == expected_url

def test_get_next_page_url_no_query_params():
    current_url = "https://example.com"
    expected_url = "https://example.com/page/2"
    next_page_url = pagination_handle.get_next_page_url(current_url)
    assert next_page_url == expected_url

def test_get_next_page_url_existing_page_number():
    current_url = "https://example.com/page/3"
    expected_url = "https://example.com/page/4"
    next_page_url = pagination_handle.get_next_page_url(current_url)
    assert next_page_url == expected_url
