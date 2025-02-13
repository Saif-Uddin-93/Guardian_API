import json, os, requests
from dotenv import load_dotenv

load_dotenv()

api_keywords = [

]

def build_api_url(term:str = "tech", opt: list = []) -> str:
    filters = "&".join(["=".join(arg) for arg in opt])
    if filters:
        filters += "&"
    return f"https://content.guardianapis.com/search?q={term}&show-blocks=body&{filters}api-key={os.getenv('test-key')}"

def fetch_api(url:str) -> json:
    return requests.get(url).json()

def output_to_json_file(jsn:json, file_path='./default.json') -> None:
    with open(file_path, 'w') as f:
        json.dump(jsn, f, indent=4)

def get_guardian_data(search_term: str, options: list = None, save_to: str | None = None) -> None:
    url: str
    if not options:
        url = build_api_url(search_term)
    else:
        url = build_api_url(search_term, options)
    response = fetch_api(url=url)
    if not save_to:
        return response
    elif (save_to == "local"):
        output_to_json_file(response)
    else:
        output_to_json_file(response, save_to)
