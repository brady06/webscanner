# Imports
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

base_url = ""

# Checks if two urls have the same domain
def same_domain(url1, url2):
    url1_domain = urlparse(url1).netloc.lower()
    url2_domain = urlparse(url2).netloc.lower()
    return url1_domain == url2_domain
    

# Function: extract_links()
# - Takes raw HTML and base URL
# - Parses it with BeautifulSoup
# - Finds <a href="..."> tags and normalizes them with urljoin
# - Filters out external links
def extract_links(url):
    # get HTML from given url
    response = requests.get(url)

    # parse all <a> tags with href value
    soup = BeautifulSoup(response.text, 'lxml')
    links = [a['href'] for a in soup.find_all('a', href=True)]

    # normalize by adjoining base url if it is not included
    norm_links = []
    for link in links:
        norm_links.append(urljoin(base_url, link))

    # only consider a url if it is in the target scope
    final_links = []
    for link in norm_links:
        if(same_domain(link, base_url)):
            final_links.append(link)

    return final_links

# Function: crawl_site()
# - Takes start URL and max depth
# - Uses BFS or DFS to visit pages
# - Keeps track of visited URLs
# - For each page:
#     - download it
#     - if it's HTML, parse and extract links
#     - enqueue unvisited links for further traversal
# - Returns: list or set of discovered page URLs
