import json, os, requests
from dotenv import load_dotenv

load_dotenv()

api_keywords = []


def build_api_url(term: str = "tech", opt: list = []) -> str:
    """
    Build the API URL for fetching data from The Guardian API.

    Args:
        term (str): The search term to query. Defaults to "tech".
        opt (list): A list of additional query parameters as tuples. Defaults to an empty list.

    Returns:
        str: The constructed API URL.
    """
    filters = "&".join(["=".join(arg) for arg in opt])
    if filters:
        filters += "&"
    return f"https://content.guardianapis.com/search?q={term}&show-blocks=body&{filters}api-key={os.getenv('test-key') or 'test'}"


def fetch_api(url: str) -> json:
    """
    Fetch data from the given API URL.

    Args:
        url (str): The API URL to fetch data from.

    Returns:
        json: The JSON response from the API.
    """
    return requests.get(url).json()


def output_to_json_file(jsn: json, file_path: str = "./default.json") -> None:
    """
    Output JSON data to a file.

    Args:
        jsn (json): The JSON data to write to the file.
        file_path (str): The file path to write the JSON data to. Defaults to './default.json'.

    Returns:
        None
    """
    with open(file_path, "w") as f:
        json.dump(jsn, f, indent=4)


def get_guardian_data(
    search_term: str, options: list = []
) -> None:
    """
    Fetch data from The Guardian API and optionally save it to a file.

    Args:
        search_term (str): The search term to query.
        options (list): A list of additional query parameters as lists of key value pairs. Defaults to None.

    Returns:
        None
    """
    url = build_api_url(search_term, options)
    response = fetch_api(url=url)
    return response
