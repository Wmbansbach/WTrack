from sense_hat import SenseHat
import time

class Sensor:

    def __init__(self) -> None:
           self.sense = SenseHat()

    def HatInitialize(self):
        r = (255, 0, 0)     # red
        o = (255, 128, 0)   # orange
        y = (255, 255, 0)   # yellow
        g = (0, 255, 0)     # green
        c = (0, 255, 255)   # cyan
        b = (0, 0, 255)     # blue
        p = (255, 0, 255)   # purple
        n = (255, 128, 128) # pink
        w =(255, 255, 255)  # white
        k = (0, 0, 0)       # blank

        rainbow = [r, o, y, g, c, b, p, n]

        self.sense.clear()

        for y in range(8):
            colour = rainbow[y]
            for x in range(8):
                self.sense.set_pixel(x, y, colour)
        
        time.sleep(.5)

        self.sense.clear()


    def GetLocalEnvData(self):
        temp_data = []
        humid_data = []
        pres_data = []
        temp_master = any
        humid_master = any
        pres_master = any

        for t in range(5):
            temp_data = temp_data.append(format(self.sense.get_temperature(), '0.3f'))
            humid_data = humid_data.append(self.sense.get_humidity())
            pres_data = pres_data.append(self.sense.get_pressure())
            time.sleep(1)

        for i in range(5):
            temp_master += temp_data[i]
            humid_master = humid_data[i]
            pres_master = pres_data[i]
        
        return temp_master / 5, humid_master / 5, pres_master / 5
