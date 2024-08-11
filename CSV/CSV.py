import requests
import json
import csv
import io
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
STRAICO_API_KEY = os.getenv('STRAICO_API_KEY')
API_URL = "https://api.straico.com/v1/prompt/completion"

def make_api_request(message):
    """Make an API request to Straico."""
    headers = {"Authorization": f"Bearer {STRAICO_API_KEY}"}
    data = {
        "models": ["openai/gpt-4o-mini"],
        "message": message,
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None

def extract_csv_content(api_response):
    """Extract CSV content from the API response."""
    completions = api_response.get('data', {}).get('completions', {})
    if not completions:
        print("No 'completions' found in the response")
        return None

    model_key = next(iter(completions))
    message_content = completions[model_key]['completion']['choices'][0]['message']['content']

    csv_parts = message_content.split('```')
    if len(csv_parts) < 3:
        print("No CSV content found between triple backticks")
        return None

    csv_content = csv_parts[1].strip()
    # Remove any language identifier (like 'csv') and leading/trailing whitespace
    csv_content = '\n'.join(line.strip() for line in csv_content.split('\n') if line.strip() and not line.strip().lower() == 'csv')
    return csv_content

def is_valid_csv(csv_string):
    """Check if the string is a valid CSV."""
    try:
        reader = csv.reader(io.StringIO(csv_string), delimiter=';')
        rows = list(reader)
        return len(rows) > 1 and all(len(row) == len(rows[0]) for row in rows)
    except csv.Error:
        return False

def save_csv(csv_string):
    """Save the CSV string to a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        file.write(csv_string)
    
    print(f"CSV file saved as {filename}")

def get_user_input():
    """Prompt the user for an API request message."""
    print("Enter your API request message:")
    return input("> ").strip()

def main():
    """Main function to orchestrate the CSV generation and saving process."""
    user_message = get_user_input()
    
    api_response = make_api_request(user_message)
    if not api_response:
        print("No response received from the API.")
        return

    print("API Response:", json.dumps(api_response, indent=2))

    csv_content = extract_csv_content(api_response)
    if not csv_content:
        print("No CSV content could be extracted from the API response.")
        return

    print("Extracted CSV content:")
    print(csv_content)

    if is_valid_csv(csv_content):
        print("Valid CSV format.")
        save_csv(csv_content)
    else:
        print("Invalid CSV format. Here's what was extracted:")
        print(csv_content)
        print("Please check the API response and adjust the extraction if necessary.")

if __name__ == "__main__":
    main()