import sys
from scanner.analyzer import analyze_site

if __name__ == "__main__":
    url = sys.argv[1]
    analyze_site(url, 2)
