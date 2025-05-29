# Imports
import crawler
import issue

# Returns a list of marked issues and their locations (url)
def analyze_site(url):
    # Crawl the site for all relevent links
    response_list = crawler.crawl_site(url)

    # Issues list to append to
    global issues
    issues = []

    # main analysis logic
    for response in response_list:
        check_security_headers(response)

    return issues

def check_security_headers(response):
    if "Content-Security-Policy" not in response.headers:
        issues.append(issue.Issue("Missing Content-Security-Policy", response.url))

    if response.headers.get("X-Frame-Options", "").upper() not in ["DENY", "SAMEORIGIN"]:
        issues.append(issue.Issue("Missing or weak X-Frame-Options"))

    if "Strict-Transport-Security" not in response.headers:
        issues.append(issue.Issue("Missing Strict-Transport-Security"))

    if response.headers.get("X-Content-Type-Options", "").lower() != "nosniff":
        issues.append(issue.Issue("Missing or incorrect X-Content-Type-Options"))

    if "Referrer-Policy" not in response.headers:
        issues.append(issue.Issue("Missing Referrer-Policy"))



