#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests


class Menu(object):
    def __init__(self, title):
        self.title = title
        self.text = ""


class MenuCrawler(object):
    def __init__(self):
        self.menus = []

    def get_menus(self):
        self._crawl_menus()
        menus = ""
        for menu in self.menus:
            menus += menu.title + ":\n" + menu.text + "\n"
        return menus


class CoronaCrawler(MenuCrawler):
    def _crawl_menus(self):
        # We get a 403 Forbidden if we don't provide some kind of user agent.
        headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) '
                   'Gecko/20100101 Firefox/40.1'}
        request = requests.get("https://www.pizzeria-corona.ch/tagesmenu/",
                               headers=headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        # The menu is inside two divs with class row, that's fairly easy
        # to read.
        for p in soup.select('div.row div.row p'):
            line = p.text
            if line == "":
                continue
            if u"Menü " in line or "Tagespizza" in line:
                self.menus.append(Menu(line))
                continue
            if "CHF" in line or "Suppe oder Salat" in line:
                continue
            if self.menus:
                self.menus[-1].text += line + "\n"


def main():
    # This is just to quickly test the crawling.
    corona_crawler = CoronaCrawler()
    print(corona_crawler.get_menus())


if __name__ == '__main__':
    main()
