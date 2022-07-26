import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class PressurePrograme():
# Create the I2C bus
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
        self.ads = ADS.ADS1015(self.i2c)
        self.ads.gain = 1

# Create single-ended input on channel 0
        self.chan = AnalogIn(self.ads, ADS.P0)
        
# print("{:>5}\t{:>5}".format('raw', 'v'))

    def pressure_return(self) :
    #print(chan.value)
    #time.sleep(0.5)
    #print(chan.voltage)
    #time.sleep(0.5)
        ADCVoltage= ((self.chan.value)*(3294/26352))

        current= (ADCVoltage-0)*((20-4)/(3294-0))+4

#     print(chan.value)
#     time.sleep(0.5)
        pressure= ((current-4)*(10-0)/(20-4))+0
    #print(ADCVoltage)
#     
#     time.sleep(0.5)
#     print(current)
#     time.sleep(0.5)
    
        time.sleep(0.5)
        return pressure
    #print("{:>5}\t{:>5.5f}".format(chan.value, chan.voltage))
    #time.sleep(0.5)