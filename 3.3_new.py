from filefifo import Filefifo
from fifo import Fifo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

class Values:
    def __init__(self):
        self.data = Filefifo(10, name = 'capture_250Hz_03.txt')
        self.val_amnt = 1000
        self.values = []
        self.min_val = float("inf")
        self.max_val = float("-inf")
        
    
    def get_values(self): # Gets a set amount of values from Filefifo and appends them in to a list 
        for _ in range(self.val_amnt):
            value = self.data.get()
            self.values.append(value)
            self.min_val = min(self.min_val, value) # Gets min value from the data
            self.max_val = max(self.max_val, value) # Gets max value from the data
        print(f"min val: {self.min_val}\nmax val: {self.max_val}")
     
       
vals = Values()       



class Screen:
    def __init__(self):
        self.oled_width = 128
        self.oled_height = 64
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled = SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)
    


screen = Screen()



class Encoder:
    def __init__(self, rot_a, rot_b):
        self.fifo = Fifo(30, typecode = 'i')       
        self.a = Pin(rot_a, mode = Pin.IN)
        self.b = Pin(rot_b, mode = Pin.IN)
        self.a.irq(handler = self.handler, trigger = Pin.IRQ_RISING, hard = True)
        
    def handler(self, pin):
        if self.b():
            self.fifo.put(-2)
        else:
            self.fifo.put(2)
            
            
rot = Encoder(10, 11)   



class Sine_Wave:
    def __init__(self):
        self.pixels = []
        self.x = 0


    def scaled_values(self): # Scales the values we got from the file to fit into the Y-axis (0-64)
        for item in vals.values:
            self.scaled_value = int(((item - vals.min_val) / (vals.max_val - vals.min_val)) * 64)
            #self.pixels.append(scaled_value) # Appends scaled values to a new list
            
    
    def draw(self): # Draws the scaled values as pixels representing a sine wave on the oled screen
        screen.oled.fill(0)
        
        if self.x < 0: # Prevents scrolling when at left edge
            self.x = 0
        elif self.x >= len(self.pixels) - 127: # Prevents scrolling when at right edge
            self.x = len(self.pixels) - 128
        
        for i in range(128): # Draws the sine wave filling the X-axis (0-128)
            #screen.oled.pixel(i, self.pixels[self.x + i], 1)
            screen.oled.pixel(i, self.scaled_value, 1)
            
    def update(self): # Updates the screen
        self.draw()
        screen.oled.show()
            
            
    def scroll(self, amnt): # Enables scrolling with the rotary encoder
        self.x += amnt

            


sine = Sine_Wave()     


def main(): # Main loop
    vals.get_values()
    sine.scaled_values()
    print(f"Amnt of vals: {len(sine.pixels)}")
    sine.draw()
    
    while True:
        while rot.fifo.has_data():
            sine.scroll(+rot.fifo.get())
        
        sine.update()
    
    
if __name__ == "__main__":  
    main()