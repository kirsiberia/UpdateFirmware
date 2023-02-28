import yaml

class YamlConfig():

    def open_config_file(self):
        with open('./config/config.yaml', 'r') as config:
            return yaml.safe_load(config)

    def site_login(self):
        return self.open_config_file()['login_redmine']

    def site_password(self):
        return self.open_config_file()['password_redmine']

    def serial_device(self):
        return self.open_config_file()['serial_device']

    def tftp_path(self):
        return self.open_config_file()['tftp_path']

    def ip_tftp(self):
        return self.open_config_file()['ip_tftp']

if __name__ == '__main__':
    x = YamlConfig()
    print(x.ip_tftp() + '0')
