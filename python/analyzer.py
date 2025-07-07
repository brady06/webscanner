# Imports
import crawler
import issue
from bs4 import BeautifulSoup, Comment
import requests
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse, urljoin

# Returns a list of marked issues and their locations (url)
def analyze_site(url, max_depth):
    # Crawl the site for all relevent links

    response_list = crawler.crawl_site(url, max_depth)

    # Issues list to append to
    global issues
    issues = []

    # main analysis logic
    for response in response_list:
        check_security_headers(response)
        HTML_static_checks(response)
        reflected_xss_check(response)
        test_open_redirect(response)
        test_error_disclosure(response)
        test_admin_accessibility(response)
        test_debug_mode(response)

    return issues

def check_security_headers(response):
    if "Content-Security-Policy" not in response.headers:
        issues.append(issue.Issue("Missing Content-Security-Policy", "MEDIUM", response.url))

    if response.headers.get("X-Frame-Options", "").upper() not in ["DENY", "SAMEORIGIN"]:
        issues.append(issue.Issue("Missing or weak X-Frame-Options", "MEDIUM", response.url))

    if "Strict-Transport-Security" not in response.headers:
        issues.append(issue.Issue("Missing Strict-Transport-Security", "MEDIUM", response.url))

    if response.headers.get("X-Content-Type-Options", "").lower() != "nosniff":
        issues.append(issue.Issue("Missing or incorrect X-Content-Type-Options", "MEDIUM", response.url))

    if "Referrer-Policy" not in response.headers:
        issues.append(issue.Issue("Missing Referrer-Policy", "LOW", response.url))

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
            issues.append(issue.Issue("Form missing CSRF token", "HIGH", response.url))

    # Inline javascript
    for script in soup.find_all("script"):
        if not script.get("src") and script.string:
            issues.append(issue.Issue("Inline <script> tag found", "LOW", response.url))
            break

    # Autocomplete enabled on password field
    passwords = soup.find_all("input", {"type": "password"})
    for password in passwords:
        # default return "on" if the setting doesn't exist
        if password.get("autocomplete", "on").lower() == "on":
            issues.append(issue.Issue("Password input with autocomplete enabled", "LOW", response.url))

    # Suspicious comments (possible sensitive info)
    sus_words = {
        "password", "secret", "token", "apikey", "debug", "localhost", "internal",
        "auth", "key", "private", "admin", "sql", "db", "ftp", "config", "csrf",
        "xss", "trace", "console.log", "sandbox", "credentials", "access_token"
    }

    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        for word in sus_words:
            if word in comment.lower():
                issues.append(issue.Issue("Suspicous comment found in HTML: " + word, "LOW", response.url))

    if not response.url.startswith("https://"):
        issues.append(issue.Issue("Site does not use HTTPS", "LOW", response.url))


# Inject url to see if site reflects response
def reflected_xss_check(response):
    # Insert
    test_insert = "<script>/**/alert('xss')/**/</script>"

    try:
        for param in list(parse_qs(urlparse(response.url).query).keys()):
            test_url = add_param_to_url(response.url, param, test_insert)
            response_test = requests.get(test_url)
            if test_insert in response_test.text:
                issues.append(issue.Issue("Reflected XSS detected", "HIGH", test_url))
                break
    except requests.RequestException:
        print("Request Issue: " + test_url)

# Test rediract url
def test_open_redirect(response):
    # Set up malicious URL
    target = "http://evil.com"
    test_url = response.url + "?redirect=" + target

    # Test whether the site allows the redirect to take place
    try:
        response_test = requests.get(test_url, allow_redirects=False, timeout=5)
        # Get "" if there is no "location"
        location = response_test.headers.get("Location", "")
        if target in location:
            issues.append(issue.Issue("Open redirect detected", "HIGH", test_url))
    except requests.RequestException:
        print("Request Issue: " + response.url)

# Testing whether an error thrown in displayed to the user
def test_error_disclosure(response):
    # url that should cause an error
    test_url = response.url + "?input=%27%22--"  # ' " --

    # check whether common error message words are displayed
    try:
        response_test = requests.get(test_url, timeout=5)
        keywords = ["exception", "stack trace", "sql", "traceback", "error in", "warning:"]
        if any(word in response_test.text.lower() for word in keywords):
            issues.append(issue.Issue("Possible error disclosure / debug info", "HIGH", test_url))
    except requests.RequestException:
        print("Request Issue: " + response.url)

# Tests whether the admin pannel is accessable from a simple link
def test_admin_accessibility(response):
    # common paths to admin panel
    admin_paths = ["/admin", "/admin/login", "/dashboard", "/manage"]
    
    for path in admin_paths:
        test_url = urljoin(response.url, path)
        try:
            response_test = requests.get(test_url, timeout=5)

            # if the page loaded (code 200) and the user wasn't redirected to a login page
            if response_test.status_code == 200 and "login" not in response_test.url.lower():
                issues.append(issue.Issue("Accessible admin panel without authentication", "MEDIUM", test_url))
        except requests.RequestException:
            continue

# Check if turning on debug mode is accessable to users
def test_debug_mode(response):
    # Test turning debug on from url
    debug_url = response.url + "?debug=true"

    try:
        # load debug_url
        response_test = requests.get(debug_url, timeout=5)

        # Common words to indicate that we are in debug mode
        debug_indicators = ["debug mode", "trace", "stack", "env", "config", "print_r"]
        if any(word in response_test.text.lower() for word in debug_indicators):
            issues.append(issue.Issue("Debug mode may be enabled", "MEDIUM", debug_url))
    except requests.RequestException:
        print("Request Issue: " + response.url)

# Properly add a paramater to a url
def add_param_to_url(url, key, value):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    query[key] = value
    new_query = urlencode(query, doseq=True)
    return urlunparse(parsed._replace(query=new_query))