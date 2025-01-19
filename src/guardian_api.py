import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_keywords = [

]

def build_api_url(arg_1:str = "tech") -> str:
    return f"https://content.guardianapis.com/search?q={arg_1}&api-key={os.getenv('test-key')}"

def fetch_api(url:str) -> json:
    return requests.get(url).json()

def output_to_json_file(jsn:json, file_path='./default.json') -> None:
    with open(file_path, 'w') as f:
        json.dump(jsn, f, indent=4)

def get_guardian_data(arg_1:str, arg_2:str = None) -> None:
    if arg_2:
        file_path = f"./{arg_2}.json"
        output_to_json_file(fetch_api(build_api_url(arg_1, arg_2)), file_path)
    else:
        output_to_json_file(fetch_api(build_api_url(arg_1)))

get_guardian_data("tech")