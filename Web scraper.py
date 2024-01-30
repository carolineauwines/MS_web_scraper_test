import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def search_website_recursive(url, target_word, visited_pages=set()):
    # Add the current URL to the set of visited pages
    visited_pages.add(url)

    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all instances of the target word in the text content
        occurrences = soup.body(text=lambda text: target_word.lower() in text.lower())
        if occurrences:
            print(f"The word '{target_word}' was found on the page: {url}")
            print(f"Total occurrences on this page: {len(occurrences)}")

        # Find all links on the page
        links = soup.find_all('a', href=True)

        # Extract the absolute URLs and filter out external links
        absolute_urls = [urljoin(url, link['href']) for link in links]
        internal_urls = [absolute_url for absolute_url in absolute_urls if urlparse(absolute_url).netloc == urlparse(url).netloc]

        # Crawl each internal link if it hasn't been visited yet
        for internal_url in set(internal_urls) - visited_pages:
            search_website_recursive(internal_url, target_word, visited_pages)

    else:
        print(f"Failed to retrieve the page {url}. Status code: {response.status_code}")

url_to_scrape = 'https://thehatstore.com.au/'
search_word = 'afterpay'

search_website_recursive(url_to_scrape, search_word)

