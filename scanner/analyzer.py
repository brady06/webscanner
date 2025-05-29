# Imports
import crawler
import issue
from bs4 import BeautifulSoup, Comment

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
        HTML_static_checks(response)

    return issues

def check_security_headers(response):
    if "Content-Security-Policy" not in response.headers:
        issues.append(issue.Issue("Missing Content-Security-Policy", response.url))

    if response.headers.get("X-Frame-Options", "").upper() not in ["DENY", "SAMEORIGIN"]:
        issues.append(issue.Issue("Missing or weak X-Frame-Options", response.url))

    if "Strict-Transport-Security" not in response.headers:
        issues.append(issue.Issue("Missing Strict-Transport-Security", response.url))

    if response.headers.get("X-Content-Type-Options", "").lower() != "nosniff":
        issues.append(issue.Issue("Missing or incorrect X-Content-Type-Options", response.url))

    if "Referrer-Policy" not in response.headers:
        issues.append(issue.Issue("Missing Referrer-Policy", response.url))

def HTML_static_checks(response):
    soup = BeautifulSoup(response.text, 'lxml')

    # Forms missing CSRF tokens
    forms = soup.find_all("form")

    for form in forms:
        hidden_inputs = form.find_all("input", type="hidden")
   
        has_csrf = False
        for input in hidden_inputs:
            # "" in case "name" doesn't exist
            if("csrf" in input.get("name", "").lower()):
                has_csrf = True
        if not has_csrf:
            issues.append(issue.Issue("Form missing CSRF token", response.url))

    # Inline javascript
    for script in soup.find_all("script"):
        if not script.get("src") and script.string:
            issues.append(issue.Issue("Inline <script> tag found", response.url))
            break

    # Autocomplete enabled on password field
    passwords = soup.find_all("input", {"type": "password"})
    for password in passwords:
        # default return "on" if the setting doesn't exist
        if password.get("autocomplete", "on").lower() == "on":
            issues.append(issue.Issue("Password input with autocomplete enabled", response.url))

    # Suspicious comments (possible sensitive info)
    sus_words = {
        "password", "secret", "token", "apikey", "debug", "localhost", "internal",
        "auth", "key", "private", "admin", "sql", "db", "ftp", "config", "csrf",
        "xss", "trace", "console.log", "sandbox", "credentials", "access_token"
    }

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        for word in sus_words:
            if word in comment.lower():
                issues.append(issue.Issue("Suspicous comment found in HTML: " + word, response.url))

