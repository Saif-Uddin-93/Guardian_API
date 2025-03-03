from api_handler.api_utils import *
from dotenv import load_dotenv
import pytest
import os
import json

load_dotenv()

def test_api_call_successful_with_only_search_term():
    """
    Test that the API call is successful with only the search term provided.
    """
    result = get_guardian_data(search_term="tech")
    assert result["response"]["status"] == "ok"

def test_api_url_formatted_correctly_with_options_included():
    """
    Test that the API URL is formatted correctly when options are included.
    """
    opts = [
        ["from-date","2020-01-01"],
        ["page-size","1"]
    ]
    search_term = "tech"
    result = build_api_url(term=search_term, opt=opts)
    assert result == f"https://content.guardianapis.com/search?q=tech&show-blocks=body&from-date=2020-01-01&page-size=1&api-key={os.getenv('test-key')}"

def test_api_call_successful_with_options_included():
    """
    Test that the API call is successful when options are included.
    """
    opts = [
        ["from-date","2020-01-01"],
        ["page-size","1"]
    ]
    result = get_guardian_data(search_term="tech", options=opts)
    assert result["response"]["status"] == "ok"
    assert len(result["response"]["results"]) == 1

def test_api_call_with_invalid_options():
    """
    Test that the API call is successful with invalid options.
    """
    opts = [
        ["invalid-option", "value"]
    ]
    result = get_guardian_data(search_term="tech", options=opts)
    assert result["response"]["status"] == "ok"

def test_output_to_json_file():
    """
    Test that JSON data is correctly output to a file.
    """
    sample_data = {"key": "value"}
    output_to_json_file(sample_data, file_path='./test_output.json')
    with open('./test_output.json', 'r') as f:
        data = json.load(f)
    assert data == sample_data
    os.remove('./test_output.json')

def test_api_call_with_empty_search_term():
    """
    Test that the API call is successful with an empty search term.
    """
    result = get_guardian_data(search_term="")
    assert result["response"]["status"] == "ok"

@pytest.mark.xfail
def test_api_call_with_special_characters_in_search_term():
    """
    Test that the API call is successful with special characters in the search term.
    """
    result = get_guardian_data(search_term="!@#$%^&*()")
    print(result)
    assert result["response"]["status"] == "ok"

def test_api_url_with_multiple_options():
    """
    Test that the API URL is formatted correctly with multiple options included.
    """
    opts = [
        ["from-date", "2020-01-01"],
        ["to-date", "2020-12-31"],
        ["page-size", "5"]
    ]
    search_term = "tech"
    result = build_api_url(term=search_term, opt=opts)
    assert result == f"https://content.guardianapis.com/search?q=tech&show-blocks=body&from-date=2020-01-01&to-date=2020-12-31&page-size=5&api-key={os.getenv('test-key')}"

def test_output_to_json_file_with_different_path():
    """
    Test that JSON data is correctly output to a file with a different file path.
    """
    sample_data = {"key": "value"}
    output_to_json_file(sample_data, file_path='./test_output_different.json')
    with open('./test_output_different.json', 'r') as f:
        data = json.load(f)
    assert data == sample_data
    os.remove('./test_output_different.json')
