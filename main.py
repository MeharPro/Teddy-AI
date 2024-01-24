#Mehar Khanna and Benjamin Davidson, 
#January 23rd 2024, 
#Teddy AI Assistant 

import threading 
from openai import OpenAI 
import speech_recognition as sr 
import pyttsx3 
import RPi.GPIO as GPIO 
import time 
import requests 
import os

client = OpenAI(api_key="OPENAI-KEY") #This will need to be changed to your own API key. Check README.md for more information. 
engine = pyttsx3.init()

API_KEY = 'WEATHERAPI-KEY' #This will need to be changed to your own API key. Check README.md for more information.
BASE_URL = 'http://api.weatherapi.com/v1/current.json'
servoL_pin = 12 #Left servo
servoR_pin = 33 #Right servo
LED_home_pin = 16 #Home LED for program. 
LED_pin = 11 #This is for Brian and Damian, so they can change the pin. 
wake_word = "teddy" 
conversation_mode = False
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_home_pin, GPIO.OUT)
GPIO.setup(LED_pin, GPIO.OUT)
GPIO.setup(servoL_pin, GPIO.OUT)
GPIO.setup(servoR_pin, GPIO.OUT)
pwm = GPIO.PWM(servoL_pin, 50)
pwm1 = GPIO.PWM(servoR_pin, 50)
recognizer = sr.Recognizer()  # Declare the recognizer instance
f = ""

