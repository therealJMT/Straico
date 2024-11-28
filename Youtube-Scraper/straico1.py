import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
STRAICO_API_KEY = os.getenv('STRAICO_API_KEY')
print(f"API Key: {STRAICO_API_KEY}")

def make_api_request(url, headers, data, timeout=30):
    try:
        print(f"Making request to {url}")
        print(f"Request data: {json.dumps(data, indent=2)}")
        
        # Add timeout to the request
        response = requests.post(url, headers=headers, json=data, timeout=timeout)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error response: {response.text}")
            return None
            
        try:
            response_data = response.json()
            return response_data
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            print(f"Response text: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"Request timed out after {timeout} seconds")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Error response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
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

    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    data = {
        "models": ["anthropic/claude-3-haiku:beta"],
        "message": "what is this video about?",
        "youtube_urls": [youtube_url],
        "display_transcripts": False,
        "temperature": 0.7,
        "max_tokens": 500
    }

    print("\nAttempting to analyze YouTube video:", youtube_url)
    print("Using model: anthropic/claude-3-haiku:beta")
    print("Note: Transcript display is disabled")
    response_data = make_api_request(url, headers, data, timeout=60)

    if response_data:
        response_data['youtube_url'] = youtube_url
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"response_{timestamp}.json"
        
        save_response_to_file(response_data, filename)
        
        print("\nResponse data:")
        print(json.dumps(response_data, ensure_ascii=False, indent=2))
    else:
        print("\nTroubleshooting tips:")
        print("1. Verify that the API key is correct")
        print("2. Check if the YouTube video is accessible")
        print("3. Try with a different model")
        print("4. Contact Straico support if the issue persists")
        print("\nPossible issues:")
        print("- The API might be having issues processing YouTube videos")
        print("- The video might be too long or inaccessible")
        print("- There might be rate limiting or other API restrictions")

if __name__ == "__main__":
    main()