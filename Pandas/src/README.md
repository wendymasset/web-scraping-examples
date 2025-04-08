# Pandas Web Scraping Example

This directory contains an example of web scraping using the Pandas library. The provided script demonstrates how to extract data from HTML tables on web pages and save it as a CSV file.

## Files

- `scraper.py`: This script uses the Pandas library to scrape the first HTML table from a specified URL and save it as a CSV file.

## Requirements

To run the scraper, you need to have the following Python packages installed:

- pandas

You can install the required packages using pip:

```
pip install pandas
```

## Usage

1. Open a terminal and navigate to the `Pandas/src` directory.
2. Run the scraper script:

```
python scraper.py
```

3. When prompted, enter the URL of the page that contains an HTML table. For example:

```
https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population
```

4. The script will extract the first HTML table from the provided URL and save it as a CSV file in the same directory. The filename will include a timestamp to ensure uniqueness.

5. After the extraction, the script will display a message indicating the name of the saved CSV file and show a preview of the data.

## Example Output

The output will be a CSV file named `extracted_table_YYYY-MM-DD_HH-MM-SS.csv`, where `YYYY-MM-DD_HH-MM-SS` represents the timestamp of when the file was created. The first few rows of the extracted data will also be displayed in the terminal.

## Notes

- Ensure that the URL you provide contains at least one HTML table for the script to work correctly.
- If no tables are found, the script will notify you accordingly.