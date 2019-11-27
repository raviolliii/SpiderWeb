from sys import argv
from Spider import *


def main():
    start_url = argv[1]
    spider = Spider(levels=2)
    spider.build_web(start_url)
    spider.save()


if __name__ == "__main__":
    main()
