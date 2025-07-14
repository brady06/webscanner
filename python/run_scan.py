import os
import sys
import json
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scanner.analyzer import analyze_site


if __name__ == "__main__":
    url = sys.argv[1]
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except requests.RequestException:
        print(json.dumps({"error": "URL not found"}))
        sys.exit(1)

    issues = analyze_site(url, 2)
    issues_data = [
        {"issue": i.issue, "severity": i.severity, "url": i.url}
        for i in issues
    ]
    print(json.dumps(issues_data))
