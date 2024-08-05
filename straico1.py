import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
STRAICO_API_KEY = os.getenv('STRAICO_API_KEY')
print(f"API Key: {STRAICO_API_KEY}")

def make_api_request(url, headers, data):
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def save_response_to_file(response_data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=2)
        print(f"Response saved to {filename}")
    except IOError as e:
        print(f"Error saving response to file: {e}")

def main():
    url = "https://api.straico.com/v1/prompt/completion"

    headers = {
        "Authorization": f"Bearer {STRAICO_API_KEY}",
        "Content-Type": "application/json"
    }

    youtube_url = "https://youtu.be/r2UISJZLp7o?si=YgJJ24odrPHTa5bN"
    data = {
        "models": ["openai/gpt-4o-mini"],
        "message": "what is the video about",
        "youtube_urls": [youtube_url],
        "display_transcripts": True
    }

    response_data = make_api_request(url, headers, data)

    if response_data:
        # Add the YouTube URL to the response data
        response_data['youtube_url'] = youtube_url

        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"response_{timestamp}.json"
        
        save_response_to_file(response_data, filename)
        
        # Print the response
        print("Response status code:", response_data.get('status', 'N/A'))
        print(json.dumps(response_data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()