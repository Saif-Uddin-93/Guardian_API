from utility.api_utils import *


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
    opts = [["from-date", "2020-01-01"], ["page-size", "1"]]
    search_term = "tech"
    result = build_api_url(term=search_term, opt=opts)
    assert (
        result
        == f"https://content.guardianapis.com/search?q=tech&show-blocks=body&from-date=2020-01-01&page-size=1&api-key={'test'}"
    )


def test_api_call_successful_with_options_included():
    """
    Test that the API call is successful when options are included.
    """
    opts = [["from-date", "2020-01-01"], ["page-size", "1"]]
    result = get_guardian_data(search_term="tech", options=opts)
    assert result["response"]["status"] == "ok"
    assert len(result["response"]["results"]) == 1


def test_api_call_with_invalid_options():
    """
    Test that the API call is successful with invalid options.
    """
    opts = [["invalid-option", "value"]]
    result = get_guardian_data(search_term="tech", options=opts)
    assert result["response"]["status"] == "ok"


def test_api_call_with_empty_search_term():
    """
    Test that the API call is successful with an empty search term.
    """
    result = get_guardian_data(search_term="")
    assert result["response"]["status"] == "ok"


def test_api_url_with_multiple_options():
    """
    Test that the API URL is formatted correctly with multiple options included.
    """
    opts = [["from-date", "2020-01-01"], ["to-date", "2020-12-31"], ["page-size", "5"]]
    search_term = "tech"
    result = build_api_url(term=search_term, opt=opts)
    assert (
        result
        == f"https://content.guardianapis.com/search?q=tech&show-blocks=body&from-date=2020-01-01&to-date=2020-12-31&page-size=5&api-key={'test'}"
    )


