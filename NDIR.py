import smbus
import time

class Sensor():
    cmd_measure = [0xFF,0x01,0x9C,0x00,0x00,0x00,0x00,0x00,0x63]
    ppm         = 0

    IOCONTROL   = 0X0E << 3
    FCR         = 0X02 << 3
    LCR         = 0X03 << 3
    DLL         = 0x00 << 3
    DLH         = 0X01 << 3
    THR         = 0X00 << 3
    RHR         = 0x00 << 3
    TXLVL       = 0X08 << 3
    RXLVL       = 0X09 << 3

    def __init__(self, i2c_addr):
        self.i2c_addr = i2c_addr
        self.i2c      = smbus.SMBus(1)

    def begin(self):
        try:
            self.write_register(self.IOCONTROL, 0x08)
        except IOError:
            pass

        self.write_register(self.FCR, 0x07)
        self.write_register(self.LCR, 0x83)
        self.write_register(self.DLL, 0x60)
        self.write_register(self.DLH, 0x00)
        self.write_register(self.LCR, 0x03)

    def measure(self):
        self.write_register(self.FCR, 0x07)
        self.send(self.cmd_measure)
        self.parse(self.receive())

    def parse(self, response):
        checksum = 0

        if len(response) < 9:
            return

        for i in range (0, 9):
            checksum += response[i]

        if response[0] == 0xFF:
            if response[1] == 0x9C:
                if checksum % 256 == 0xFF:
                    self.ppm = (response[2]<<24) + (response[3]<<16) + (response[4]<<8) + response[5]

    def read_register(self, reg_addr):
        time.sleep(0.005)
        return self.i2c.read_byte_data(self.i2c_addr, reg_addr)

    def write_register(self, reg_addr, val):
        time.sleep(0.001)
        self.i2c.write_byte_data(self.i2c_addr, reg_addr, val)

    def send(self, command):
        if self.read_register(self.TXLVL) >= len(command):
            self.i2c.write_i2c_block_data(self.i2c_addr, self.THR, command)

    def receive(self):
        n     = 9
        buf   = []
        start = time.clock()

        while n > 0:
            rx_level = self.read_register(self.RXLVL)

            if rx_level > n:
                rx_level = n

            buf.extend(self.i2c.read_i2c_block_data(self.i2c_addr, self.RHR, rx_level))
            n = n - rx_level

            if time.clock() - start > 0.2:
                break

        return buf
