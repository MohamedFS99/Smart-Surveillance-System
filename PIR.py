#Import Required Libraries
import nexmo
import datetime
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime


#PIR sensor pin
pir_pin = 17

#Declare pin functions as input
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pir_pin, GPIO.IN)


def send_sms_msg():
    message = 'Intruder Alert in '+str(datetime.now())
    
    client = nexmo.Client(key='***', secret='***')
    client.send_message({
        'from': 'Vonage APIs',
        'to': '9715xxxxxxx',
        'text': message,
    })

while True:
    try:
        #Read input value of the pin
        State = GPIO.input(pir_pin)
        #When the output value nof the pin is 0
        if State == GPIO.LOW:
            print("No Motion Detected, no Intruder", State)
            sleep(0.1)
        #When the output value nof the pin is 1
        elif State == GPIO.HIGH:
            print("Motion Detected, There is an Intruder", State)
            send_sms_msg()
            sleep(5)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
    
