import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
STRAICO_API_KEY = os.getenv('STRAICO_API_KEY')

def get_available_models():
    url = "https://api.straico.com/v1/models"
    headers = {
        "Authorization": f"Bearer {STRAICO_API_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

models = get_available_models()
if models:
    print("\nAvailable models:")
    print(json.dumps(models, indent=2))
