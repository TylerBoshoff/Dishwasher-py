import json
import sys
import random
import requests
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import os

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

def sendNotification():
	url = "https://hooks.slack.com/services/T6MJETML1/B03P7M855UL/" + os.environ.get("SLACK_TOKEN")
	message = "Water is coming! :winter: "
	title = "DISHWASHER IS ON"
	slack_data = {
            "username": "TylerBot",
            "icon_emoji": ":water_wave:",
            "channel" : "#office-alerts",
            "attachments": [
                {
                    "color": "#0000FF",
                    "fields": [
                        {
                            "title": title,
                            "value": message,
                            "short": "false",
                        }
                    ]
                }
            ]
        }
	byte_length = str(sys.getsizeof( slack_data ))
	headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
	response = requests.post(url, data=json.dumps(slack_data), headers=headers)
	if response.status_code != 200:
            raise Exception(response.status_code, response.text)



while True: # Run forever
	if GPIO.input(8) == GPIO.HIGH:	
		print("Button was pushed!")
		sendNotification()
            	time.sleep(5)