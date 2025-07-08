import sys
from scanner.analyzer import analyze_site

if __name__ == "__main__":
    print("run_scan called")
    url = sys.argv[1]
    analyze_site(url, 2)
