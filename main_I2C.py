import time
import uos
from machine import I2C, Pin, ADC
from time import sleep
from pico_i2c_lcd import I2cLcd
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

#pump functions
motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)
#conditional pin for moisture sensor
moist_sensor = Pin(28, Pin.OUT)

def forward():
   motor1a.high()
   motor1b.low()
   
def stop():
   motor1a.low()
   motor1b.low()

# sensor functions
def read_sensor():
    moist_sensor.high()
    time.sleep(1)
    adc = ADC(Pin(26))
    sensor = adc.read_u16()
    moist_sensor.low()
    return sensor

print(i2c.scan())
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
watered=0


value = read_sensor()
scaled = ((value-20500)/3000)
moisture = int(15-scaled)
# initial screen:
#lcd.backlight_on()
print("Moisture lvl: " + str(moisture) + "\nNever watered")
lcd.putstr("Moisture lvl: " + str(moisture) + "\nNever watered")
        
while True:
    value = read_sensor()
    scaled = ((value-20500)/3000)
    moisture = int(15-scaled)
    
    # conditional launch of the pump
    if moisture <= 7:
        watered = time.time()
        forward()
        sleep(5)
        stop()
        
    if watered == 0:
        lcd.clear()
        print("Moisture lvl: " + str(moisture) + "\nNever watered")
        lcd.putstr("Moisture lvl: " + str(moisture) + "\nNever watered")
    else:
        lcd.clear()
        watered_ago=(time.time() - watered)/3600
        #print("Moisture lvl: " + str(moisture) + "\nWatered " + str(int(watered_ago) + "h ago")
        lcd.putstr("Moisture lvl: " + str(moisture) + "\nWater. " + str(round(float(watered_ago), 2)) + "h ago")
    
    sleep(1800)
    #lcd.backlight_off()    
    lcd.clear()

        


