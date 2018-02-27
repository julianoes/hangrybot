#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests


class Menu():
    def __init__(self, title):
        self.title = title
        self.text = ""


class MenuCrawler(object):
    def __init__(self):
        self.menus = []


class CoronaCrawler(MenuCrawler):
    def get_menus(self):
        self._crawl_menus()
        menus = ""
        for menu in self.menus:
            menus += menu.title + ":\n" + menu.text + "\n"
        return menus

    def _crawl_menus(self):
        headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) '
                   'Gecko/20100101 Firefox/40.1'}
        request = requests.get("https://www.pizzeria-corona.ch/tagesmenu/",
                               headers=headers)
        soup = BeautifulSoup(request.text, 'html.parser')
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
    corona_crawler = CoronaCrawler()
    print(corona_crawler.get_menus())


if __name__ == '__main__':
    main()
