from selenium import webdriver
from var.os_actions import OSAction

import requests
import re


class ActionSite(OSAction):

    def __init__(self, file_name=None):
        print('Init ActionSite')
        super().__init__(file_name)
        # self.op = webdriver.FirefoxOptions()
        # self.op.add_argument('--headless')
        # self.op.add_argument('--window-size=1920x935')
        # self.op.set_preference("browser.download.folderList", 2)
        # self.op.set_preference("browser.download.manager.showWhenStarting", False)
        # self.op.set_preference("browser.download.dir", "/tftp/")
        # self.se = webdriver.Firefox(executable_path='./driver/geckodriver', options=self.op)
        self.username = self.site_login()
        self.password = self.site_password()
        self.req = requests

    # def login(self):
    #     self.se.get('http://red.eltex.loc/login')
    #     self.se.find_element('css selector', '#username').send_keys(self.username)
    #     self.se.find_element('css selector', '#password').send_keys(self.password)
    #     self.se.find_element('css selector',
    #                          '#login-form > form > table > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=submit]').click()

    def get_page(self, url, write=False, write_mode='w'):
        # self.se.get(url)
        # page_source = self.se.page_source
        # if write == True:
        #     self.write_in_file(self.se.page_source)
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)
        page_source = self.session.get(url)
        if write == True:
            file = self.get_page(url)
            open(f'{self.tftp_path()}{url.split("/")[-1]}', write_mode).write(file.content)
        return page_source

    def get_serial(self):
        try:
            ip_cpe = '192.168.0.1'
            if self.ping(ip_cpe) is False:
                ip_cpe = '192.168.1.1'
            about_data = self.req.get(f'http://{ip_cpe}/server/api.lua?operation=about')
            cpe_serial = re.search(r'GP\w+', about_data.text)
            return cpe_serial.group(0)
        except requests.exceptions.ConnectionError:
            print('Check CPE Availability!')

    # def close_br(self):
    #     self.se.close()

    def logout(self):
        pass
