import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_site_name_with_requests(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <meta> tag with property="og:site_name"
        meta_tag = soup.find('meta', {'property': 'og:site_name'})

        if meta_tag:
            content = meta_tag.get('content')
            return content,True
        else:
            domain = extract_domain(url)
            return domain,False
            print('No meta tag found with property="og:site_name"')

    except requests.exceptions.RequestException as e:
        domain = extract_domain(url)
        return domain,False
        print(f'Error: {e}')