# define class of time
class TimeLord:
    def __init__(self):#run when initialized
        self.seconds = 0
        self.start_time = 0
        self.end_time = 0
        self.alarm_Time = 0
        self.timerActive = False
        self.alarmActive = False
        self.month_dict ={
            1: "January",
            2: "Feburary",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        self.weekDays ={
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

    def setTimer(self, s, t):
        self.start_time = time.time()
        self.end_time = self.start_time+s
        self.timerActive = True

    def setAlarm(self, user_in):
        p = ""
        splt = user_in.split()
        for x in splt:
            if x.rfind(":") > 0:
                self.alarmTime = x.split(":")
                print(self.alarmTime)
                self.alarmActive = True
                p = x
                break
            elif x.isdigit():
                if len(x) == 4:
                    self.alarmTime[0] = x[0:2]
                    self.alarmTime[1] = x[2:4]
                    self.alarmActive = True
                    p = ("{self.alarmTime[0]}:{self.alarmTime[1]}")
                elif len(x) == 3:
                    x = x.zfill(4)
                    self.alarmTime[0] = x[0:2]
                    self.alarmTime[1] = x[2:4]
                    self.alarmActive = True
                    p = ("{self.alarmTime[0]}:{self.alarmTime[1]}")
                else:
                    p = ("{x} is invalid, please try again.")
                    self.alarmActive = False

        say("Setting an alarm for {p}")

    def calcTimer(self, Amount, Type):
        if Type == ("hours"):
            self.seconds = 3600*Amount
        elif Type == ("minutes"):
            self.seconds = 60*Amount
        elif Type == ("seconds"):
            self.seconds = Amount
        tl.setTimer(self.seconds,Type)
        say(f"Setting a timer for {Amount} {Type}")
        return f"Setting a timer for {Amount} {Type}"

    def getTimeLeft(self):
        if self.timerActive == False:
            return None
        return self.end_time-time.time()

    def isTimerFinished(self):
        if (time.time() >= self.end_time and self.timerActive == True):
            self.timerActive = False
            return True
        return False
    def isAlarmFinished(self):
        if (time.localtime(time.time).tm_hour == int(intime[0]) and time.localtime(time.time).tm_min == int(intime[1]) and self.alarmActive == True):
            self.alarmActive == False
            return True
        return False
    def getDate(self):
        wd = self.weekDays[time.localtime(time.time()).tm_wday]
        d = time.localtime(time.time()).tm_mday
        m = self.month_dict[time.localtime(time.time()).tm_mon]
        y = time.localtime(time.time()).tm_year
        return f"today is {wd} {m} {d} {y}"
    def getTime(self):
        return 0       
class AudioLord:
    def __init__(self):
        self.filePath = "~/Music/"
        self.dirPath = ""
    def playFile(self,f):
        print(f"play {self.filePath}{f}")
        os.system(f"play {self.filePath}{f}")
        return 0
# Initialize messages list
messages = [{"role": "assistant", "content": "You are a human assistant named teddy, you're not an AI, and you have personal opinions."}] #Background AI info

# Initialize servo state
servo_position = 7.5  # Default neutral position

tl = TimeLord()
al = AudioLord()
print(tl.getDate())
def say(text, rate=170):
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    params = {'key': API_KEY, 'q': city}
    response = requests.get(BASE_URL, params=params)
    weather_data = response.json()

    if 'error' in weather_data:
        return "Sorry, I couldn't retrieve the weather information at the moment."
    else:
        temperature_c = weather_data['current']['temp_c']
        feels_like_c = weather_data['current']['feelslike_c']
        condition_text = weather_data['current']['condition']['text']
        wind_speed_kph = weather_data['current']['wind_kph']
        wind_direction = weather_data['current']['wind_dir']
        pressure_mb = weather_data['current']['pressure_mb']
        humidity = weather_data['current']['humidity']
        uv_index = weather_data['current']['uv']

        return f"The current weather in {city} is {temperature_c} celsius. " \
               f"It feels like {feels_like_c} celsius. " \
               f"Condition: {condition_text}. " \
               f"Wind speed: {wind_speed_kph} kilometers per hour from {wind_direction}. " \
               f"Pressure: {pressure_mb} millibar. Humidity: {humidity}%. UV Index: {uv_index}."

def process_command(user_input):
    global messages, servo_position
    messages.append({"role": "user", "content": user_input})

    # Weather???
    if any(keyword in user_input for keyword in ["weather", "forecast", "temperature"]) and any(w in user_input for w in ["what", "how"]):
        weather_info = get_weather("Milton")  # We live in Milton, thus Milton.
        say(weather_info)
        messages.append({"role": "assistant", "content": weather_info})

    #Servo command Forward
    elif any(k in user_input for k in ["move", "go", "walk", "run", "sprint"]) and any(f in user_input for f in ["forward", "ahead"]):
        output = ''.join(filter(str.isdigit, user_input))
        if output.isdigit() and int(output) > 0:
            servo_info = f"Moving {output} steps forward"
            say(servo_info)
            pwm.start(0)
            pwm1.start(0)
            time.sleep(0.1)
            pwm.ChangeDutyCycle(5.5) #right
            pwm1.ChangeDutyCycle(7) #left
            time.sleep(int(output))
            servo_position = 12
            pwm.stop(0)
            pwm1.stop(0)
            messages.append({"role": "assistant", "content": servo_info})
        else:
            print("Invalid or no numeric value provided for steps in the command.")

    # Servo command back
    elif any(k in user_input for k in ["move", "go", "walk", "run", "sprint"]) and any(f in user_input for f in ["back", "backwards", "reverse"]):
        output = ''.join(filter(str.isdigit, user_input))
        if output.isdigit() and int(output) > 0:
            servo_info = f"Moving {output} steps back"
            say(servo_info)
            pwm.start(0)
            pwm1.start(0)
            pwm.ChangeDutyCycle(12)
            pwm1.ChangeDutyCycle(10)
            time.sleep(int(output))
            servo_position = 12
            pwm.stop(0)
            pwm1.stop(0)
            messages.append({"role": "assistant", "content": servo_info})
        else:
            print("Invalid or no numeric value provided for steps in the command.")

    # Servo command turn right
    elif any(keyword in user_input for keyword in ["turn", "twist", "move"]) and any(w in user_input for w in ["right", "righty"]):
        servo_info = "Turning right"
        say(servo_info)
        pwm1.start(0)
        pwm1.ChangeDutyCycle(10)
        time.sleep(5)
        servo_position = 12
        pwm1.stop(0)
        messages.append({"role": "assistant", "content": servo_info})

    # Servo command turn left
    elif any(keyword in user_input for keyword in ["turn", "twist", "move"]) and any(w in user_input for w in ["left", "lefty"]):
        servo_info = "Turning left"
        say(servo_info)
        pwm.start(0)
        pwm.ChangeDutyCycle(10)
        time.sleep(5)
        servo_position = 12
        pwm.stop(0)
        messages.append({"role": "assistant", "content": servo_info})

    # LED ON Damian and Brian
    elif any(keyword in user_input for keyword in ["Turn", "Switch"]) and any(w in user_input for w in ["On", "Shiny"]):
        led_info = "Switching light on"
        say(led_info)
        GPIO.output(LED_pin, GPIO.HIGH)
        messages.append({"role": "assistant", "content": led_info})

    # LED OFF Damian and Brian
    elif any(keyword in user_input for keyword in ["Turn", "Switch"]) and any(w in user_input for w in ["Off", "Dark"]):
        led_info = "Switching light off"
        say(led_info)
        GPIO.output(LED_pin, GPIO.LOW)
        messages.append({"role": "assistant", "content": led_info})

    # Timer in seconds
    elif any(k in user_input for k in ["timer", "countdown"]) and any(f in user_input for f in ["second", "seconds"]):
        inNum = int(''.join(filter(str.isdigit, user_input)))
        if inNum > 0:
            tl.calcTimer(inNum, "seconds")
    # Timer in minutes
    elif any(k in user_input for k in ["timer", "countdown"]) and any(f in user_input for f in ["minute", "minutes"]):
        inNum = int(''.join(filter(str.isdigit, user_input)))
        if inNum > 0:
            tl.calcTimer(inNum, "minutes")
    #Timer in hours
    elif any(k in user_input for k in ["timer", "countdown"]) and any(f in user_input for f in ["hour", "hours"]):
        inNum = int(''.join(filter(str.isdigit, user_input)))
        if inNum > 0:
            tl.calcTimer(inNum, "hours")
    #Date
    elif any(k in user_input for k in ["what", "when"]) and any(f in user_input for f in ["date", "today"]):
        output = tl.getDate()
        say(output)
    #play music
    elif any(k in user_input for k in ["play"]) and any(f in user_input for f in ["music", "song"]):
        al.playFile("randommusic.mp3")
    #set alarm
    elif any(k in user_input for k in ["set", "create", "make"]) and any(f in user_input for f in ["alarm", "reminder"]):
        tl.setAlarm(user_input)
    else:
        # Normal Response
        chat = client.chat.completions.create(messages=messages, model="gpt-3.5-turbo", max_tokens=999)
        reply = chat.choices[0].message
        say(reply.content)
        print("Assistant:", reply.content)
        messages.append(reply)

#Function on seperate thread checking if sufficient time has passed
def time_check ():
    jerry = pyttsx3.init()
    while True:
        #print(tl.getTimeLeft())
        if tl.isTimerFinished():
            print("Time sup")
            os.system('play -nq -t alsa synth 5 sine 440')
        if tl.isAlarmFinished():
            print("Alarm done")
            os.system("play -nq -t alsa synth 5 sine 440")
        time.sleep(0.1)
#create thread
t1 = threading.Thread(target = time_check)
t1.start()
# Main loop
try:
    while True:
        print("Listening...")

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=None)  # Set timeout to None for continuous listening

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("You:", user_input)

            if wake_word in user_input:
                process_command(user_input[len(wake_word):])

        except sr.UnknownValueError:
            continue
        except sr.RequestError as e:
            print(f"Error with the speech recognition service; {e}")
            continue

        # Introduce a delay or periodic restart to prevent resource exhaustion
        time.sleep(1)

finally:
    # Set the servo position to the last known state when the program ends
    pwm.start(0)
    pwm.ChangeDutyCycle(servo_position)
    time.sleep(1)
    pwm.stop()
    GPIO.cleanup()



