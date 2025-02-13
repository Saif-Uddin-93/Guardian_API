from api_handler.api_utils import *
from dotenv import load_dotenv
import os


load_dotenv()


def test_api_call_successful_with_only_search_term():
    result = get_guardian_data(search_term="tech")
    assert result["response"]["status"] == "ok"


def test_api_url_formatted_correctly_with_options_included():
    opts = [
        ["from-date","2020-01-01"],
        ["page-size","1"]
    ]
    search_term = "tech"
    result = build_api_url(term=search_term, opt=opts)
    assert result == f"https://content.guardianapis.com/search?q=tech&show-blocks=body&from-date=2020-01-01&page-size=1&api-key={os.getenv('test-key')}"


def test_api_call_successful_with_options_included():
    opts = [
        ["from-date","2020-01-01"],
        ["page-size","1"]
    ]
    result = get_guardian_data(search_term="tech", options=opts)
    assert result["response"]["status"] == "ok"
    assert len(result["response"]["results"]) == 1
