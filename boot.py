# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
import webrepl
import machine
import time
from machine import Pin
webrepl.start()
gc.collect()

def blink(times,delay):
  p=Pin(2,Pin.OUT)
  p.value(1)
  for i in range(times):
    p.value(0)
    time.sleep_ms(delay)
    p.value(1)
    time.sleep_ms(delay)

# configure RTC.ALARM0 to be able to wake the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    blink(10,100)
else:
    blink(2,250)



