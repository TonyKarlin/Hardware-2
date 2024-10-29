from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C
import time


class Line:

    def __init__(self):  # Initial values of the Class.
        self.sw2 = Pin(9, Pin.IN, Pin.PULL_UP)
        self.sw1 = Pin(8, Pin.IN, Pin.PULL_UP)
        self.sw0 = Pin(7, Pin.IN, Pin.PULL_UP)
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
        self.oled_width = 128
        self.oled_height = 64
        self.oled = SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)

    def start_pos(self):  # Sets a starting position for the line/pixel.
        self.x = 0
        self.y = self.oled_height // 2
        self.colour = 1

        self.oled.pixel(self.x, self.y, self.colour)

    def move(self):  # Moves the line forwards.
        self.x += 1
        self.oled.pixel(self.x, self.y, self.colour)
        self.oled.show()

    def draw_up(self):  # Draws the line upwards.
        self.y += 1
        if self.y >= self.oled_height:
            self.y = self.oled_height - 1

    def draw_down(self):  # Draws the line downwards.
        self.y -= 1
        if self.y <= 0:
            self.y = 1

    def clear(self):  # Clears the display
        self.oled.fill(0)
        self.oled.show()

    def cross_screen(self):  # Resets x coordinate
        self.x = 0

    def reset(self):  # Resets the position of the line when sw1 is pressed,
        # but also returns a Boolean value if button is held down for a certain amount of time.
        # Amount of time the program wants the button to be held down.
        duration_threshold = 1

        if self.sw1.value() == 0:
            self.clear()
            self.start_pos()
            # Sets a time value when "sw1" is first pressed down.
            start_time = time.time()

            while self.sw1.value() == 0:
                # Subtracts the initial start time with the time the button has been held down for and checks if it reaches the duration threshold.
                # If threshold is reached program returns "True".
                if time.time() - start_time >= duration_threshold:
                    return True

    def shut_down(self):
        # Gives a centered shut down message to the user on the OLED display.
        shut_dwn_msg = "Shut down"
        msg_width = len(shut_dwn_msg) * 8
        msg_height = 8
        self.oled.text(
            shut_dwn_msg,
            (self.oled_width - msg_width) // 2,
            (self.oled_height - msg_height) // 2,
        )
        self.oled.show()


lines = Line()  # Creates an instance of the class Line.


def main():
    # Initializes a starting position for our line in the main function.
    lines.start_pos()

    while True:
        lines.move()  # Starts the movement of the line.

        if lines.x >= lines.oled_width:  # Resets x coordinate of the line
            lines.cross_screen()  # when it reaches right edge of the screen.

        if lines.sw2.value() == 0:  # Draws upwards on button press/hold
            lines.draw_up()
        elif lines.sw0.value() == 0:    # Draws downwards on button press/hold
            lines.draw_down()
        elif lines.sw1.value() == 0:  # Resets the position of the line
            lines.reset()
            # If reset() function returns "True", loop breaks and the program is shut down.
            if lines.reset():
                lines.clear()   # Clears a trashy pixel on the edge of the screen
                lines.shut_down()   # Displays the shut down message to the user
                time.sleep(2)   # for 2 seconds,
                lines.clear()   # before it clears the display.
                break


if __name__ == "__main__":
    main()
