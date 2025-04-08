import time
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

import socket
socket.getaddrinfo('localhost', 8080)

# Retry mechanism function
def retry_request(url, headers, max_retries=5):
    retries = 0
    while retries < max_retries:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 503:
            print(f"503 error encountered. Retrying... ({retries+1}/{max_retries})")  #503
            retries += 1
            # Exponential backoff: waiting time increases with each retry
            time.sleep(random.randint(5, 15) * 2 ** retries)
        else:
            print(f"Failed with status code {response.status_code}. No retries.")
            break
    return None

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id":'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()
        except:
            price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available

if __name__ == '__main__':
    # New user-agent string
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'})

    URL = "https://www.amazon.co.uk/s?k=plushies&crid=1WZVBGNE4B497&sprefix=plushies%2Caps%2C106&ref=nb_sb_noss_1"

    print("Loading products... Please wait.")  # Display loading message
    
    # HTTP Request
    webpage = retry_request(URL, HEADERS)

    if webpage:
        soup = BeautifulSoup(webpage.content, "html.parser")
        
        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
        
        # Check if any links were found
        if len(links) > 0:
            links_list = [link.get('href') for link in links]
            
            d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}
            
            # Loop for extracting product details from each link
            for link in links_list:
                new_webpage = retry_request("https://www.amazon.co.uk" + link, HEADERS)
                if new_webpage:
                    new_soup = BeautifulSoup(new_webpage.content, "html.parser")
                    
                    d['title'].append(get_title(new_soup))
                    d['price'].append(get_price(new_soup))
                    d['rating'].append(get_rating(new_soup))
                    d['reviews'].append(get_review_count(new_soup))
                    d['availability'].append(get_availability(new_soup))
                    
                    # Add a delay to avoid being blocked
                    time.sleep(2)
            
            amazon_df = pd.DataFrame.from_dict(d)
            amazon_df['title'].replace('', np.nan, inplace=True)
            amazon_df = amazon_df.dropna(subset=['title'])
            
            # Print an example of the data (first 5 rows)
            print("Data scraped successfully!")
            print(amazon_df.head())
            
            # Save data to CSV
            amazon_df.to_csv("amazon_data.csv", header=True, index=False)
        else:
            print("No product links found.")
    else:
        print(f"Failed to retrieve the webpage.")
