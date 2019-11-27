import re

class Link:
    def __init__(self, base=None, path=None, url=None):
        """
        Creates a sanitized link url using the full url,
        or the combined base and path
        """
        self.url = ''
        if url is not None:
            self.url = Link.sanitize(url)
        elif base is not None and path is not None:
            self.url = Link.sanitize(base + path)
        self.parts = Link.parse(self.url)
        self.schema, self.base, self.port, self.path = self.parts
        self.root = f'{self.schema}://{self.base}'
   
    def __eq__(self, other):
        """
        Compares two Links' to check if they're equal
        """
        return self.url == other.url
    
    def __hash__(self):
        """
        Hashes link url for use in sets, lists, etc.
        """
        return hash(self.url)
    
    def __repr__(self):
        """
        String representation for Links
        """
        return self.url
    
    @staticmethod
    def parse(url):
        """
        Parses a url into its parts, including 
        scheme, base, port, and path with regex
        """
        scheme = '(.*)(?::\/\/)'
        base = '([A-Za-z0-9\-\.]+)'
        port = '(:[0-9]+)?'
        path = '(.*)'
        reg = re.compile(f'^{scheme}{base}{port}{path}$')
        if reg.match(url) is None:
            print(f'not matched: {url}')
            return (None,) * 4
        return reg.match(url).groups()
    
    @staticmethod
    def sanitize(url):
        """
        Sanitize url, removing trailing chars, etc.
        """
        if url.endswith('/'):
            return url[:-1]
        return url
    

if __name__ == "__main__":
    link = Link(url='https://www.nytimes.com/rest-of-path?q=test/')
    thing = Link(url='https://www.nytimes.com/rest-of-path?q=test')
    f = [link, thing]
    print(set(f))
