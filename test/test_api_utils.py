from api_handler.api_utils import *
from dotenv import load_dotenv
import pytest
import os
import json


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


def test_api_call_with_invalid_search_term():
    result = get_guardian_data(search_term="invalidterm")
    assert result["response"]["status"] == "ok"
    assert len(result["response"]["results"]) == 0

def test_api_call_with_invalid_options():
    opts = [
        ["invalid-option", "value"]
    ]
    result = get_guardian_data(search_term="tech", options=opts)
    assert result["response"]["status"] == "ok"

def test_output_to_json_file():
    sample_data = {"key": "value"}
    output_to_json_file(sample_data, file_path='./test_output.json')
    with open('./test_output.json', 'r') as f:
        data = json.load(f)
    assert data == sample_data
    os.remove('./test_output.json')

def test_api_call_with_empty_search_term():
    result = get_guardian_data(search_term="")
    assert result["response"]["status"] == "ok"

@pytest.mark.xfail
def test_api_call_with_special_characters_in_search_term():
    result = get_guardian_data(search_term="!@#$%^&*()")
    print(result)
    assert result["response"]["status"] == "ok"

def test_api_url_with_multiple_options():
    opts = [
        ["from-date", "2020-01-01"],
        ["to-date", "2020-12-31"],
        ["page-size", "5"]
    ]
    search_term = "tech"
    result = build_api_url(term=search_term, opt=opts)
    assert result == f"https://content.guardianapis.com/search?q=tech&show-blocks=body&from-date=2020-01-01&to-date=2020-12-31&page-size=5&api-key={os.getenv('test-key')}"

def test_output_to_json_file_with_different_path():
    sample_data = {"key": "value"}
    output_to_json_file(sample_data, file_path='./test_output_different.json')
    with open('./test_output_different.json', 'r') as f:
        data = json.load(f)
    assert data == sample_data
    os.remove('./test_output_different.json')
