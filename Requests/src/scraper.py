import requests
from bs4 import BeautifulSoup

# Ask the user for the URL
url = input("Enter the URL of the page to scrape: ")

try:
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Extract all the headings (h1, h2, h3, etc.)
    headings = soup.find_all(['h1', 'h2', 'h3'])
    
    # Print the extracted headings
    for heading in headings:
        print(heading.get_text(strip=True))

except Exception as e:
    print(f"An error occurred: {e}")