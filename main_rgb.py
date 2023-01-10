import time
import uos
from machine import I2C, Pin, ADC, PWM
from time import sleep
#from pico_i2c_lcd import I2cLcd
#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

#pump functions
motor1a = Pin(14, Pin.OUT)
motor1b = Pin(15, Pin.OUT)
#conditional pin for moisture sensor
moist_sensor = Pin(28, Pin.OUT)

# LEDS (defining through PWM)

pwm_RED = PWM(Pin(7))
pwm_GREEN = PWM(Pin(5))
pwm_BLUE = PWM(Pin(6))
pwm_RED.freq(1000)
pwm_GREEN.freq(1000)
pwm_BLUE.freq(1000)

pwm_BLUE.duty_u16(0)
pwm_RED.duty_u16(0)
pwm_GREEN.duty_u16(0)


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

        
#print(i2c.scan())
#I2C_ADDR = i2c.scan()[0]
#lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
#watered=0


value = read_sensor()
scaled = ((value-20500)/3000)
moisture = int(15-scaled)
# initial screen:


#lcd.putstr("Moisture lvl: " + str(moisture) + "\nNever watered")
dry_counter=0

while True:
    value = read_sensor()
    scaled = ((value-20500)/3000)
    moisture = int(15-scaled)
    
    pwm_BLUE.duty_u16(0)
    pwm_RED.duty_u16(0)
    pwm_GREEN.duty_u16(0)

    
    # conditional launch of the pump
    if moisture <= 6 and dry_counter <= 1:
        print('Moisture: ' + str(moisture) +' dry counter: ' + str(dry_counter)+ ' First Watering')
        dry_counter+=1
        pwm_BLUE.duty_u16(500)
        forward()
        sleep(5)
        stop()
        pass
    elif moisture <= 6 and dry_counter > 1:
        print('Moisture: ' + str(moisture) +' dry counter: ' + str(dry_counter) + ' Too dry for too long')
        dry_counter=dry_counter + 1
        pwm_RED.duty_u16(1525)
        forward()
        sleep(5)
        stop()
    elif moisture >=7 and moisture <= 10:
        print('Moisture: ' + str(moisture) +' dry counter: ' + str(dry_counter) + ' No need to water')
        pwm_RED.duty_u16(625)
        pwm_GREEN.duty_u16(525)
        dry_counter = 0
    elif moisture > 10:
        print('Moisture: ' + str(moisture) +' dry counter: ' + str(dry_counter) + ' No need to water')
        dry_counter = 0
        pwm_GREEN.duty_u16(500)
    
    sleep(3600)
  


        


