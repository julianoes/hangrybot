#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests
import datetime


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
        request = requests.get(
            "https://www.pizzeria-corona.ch/tagesmenu/",
            headers=headers)
        soup = BeautifulSoup(request.text, 'html.parser')
        # The menu is inside two divs with class row, that's fairly easy
        # to read.
        for p in soup.select('div.page-content p'):
            for line in p.text.split('\n'):
                if line == "":
                    continue
                if u"Menü " in line or "Tagespizza" in line:
                    self.menus.append(Menu(line))
                    continue
                if "CHF" in line:
                    continue
                if self.menus:
                    self.menus[-1].text += line + "\n"


class BackmarktCrawler(MenuCrawler):
    def _crawl_menus(self):
        headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) '
                   'Gecko/20100101 Firefox/40.1'}
        request = requests.get(
            "http://www.backmarkt.ch/restaurant/menu/wocheodd.html",
            headers=headers)

        now = datetime.datetime.now()
        day_of_month = now.day
        year = now.year

        our_day_active = False
        soup = BeautifulSoup(request.text, 'html.parser')
        for h2 in soup.select('div#contentBlock-1 div h2'):
            day_in_german, date_in_german = h2.text.split(",")
            day_of_month_parsed, _ = date_in_german.split(".")
            if day_of_month == int(day_of_month_parsed) \
                    and str(year) in h2.text:
                our_day_active = True
            elif our_day_active and str(year) in h2.text:
                our_day_active = False

            if our_day_active:
                for div in h2.parent.next_sibling.select('div div p'):
                    if u"menü " in div.text or u"menu" in div.text:
                        self.menus.append(Menu(div.text))
                        continue
                    if u"Menüsalat" in div.text or u"Menusalat" in div.text:
                        continue
                    # Don't add empty lines.
                    if self.menus and div.text.strip():
                        self.menus[-1].text += div.text + "\n"


def main():
    # This is just to quickly test the crawling.
    corona_crawler = CoronaCrawler()
    print("Corona:")
    print(corona_crawler.get_menus())

    backmarkt_crawler = BackmarktCrawler()
    print("Backmarkt:")
    print(backmarkt_crawler.get_menus())


if __name__ == '__main__':
    main()
