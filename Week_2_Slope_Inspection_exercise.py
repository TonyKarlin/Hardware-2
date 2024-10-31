from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
from filefifo import Filefifo 


data = Filefifo(10, name = 'capture_250Hz_01.txt') 
for _ in range(100): 
    print(data.get())
    
