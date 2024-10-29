from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

sw2 = Pin(9, Pin.IN, Pin.PULL_UP)
sw1 = Pin(8, Pin.IN, Pin.PULL_UP)
sw0 = Pin(7, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)


font_height = 8
font_width = 8

ufo = "<=>"
ufo_height = font_height
ufo_width = len(ufo) * font_width

y = int(oled_height - ufo_height)
x = int(oled_width - ufo_width) // 2
colour = 1

def start_up():
    oled.text(ufo, x, y, colour)
    oled.show()

def update():
    global x
    global y
    global colour
    oled.text(ufo, x, y, colour)
    oled.show()
    oled.fill(0)
    
def move_right():
    global x
    x += 1
    if x >= oled_width - ufo_width:
            x = oled_width - ufo_width
            
def move_left():
    global x
    x -= 1
    if x <= 0:
        x = 0
    
def clear():
    oled.show()
    oled.fill(0)
    

def main():
    start_up()
    while True:
        if sw2() == 0:
            move_right()
            update()
            
        elif sw0() == 0:
            move_left()
            update()
            
        elif sw1() == 0:
            clear()
            break

main()
    
    
        
        
        
