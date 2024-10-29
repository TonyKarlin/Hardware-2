from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import framebuf

class Scrolling_inputs:
    
    def __init__(self):
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled_width = 128
        self.oled_height = 64
        self.oled = SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)
        self.user_inp_height = 8
        self.x = 0
        self.y = 0
    
    
    def user_input(self):
        self.user_inp = input("Input: ")
        self.oled.text(self.user_inp, self.x, self.y, 1)

    def scroll_input(self):
        self.oled.scroll(self.x, self.y + self.user_inp_height)
        self.oled.fill_rect(self.x, self.y, self.oled_width, self.user_inp_height, 0)
        self.oled.show()



inputs = Scrolling_inputs()

def main():

    while True:
        inputs.user_input()
        inputs.scroll_input()


if __name__ == "__main__":
    main()