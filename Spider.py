from lxml import html
import requests
import json
from Link import *


class Spider:
    def __init__(self, levels=2):
        self.levels = levels
        self.links = [] # list[Link]
        self.web = {} # int: list[int]
    
    def build_web(self, start_url):
        """
        Starts at the given URL and builds a web that
        is levels deep using BFS. Uses helper function 
        crawl, to visit, connect, and mark sites.
        """
        self.links = [Link(url=start_url)]
        Q = [0]
        for _ in range(self.levels):
            level = []
            for link_id in Q:
                origin = self.links[link_id]
                links = self.crawl(origin) # list[Link]
                for link in links:
                    conn = self.web.get(link_id, [])
                    if link in self.links:
                        i = self.links.index(link)
                        self.web[link_id] = conn + [i]
                        continue
                    i = len(self.links)
                    self.links.append(link)
                    self.web[link_id] = conn + [i]
                    level.append(i)
            Q = level
        self.save_links('links.json')
        self.save_web('web.json')
        return
    
    def crawl(self, origin):
        """
        Crawls to URL and returns a unique, sanitized list
        of all links associated with this site.
        """
        res = requests.get(origin.url)
        page = html.fromstring(res.content)
        # build unique set of Links with hrefs
        links = set()
        for href in page.xpath('//a/@href'):
            if href.startswith('http'):
                link = Link(url=href)
            else:
                link = Link(base=origin.root, path=href)
            links.add(link)
        return list(links)
    
    def save_links(self, file_path):
        """
        Saves all visited links with their link id for
        the web, and later use.
        """
        with open(file_path, 'w+') as file:
            links = {i: link.url for i, link in enumerate(self.links)}
            data = json.dumps(links, indent=2)
            file.write(data)
        return
    
    def save_web(self, file_path):
        """
        Saves the built web including connections between
        all links in a graph like structure.
        """
        with open(file_path, 'w+') as file:
            web = json.dumps(self.web, indent=2)
            file.write(web)
        return
    
    def save(self, link_path='links.json', web_path='web.json'):
        self.save_links(link_path)
        self.save_web(web_path)

