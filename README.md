# Project Summary
the goal of this project was to create a basic temperature/humidity probe using an:
1. esp8266 board
2. MCP9808 breakout board
3. SHT31 breakout board

programmed in [micropython](https://micropython.org/), sending data to [adafruit.io](https://io.adafruit.com)

#Micropython
This is my first time getting my feet wet with micropython, so comments are welcome, and appreciated. 

# Adafruit REST interface
At the time of writing (august 2017) there was not a prewritten interface for micropython to talk to adafruit.io. So a few functions communicate with the REST api
full documentation on the REST api can be found [https://io.adafruit.com/api/docs/]

```python
def sendValToFeed(user,feedName,value):
```
this function can be used to send data to any feed in your account
```python
def getLastVal(user,feedName):
```
this function retrieves the most recent value from a particular feed.

# The Credentials
In order to communicate with the adafruit.io server you must have an AIO key. To keep my data safe from the cloud ive dumped my username and my AIO key as a json object into a file called aio.key. for obvious reasons, i havent uploaded that file. i have, however, uploaded aio.key.sample which you can modify for your username and key.

if you want to create it programatically, i did the following
```python
import ujson as json
import uio
key={}
key['AIOkey']='youre magic key goes here'
key['username']='your username...'
f = uio.open('aio.key',mode='w')
f.write(json.dumps(key)+"\r\n") # not sure if the \r\n is strictly needed but old unix habits die hard
f.close()
```

# Other files
## boot.py
boot.py has two jobs. first it turns on webREPL. second it blinks the onboard LED everytime the board resets. 
## main.py
this boilerplate file just calls the real code in brv1.py. but i leave it as good practice in case i want to put multiple apps in a project.
