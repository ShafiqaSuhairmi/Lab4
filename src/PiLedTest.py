import RPi.GPIO as GPIO  # Import RPi.GPIO module
import time  # Import time for delay functions
from hal import hal_led as led  # Import LED module

def init():
    GPIO.setmode(GPIO.BCM)  # Choose BCM mode
    GPIO.setwarnings(False)
    GPIO.setup(22, GPIO.IN)  # Set GPIO 22 as input (for switch)
    GPIO.setup(24, GPIO.OUT)  # Set GPIO 24 as output (for LED)

def read_slide_switch():
    # Read the state of the slide switch
    return GPIO.input(22)

def blink_led(frequency, duration):
    # Initialize the LED
    led.init()
    
    # Calculate the delay for the given frequency
    delay = 1 / (2 * frequency)  # Half-period for on/off cycle

    # Blink the LED for the specified duration (in seconds)
    end_time = time.time() + duration
    while time.time() < end_time:
        led.set_output(0, 1)  # Turn LED on
        time.sleep(delay)
        led.set_output(0, 0)  # Turn LED off
        time.sleep(delay)

def main():
    init()  # Initialize GPIO and setup
    try:
        if read_slide_switch() == 0:  # Switch moved to left position
            # Blink at 5 Hz indefinitely until switch changes
            while read_slide_switch() == 0:
                blink_led(5, 1)  # Blink at 5 Hz with 1-second chunks to keep checking switch state
        else:  # Switch moved to the right position
            blink_led(10, 5)  # Blink at 10 Hz for 5 seconds
            GPIO.output(24, False)  # Turn off LED after blinking
    finally:
        GPIO.cleanup()  # Clean up GPIO pins

# Main entry point
if __name__ == "__main__":
    main()
