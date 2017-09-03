import ustruct
from machine import Pin,I2C
import time

MCP9808_addr = 0x18
SHT31_add =68
i2c=I2C(sda=Pin(4),scl=Pin(5),freq=100000)

def CtoF(x):
    return x*9./5+32

def getTemperature():
    x=i2c.readfrom_mem(MCP9808_addr,5,2)
    a,b=ustruct.unpack('>BB',x)
    sign=0x10
    a&=0x0f 
    temp = (a*16+b/16)
    if sign:
        return temp;
    else:
        return -temp

#returns (TempF,RH)        
def getSHT():
  i2c.writeto(68,b'\x2c\x10')
  time.sleep_ms(100)
  x=i2c.readfrom(68,6)
  (a,aCRC,b,bCRC)=ustruct.unpack('>HBHB',x)
  RH= 100* b/(2**16-1)
  Tf= -49+315*a/(2**16-1)
  return (Tf,RH)

        
import urequests
import ujson
import uio

AIOKey ="noKey"
userName="noUsername"


  
baseURL='https://io.adafruit.com/api/v2/'

def sendValToFeed(user,feedName,value):
    h= {}
    h['X-AIO-Key']=AIOKey
    h['Content-Type']='application/json'
    v={}
    v['value']=value
    path = "{0}/feeds/{1}/data".format(user,feedName)
    full = baseURL+path
    print (full)
    return urequests.post(full,headers=h,data=ujson.dumps(v))

def getLastVal(user,feedName):
    h= {}
    h['X-AIO-Key']=AIOKey
    path = "{0}/feeds/{1}/data/last".format(user,feedName)
    full = baseURL+path
    print (full)
    return urequests.get(full,headers=h)


def main():
  global AIOKey,userName
  try:
    with uio.open('aio.key',mode='r') as f:
      key = ujson.loads(f.readline())
      AIOKey=key['AIOkey']
      userName = key['userName']
  except:
    print("Couldent get credentials!!")
    return


  #get temp from the MCP9808 sensor
  TC=getTemperature()
  sendValToFeed(userName,'foo',TC)
  
  #get temp/humidty ffrom the SHT31 sensor
  TF,RH=getSHT()
  sendValToFeed(userName,'bassementtempf',TF)
  sendValToFeed(userName,'basementrh',RH)

  # should we goto sleep? 
  ctrl = getLastVal(userName,'ctrl')
  print(ctrl.json())
  if (ctrl.json()['value']=='ON'):
    import machine
    rtc=machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    #if so for how long?
    t = int(getLastVal(userName,'updatetime').json()['value'])
    rtc.alarm(rtc.ALARM0,t*60*1000) #
    machine.deepsleep()





