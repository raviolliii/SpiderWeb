from lxml import html
import requests
from sys import argv
import json


class Spider:
    def __init__(self, levels=2):
        self.levels = levels
        self.links = []
        self.web = {}
    
    def build_web(self, start_url):
        """
        Starts at the given URL and builds a web that
        is levels deep using BFS. Uses helper function 
        crawl, to visit, connect, and mark sites.
        """
        self.links = [start_url]
        Q = [0]
        for _ in range(self.levels):
            level = []
            for link in Q:
                urls = self.crawl(self.links[link])
                unq = [u for u in urls if u not in self.links]
                level += [i + len(self.links) for i in range(len(unq))]
                self.web[link] = level
            self.links += unq
            Q = level
        self.save_links('links.json')
        self.save_web('web.json')
        return
    
    def crawl(self, url):
        """
        Crawls to URL and returns a unique, sanitized list
        of all links associated with this site.
        """
        res = requests.get(url)
        page = html.fromstring(res.content)
        # build unique links set
        links = set()
        for href in page.xpath('//a/@href'):
            if href.startswith('http'):
                links.add(href)
        return list(links)
    
    def save_links(self, file_path):
        """
        Saves all visited links with their link id for
        the web, and later use.
        """
        with open(file_path, 'w+') as file:
            links = {i: link for i, link in enumerate(self.links)}
            data = json.dumps(links, indent=2)
            file.write(data)
        return
    
    def save_web(self, file_path):
        """
        Saves the built web including connections between
        all links in a graph like structure.
        """
        with open(file_path, 'w+') as file:
            web = json.dumps(self.web)
            file.write(web)
        return


if __name__ == "__main__":
    start_url = argv[1]
    spider = Spider(2)
    spider.build_web(start_url)
