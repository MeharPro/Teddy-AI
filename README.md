Hey there! Thanks for using our AI bot, Teddy. - Mehar and Ben

T-TACTAL

E-ENHANCED

D-DIGITAL

D-DECISION-MAKING

Y-YOTTACORE

**General Information**
We've made a moving AI robot assistant with servos using a RaspberryPi, able to move on command, talk using its voice and mic input, and retrieve past conversations, and as it's using OpenAIs GPT-3.5-turbo, it's not limited to any conversation.  
This bot uses OpenAI, and WeatherAPI, and it's not limited to any other AI implementation. 
The code is commented with the necessary information. 
All of the code is compiled into one .py file since it would require fewer modifications when uploading the code to a Raspberry.

**IMPORTANT NOTICE**
Every import mentioned at the beginning of the code requires installation on the actual machine. 

**FUN COMMANDS** 
***"Teddy" is a wake word.***
"Teddy, how's the weather today?"
"Teddy, move 20 steps forward."
"Teddy, play music."
"Teddy, who are you?"
"Teddy, what makes you human?"
"Teddy, what did I say before?"
"Teddy, what can you do?"
"Teddy, what is your opinion about AI?"
There are so many more inputs that we would love to include here, so try out EVERYTHING. 

**OpenAI API Issues**
OpenAI has strict policy usage when it comes to using the use of prompts.
Thus, be careful when using certain prompts, background info, etc, as it may permanently ban your API key.

How to get an API key?
1. Go to openai.com
2. Create a free account
3. Head to the API key page, you may need to input a valid phone number to be eligible for the free trial.
4. Now click "Create API key", and input it into the code.

**WeatherAPI Issues**
The WeatherAPI shouldn't have any issues per se, though if their policies do change about "free for life," it may cause problems.
Weather code isn't vital to the program working, so even if the API key is not there, the code will function, as long as there is an OpenAI key. 

How to get a WeatherAPI key?
1. Sign up for a free account
2. Go to your main dashboard and input the API key there, to the code.

**Other API Issues**
This code uses only OpenAI and WeatherAPI, if you have added your own API, check its implementation in the code, and further documentation.
It goes for any API key used in the code, make sure to never give out your API key, especially the OpenAI key, it will be tracked, and the key will be banned.

**FAQs**
**Is the program running?**
If you've connected an LED to the LED_home_pin, then it will always light on, once the program is running, if it detects a wake word, it will turn off for a moment. 

**Why is it not listening or the delay?**
Delay occurrence varies upon the input device used to input audio into the Raspberry Pi to the API key receiving and sending a request. 
So if you're having a delay, check your microphone, or output. 
Delays are inevitable, we're not Google, so all in all refresh the Raspberry Pi. 

**Can I change the wake-word?**
YES! Change it to whatever you like, "Teddy" was an easy wakeword for us to say, and it's the reason why we chose it. 
Under the wake-word variable, you'll see a string that says "teddy", replace it with whatever you like, make sure it's English and a common word though. 
Keynote* Don't put more than one wake word, it will not function. 

If you have any questions about the code, feel free to email me at imeharkhanna8@gmail.com. 

