# Imports

# Object that stores issue data and methods
class Issue:
    def __init__(self, issue, severity, url):
        self.issue = issue
        self.url = url
        self.severity = severity