# Straico API CSV Extractor

This Python script interacts with the Straico API, extracts CSV content from the API response, and saves it to a file. It is designed to handle the communication with the API, parse the response, validate the CSV format, and save the data locally.

## Features

- Sends a request to the Straico API with a user-defined message.
- Extracts CSV content from the API response.
- Validates the CSV format.
- Saves the extracted CSV content to a timestamped file.

## Requirements

- Python 3.7 or higher
- `requests`
- `python-dotenv`

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>

### Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies. Run the following commands:

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### Environment Variables

This project uses environment variables to manage the API key securely. Create a `.env` file in the root directory of the project and add your Straico API key:

```bash
STRAICO_API_KEY=your_api_key_here
```

## Usage

To run the script, use the following command:

```bash
python main.py
```

### Workflow

1. The script will prompt you to enter a message for the API request.
2. It sends the request and processes the API response.
3. If CSV content is found and validated, it will be saved to a file with a timestamped filename.
4. If the CSV is invalid, the script will notify you and print the extracted content for manual review.

## License

This project is licensed under the MIT License.
```

Let me know if you would like me to add an MIT license file, and if so, provide the year and name it should be attributed to.
