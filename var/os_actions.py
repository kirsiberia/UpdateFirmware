import datetime
import os
from var.config import YamlConfig

class OSAction(YamlConfig):

    def __init__(self, file_name):
        print('Init OSAction')
        if file_name is None:
            file_name = f'data_{datetime.date.today()}.html'
        self.file_name = file_name

    def set_file_name(self, new_file_name):
        self.file_name = new_file_name
        return self.file_name

    def create_file(self):
        open(self.file_name, 'w')

    def write_in_file(self, data):
        with open(self.file_name, 'w') as file:
            file = file.write(data)

    def read_file(self):
        with open(self.file_name, 'r') as file:
            file = file.read()
        return file

    def get_file_name(self):
        return self.file_name

    def download_version(self, url):
        os.system(f'wget -P {self.tftp_path()} {url} > /dev/null 2>&1')
        self.create_img_fw(url)

    def create_img_fw(self, url):
        firmware = url.split('/')[-1]
        os.system(f'cd {self.tftp_path()}; dd if={firmware} of=./img.tar bs=1 skip=1043; rm {firmware}')

    def ping(self, host):
        if os.system(f'ping {host} -c 1 > /dev/null') is 256:
            return False
        return True
