# Imports
# - requests or httpx
# - BeautifulSoup
# - urlparse, urljoin, etc.
from urllib.parse import urlparse, urljoin

# Function: is_same_domain()
# - Compares two URLs to check if they belong to the same site
def is_same_domain(url1, url2):
    url1_domain = urlparse(url1).netloc.lower()
    url2_domain = urlparse(url2).netloc.lower()
    return url1_domain == url2_domain
    

# Function: extract_links()
# - Takes raw HTML and base URL
# - Parses it with BeautifulSoup
# - Finds <a href="..."> tags and normalizes them with urljoin
# - Filters out external links

#def extract_links():


# Function: crawl_site()
# - Takes start URL and max depth
# - Uses BFS or DFS to visit pages
# - Keeps track of visited URLs
# - For each page:
#     - download it
#     - if it's HTML, parse and extract links
#     - enqueue unvisited links for further traversal
# - Returns: list or set of discovered page URLs
