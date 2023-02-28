import codecs
import hashlib
import re
import time

import requests.exceptions

from var.bs4_actions import ActionBS
from var.serial_action import Serial
import sys


class UpdateCPE(ActionBS, Serial):

    def __init__(self):
        super().__init__()
        Serial.__init__(self)
        self.model_or_url = sys.argv[1]
        self.version = None
        if len(sys.argv) >= 3:
            self.version = sys.argv[2]
        self.build = None
        if len(sys.argv) >= 4:
            self.build = sys.argv[3]

    def model_name(self):
        rev_b = ''
        valid_model = ['5420',
                       '5421',
                       '5421b',
                       '5440',
                       '52w',
                       'md500',
                       ]
        if self.model_or_url.lower() in valid_model:
            if 'B' in self.model_or_url:
                self.model_or_url = self.model_or_url.strip('B')
                rev_b = '-revb'
            if '5421' in self.model_or_url:
                self.model_or_url = '542x'
            if '5440' in self.model_or_url:
                self.model_or_url = '544x'
            return self.model_or_url + rev_b
        else:
            return

    def find_version(self):

        links = self.links_version()
        model = self.model_name()

        for link in links:
            self.version = self.version.replace('.', '-')
            if model in link and self.version in link:
                if 'revb' not in model and 'revb' not in link:
                        return link
                return link

    def find_build_in_version(self):
        build = self.get_build(self.find_version())
        if self.build == None:
            return build[0]
        for link in build:
            if self.build in link:
                return link

    def check_version(self):
        if self.version is None:
            return False
        return True

    def create_password_for_rtk(self):
        serial = self.get_serial()
        re_pon_sn = re.compile('(>[A-F0-9]{8}<)|(>0200[A-F0-9]{8}<)')
        url = requests.get('http://eltex.loc/mac.php?serial=' + serial.upper())
        pon_sn = re_pon_sn.findall(url.text)
        if (len(pon_sn[0][0]) < len(pon_sn[0][1])):
            pon_sn = pon_sn[0][1]
        else:
            pon_sn = pon_sn[0][0]
        pon_sn = pon_sn[1:-1]
        pw1 = 'ELTEX'
        pw2 = '454C5458' + pon_sn
        pwd = codecs.encode(codecs.decode(hashlib.sha256((''.join([pw1, pw2]).encode())).hexdigest(), 'hex'),
                            'base64').decode()[0:16]
        return pwd

    def set_param_for_login(self):
        """
        :return: list:
        [0] - login for CPE
        [1] - password for CPE
        [2] - prompt UBOOT
        [3] - ip CPE
        """
        prompt = '9607C/9603C#'
        ip ='192.168.1.1'
        if self.ping(ip) is True:
            login = 'admin'
            password = 'kW5i_1bYC6os'
            if self.model_or_url == '52w':
                prompt = '9603CVD#'
        else:
            ip = '192.168.0.1'
            login = 'superadmin'
            password = self.create_password_for_rtk()
        return [login, password, prompt, ip]

    def update_fw(self):
        param = self.set_param_for_login()
        self.update_fw_uboot(param[0], param[1], param[2])
        stop_ping = False
        while stop_ping is False:
            if self.ping(param[3]) == True:
                time.sleep(5)
                stop_ping = True
        self.restore(param[0], param[1])
        self.close_connect()

    def update(self):
        print(self.model_or_url, self.version, self.build)
        if 'http:' in self.model_or_url:
            self.get_page(self.model_or_url, write=True, write_mode='wb')
            self.create_img_fw(self.model_or_url)
        elif '№' in self.model_or_url:
            firmware = self.links_test_version(self.model_or_url.strip('№'))[-1]
            self.get_page(firmware, write=True, write_mode='wb')
            self.create_img_fw(firmware)
        else:
            if not self.check_version():
                print('Enter version!')
                return
            url = self.find_build_in_version()
            self.download_version(url)
        self.update_fw()

if __name__ == '__main__':
    x = UpdateCPE()
    x.update()
