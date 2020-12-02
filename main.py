from sense_hat import SenseHat
from time import sleep
from picamera import PiCamera
import os
import ephem
import datetime

start_time = datetime.datetime.now()
now_time = datetime.datetime.now()
duration = datetime.timedelta(seconds=5)
sense = SenseHat()
sense.clear()

with open ("magnetic_measurements.csv", "w") as file:
        file.write("MagX , MagY , MagZ \n")

is_day = False

def where_iss():
    name = "ISS (ZARYA)"
    
    line1 = "1 25544U 98067A   20309.20855620  .00002422  00000-0  51431-4 0  9990"
    line2 = "2 25544  51.6472  15.6247 0001884  85.9288  10.5094 15.49382450253722"
    
    iss = ephem.readtle(name, line1, line2)
    iss.compute()
    
    iss_sublat = iss.sublat
    iss_sublong = iss.sublong
    iss_pos = "latitude: " + str(iss.sublat) + " longitude: " + str(iss_sublong)
    print(iss_pos)
    
    return(iss_pos)
    
def night_or_day():
    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   20310.24235862  .00002240  00000-0  48175-4 0  9995"
    line2 = "2 25544  51.6464  10.5089 0001916  86.8260  19.7416 15.49387201253882"

    iss = ephem.readtle(name, line1, line2)
    iss.compute()

    sun = ephem.Sun()
    sun.compute()

    #Angle calculated by translating to radians with repr
    #Angle between sun and iss from equator
    angle = float(repr(iss.ra))-float(repr(sun.ra))
    max_angle = float(1.57)
    min_angle = float(-1.57)
    
    if min_angle < angle < max_angle:
        print('It is day. Angle between the Sun and the ISS is {:1.6f} radians.'.format(angle))
        return True
    else:
        print('It is night. Angle between the Sun and the ISS is {:1.6f} radians.'.format(angle))
        return False

def take_picture():
    if is_day == True:
        with PiCamera() as camera:
            camera.capture('/home/pi/Desktop/SuRvEyOrS/pics/' + str(where_iss()) + '.jpg')
            print('picture taken')

def magnetic_field():
    compass = sense.get_compass_raw()
    x = float(compass['x'])
    y = float(compass['y'])
    z = float(compass['z'])
    
    with open ("magnetic_measurements.csv", "a") as file:
        file.write("%s, %s, %s  \n" % (x,y,z))
  
    print('magnetic taken')

while True: 
    is_day = night_or_day()
    magnetic_field()
    now_time = datetime.datetime.now()
    
    if now_time > start_time + duration:
        take_picture()
        start_time = now_time
    sleep(1)


