import RPi.GPIO as GPIO
import time
from pylepton_capture import * 

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        pics = 10
        for count in range(pics):
           image = capture(flip_v=False, device = "/dev/spidev0.1")
           cv2.imwrite('image_%03d.tiff'%(count),image)

        time.sleep(0.2)
