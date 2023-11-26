import time
import uos
from machine import I2C, Pin, ADC, PWM
from time import sleep
from neopixel import Neopixel
#from pico_i2c_lcd import I2cLcd
#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
numpix = 5 
strip = Neopixel(numpix, 0, 28, "RGBW")
#color = strip.colorHSV(255, 255, 255, 255)
#pump functions
motor1a = Pin(14, Pin.OUT)
#conditional pin for moisture sensor
soil = ADC(Pin(26))  # Soil moisture PIN reference

#Calibraton values
min_moisture=37008
max_moisture=26158


def forward():
    motor1a.high()
   
def stop():
    motor1a.low()       

dry_counter=0
while True: 
    moist_list = []
    for i in range(3):
        moist_list.append(soil.read_u16())
        sleep(0.1)
    mean_moist = sum(moist_list)/len(moist_list)
    moisture = (min_moisture-mean_moist)*100/(min_moisture-max_moisture) 
    # print values
    print("moisture: " + "%.2f" % moisture +"% (adc: "+str(soil.read_u16())+")")

    
    # conditional launch of the pump
    if moisture <= 30 and dry_counter < 1:
        print('Moisture: ' + str(round(moisture)) +' dry counter: ' + str(dry_counter)+ ' First Watering')
        dry_counter+=1
        strip.fill((0, 0, 0, 0))
        strip.show()
        strip.fill((0, 1, 1, 0))
        strip.show()
        forward()
        sleep(5)
        stop()
        pass
    elif moisture <= 10 and dry_counter >= 1:
        print('Moisture: ' + str(round(moisture)) +' dry counter: ' + str(dry_counter) + ' Too dry , watering needed')
        dry_counter=dry_counter + 1
        strip.fill((0, 0, 0, 0))
        strip.show()
        strip = Neopixel(1, 0, 28, "RGBW")
        strip.fill((0, 1, 0, 0))
        strip.show()
        forward()
        sleep(5)
        stop()
    elif 10 < moisture <= 20 and dry_counter >= 1:
        print('Moisture: ' + str(round(moisture)) +' dry counter: ' + str(dry_counter) + ' Dry, watering')
        dry_counter=dry_counter + 1
        strip.fill((0, 0, 0, 0))
        strip.show()
        strip = Neopixel(2, 0, 28, "RGBW")
        strip.fill((1, 5, 0, 0))
        strip.show()
        forward()
        sleep(5)
        stop()
    elif 20 < moisture <= 30 and dry_counter >= 1:
        print('Moisture: ' + str(round(moisture)) +' dry counter: ' + str(dry_counter) + ' Dry a bit, we will water')
        dry_counter=dry_counter + 1
        strip.fill((0, 0, 0, 0))
        strip.show()
        strip = Neopixel(3, 0, 28, "RGBW")
        strip.fill((1, 1, 0, 0))
        strip.show()
        forward()
        sleep(5)
        stop()
    elif 30 < moisture <= 40 and dry_counter >= 1:
        print('Moisture: ' + str(round(moisture)) +' dry counter: ' + str(dry_counter) + ' No need to water')
        dry_counter=dry_counter + 1
        strip.fill((0, 0, 0, 0))
        strip.show()
        strip = Neopixel(4, 0, 28, "RGBW")
        strip.fill((1, 0, 0, 0))
        strip.show()
        sleep(5)
    else:
        print('Moisture: ' + str(round(moisture)) +' dry counter: ' + str(dry_counter) + 'It is dump out here, no need to water')
        dry_counter=dry_counter + 1
        strip.fill((0, 0, 0, 0))
        strip.show()
        strip = Neopixel(5, 0, 28, "RGBW")
        strip.fill((1, 0, 1, 0))
        strip.show()
        sleep(5)
    
    sleep(10)
  




