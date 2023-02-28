import time
import serial
from var.config import YamlConfig

class Serial(YamlConfig):

    def __init__(self):
        print('Init Serial')
        self.device = 'ttyUSB0'
        self.ser = serial.Serial(f"/dev/{self.device}", baudrate=115200, timeout=3)

    def send(self, cmd):
        self.ser.reset_input_buffer()
        self.ser.write(bytes(cmd, encoding="utf8") + b"\n")
        time.sleep(0.1)

    def read(self):
        return self.ser.read_all()

    def close_connect(self):
        self.send("exit")
        self.ser.close()

    def reboot(self):
        self.send('reboot')

    def wait_uboot(self):
        self.ser.read_until(b'Hit any key to stop autoboot:')
        self.send('a')
        self.send('eltexpon')

    def wait_prompt(self, prompt):
        self.send('\n')
        res = self.ser.read_until(bytes(prompt, encoding='utf-8'))
        return res

    def connect(self, login, password):
        self.send(login)
        self.send(password)

    def restore(self, login, password):
        self.connect(login, password)
        self.send('flash default cs')
        self.reboot()

    def update_fw_uboot(self, login, password, prompt):
        self.connect(login, password)
        self.reboot()
        self.wait_uboot()
        self.wait_prompt(prompt)
        self.send('setenv serverip 192.168.1.5; setenv ipaddr 192.168.1.10; run upt;')
        self.wait_prompt(prompt)
        self.send('')
        self.send('reset')

    def test(self, login, password):
        self.send('\n')
        if 'assword:' in self.read().decode('utf-8'):
            self.send('\n')
        self.connect(login, password)
if __name__ == '__main__':
    x = Serial()
    x.test('superadmin', 'hLFfqnM3GInaxlPa')
