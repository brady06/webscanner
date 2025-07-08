import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scanner.analyzer import analyze_site

if __name__ == "__main__":
    print("run_scan called")
    url = sys.argv[1]
    analyze_site(url, 2)
