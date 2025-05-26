# Imports
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

# Base_URL for page
base_url = ""

# Keep track of visited as to not get in a loop
visited_URLs = []

# Checks if two urls have the same domain
def same_domain(url1, url2):
    url1_domain = urlparse(url1).netloc.lower()
    url2_domain = urlparse(url2).netloc.lower()
    return url1_domain == url2_domain
    
# Extracts all relevent links from the webpage of the given url
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
    target_links = []
    for link in norm_links:
        if(same_domain(link, base_url)):
            target_links.append(link)

    # remove link if it has already been visited
    final_links = []
    for link in target_links:
        if(link not in visited_URLs):
            visited_URLs.append(link)
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

def crawl_helper(curr_url):
    # extract links
    extracted = extract_links(curr_url)
    final = extracted

    for link in extracted:
        # recursively add links inside extracted links
        final.append(crawl_helper(link))

    return final

# Returns a list of the HTML for each page that is accessable below the given url
def crawl_site(url):
    # set base
    base_url = url

    # get list of all accessable pages
    URLs = crawl_helper(url)
    URLs.insert(0, url)
    
