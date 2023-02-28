from bs4 import BeautifulSoup
from var.site_actions import ActionSite


class ActionBS(ActionSite):

    def __init__(self):
        print('Init ActionBS')
        super().__init__()

    def beautiful_soup(self, url):
        self.soup = BeautifulSoup(self.get_page(url).text, 'lxml')
        return self.soup

    def links_version(self):
        link = []
        for href in self.beautiful_soup('http://red.eltex.loc/projects/gpon/wiki').findAll('a', class_='wiki-page'):
            link.append('http://red.eltex.loc' + href.get('href'))
        return link

    def links_test_version(self, task):
        link = []
        for href in self.beautiful_soup(f'http://red.eltex.loc/issues/{task}').findAll('a', class_='icon icon-attachment'):
            if '.bin' in href.get('href'):
                link.append('http://red.eltex.loc' + href.get('href'))
        return link

    def get_build(self, link_version):
        build = []
        for href in self.beautiful_soup(link_version).findAll('a'):
            if 'ftp://' in str(href.get('href')):
                build.append(href.get('href'))
        return build
