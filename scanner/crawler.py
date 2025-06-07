# Imports
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

# Checks if two urls have the same domain
def same_domain(url1, url2):
    url1_domain = urlparse(url1).netloc.lower()
    url2_domain = urlparse(url2).netloc.lower()
    return url1_domain == url2_domain
    
# Extracts all relevent links from the webpage of the given url
def extract_links(url):
    global base_url
    global visited_URLs

    # get HTML from given url
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException:
        print(url + "failed to load in extract_links")
        return []  # skip failed pages

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
            visited_URLs.add(link)
            final_links.append(link)

    return final_links

# reccursive helper method
def crawl_helper(curr_url):
    global curr_depth
    global max_link_depth

    # If max depth has been reached, return nothing
    if curr_depth >= max_link_depth:
        return
    curr_depth += 1

    # extract links
    extracted = extract_links(curr_url)
    final = list(extracted)

    for link in extracted:
        # recursively add links inside extracted links
        final += crawl_helper(link)

    return final

# Returns a list of the HTML for each page that is accessable below the given url
def crawl_site(url, max_depth=2):
    # set base
    global base_url
    base_url = url

    # Don't let the program expand infinitely
    global max_link_depth
    max_link_depth = max_depth
    global curr_depth
    curr_depth = 0

    # Keep track of visited as to not get in a loop
    global visited_URLs
    visited_URLs = set()

    # get list of all accessable pages
    URLs = crawl_helper(url)
    URLs.insert(0, url)

    # make list of response objects for each page
    response_list = []
    for link in URLs:
        try:
            response_list.append(requests.get(link, timeout=5))
        except requests.RequestException:
            print(link + "failed to load in crawl_site")
    
    return response_list