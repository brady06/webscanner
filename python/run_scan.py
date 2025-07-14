import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scanner.analyzer import analyze_site


if __name__ == "__main__":
    url = sys.argv[1]
    issues = analyze_site(url, 2)
    issues_data = [
        {"issue": i.issue, "severity": i.severity, "url": i.url}
        for i in issues
    ]
    print(json.dumps(issues_data))
