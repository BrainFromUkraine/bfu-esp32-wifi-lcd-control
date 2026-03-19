from time import sleep_ms
from lcd_api import LcdApi

MASK_RS = 0x01
MASK_RW = 0x02
MASK_E  = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4


class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, bytes([0]))
        sleep_ms(20)

        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        sleep_ms(5)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION_RESET)
        sleep_ms(1)
        self.hal_write_init_nibble(self.LCD_FUNCTION)

        sleep_ms(1)
        LcdApi.__init__(self, num_lines, num_columns)
        cmd = self.LCD_FUNCTION
        if num_lines > 1:
            cmd |= self.LCD_FUNCTION_2LINES
        self.hal_write_command(cmd)

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble >> 4) & 0x0F) << SHIFT_DATA
        self.i2c.writeto(self.i2c_addr, bytes([byte | (1 << SHIFT_BACKLIGHT)]))
        self.i2c.writeto(self.i2c_addr, bytes([byte | MASK_E | (1 << SHIFT_BACKLIGHT)]))
        self.i2c.writeto(self.i2c_addr, bytes([byte | (1 << SHIFT_BACKLIGHT)]))

    def hal_backlight_on(self):
        self.i2c.writeto(self.i2c_addr, bytes([1 << SHIFT_BACKLIGHT]))

    def hal_backlight_off(self):
        self.i2c.writeto(self.i2c_addr, bytes([0]))

    def hal_write_command(self, cmd):
        self.hal_write_byte(cmd, 0)
        if cmd <= 3:
            sleep_ms(5)

    def hal_write_data(self, data):
        self.hal_write_byte(data, MASK_RS)

    def hal_write_byte(self, value, mode):
        high = ((value >> 4) & 0x0F) << SHIFT_DATA
        low = (value & 0x0F) << SHIFT_DATA
        backlight = (1 << SHIFT_BACKLIGHT) if self.backlight else 0

        self.i2c.writeto(self.i2c_addr, bytes([high | mode | backlight]))
        self.i2c.writeto(self.i2c_addr, bytes([high | mode | MASK_E | backlight]))
        self.i2c.writeto(self.i2c_addr, bytes([high | mode | backlight]))

        self.i2c.writeto(self.i2c_addr, bytes([low | mode | backlight]))
        self.i2c.writeto(self.i2c_addr, bytes([low | mode | MASK_E | backlight]))
        self.i2c.writeto(self.i2c_addr, bytes([low | mode | backlight]))