# Web Scraping with Requests

This project demonstrates how to use the Requests library to scrape web pages. The `scraper.py` file contains a simple web scraping script that retrieves content from a specified URL and extracts relevant data.

## Getting Started

### Prerequisites

Make sure you have Python installed on your machine. You will also need to install the Requests library if you haven't already:

```bash
pip install requests
```

### Running the Scraper

1. Open the `scraper.py` file in your preferred code editor.
2. Modify the URL variable in the script to point to the web page you want to scrape.
3. Run the script using the following command:

```bash
python scraper.py
```

### What Data is Extracted

The scraper retrieves the HTML content of the specified web page and extracts specific data points based on the logic defined in the script. You can customize the extraction logic to suit your needs.

## Example Usage

Here is a simple example of how to use the scraper:

```python
import requests

url = 'https://example.com'
response = requests.get(url)

if response.status_code == 200:
    print(response.text)  # Print the HTML content of the page
else:
    print(f"Failed to retrieve data: {response.status_code}")
```

Feel free to modify the example and explore different web pages!