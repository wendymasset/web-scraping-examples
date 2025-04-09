# Dynamic Web Scraping
# This script scrapes the first HTML table from a given URL and saves it as a CSV file.
# It also displays an example of the content in the CSV file.

import pandas as pd
from datetime import datetime

# Ask the user for the URL
url = input("Enter the URL of the page that contains an HTML table: ") #Example: https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population

try:
    # Read the tables from the URL
    tables = pd.read_html(url)
    
    if len(tables) == 0:
        print("No tables found on that page.")
    else:
        df = tables[0]  # Take the first table
        
        # Create a dynamic filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_filename = f"extracted_table_{timestamp}.csv"
        
        # Save the CSV file
        df.to_csv(csv_filename, index=False)
        
        # Step 5: Display a message and an example of the content
        print(f"\nCSV saved as: {csv_filename}")
        print("\nHere is an example of the CSV created:\n")
        print(df.head())

except Exception as e:
    print(f"An error occurred: {e}")