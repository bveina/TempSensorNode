# Project Summary
The goal of this project was to create a basic temperature/humidity probe using an:
1. esp8266 board
2. MCP9808 breakout board
3. SHT31 breakout board
4. Programmed in [micropython](https://micropython.org/)
5. Sending data to [adafruit.io](https://io.adafruit.com)

# Micropython
This is my first time getting my feet wet with micropython, so comments are welcome, and appreciated. 

# AdafruitIO
adafruit.io is the backend for this IOT project and comes in two parts the rest interface to the backend and the io dashboard interface

## REST interface
At the time of writing (august 2017) there was not a prewritten interface for micropython to talk to adafruit.io. So a few functions communicate with the REST api

full documentation on the REST api can be found [https://io.adafruit.com/api/docs/]

```python
def sendValToFeed(user,feedName,value):
```
sendValToFeed can be used to send data to any feed in your account
```python
def getLastVal(user,feedName):
```
getLastVal retrieves the most recent value from a particular feed.

# Dashboard interface
![io-dashboard](https://github.com/bveina/TempSensorNode/blob/master/docs/IOdashboardSetup.PNG "Sample IO dashboard ")
this project uses 5 total feeds. three feeds are data, the data is sourced from the sensors through the esp8266 and upto the server
1. foo - temperature in C from the MCP9808
2. BasementTempF - temperature in F from the SHT31
3. BasementRH - relative humidity from the SHT31

two feeds are control
1. ctrl - acts as an on/off switch when ctrl == 0 the sensor does not continuously read it drops out of the main code and the webREPL prompt is made available. 
2. UpdateTime - sets the time (in minutes) the sensor will sleep between sensor readings. 

both control feeds are checked only when the node takes a reading. so if you change a value on the server, while the sensor is asleep nothing will change until the next wakeup period.

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
