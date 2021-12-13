#updated 11/2/2021 9:58pm -Micah Le
#updated 11/3/2021 6:30pm -Jared
#updated 11/3/2021 11:00pm -Jared and Micah
#updated 11/4/2021 8:31pm -Micah
#updated 11/13/2021 7:30PM-
#updated 11/13 8:15pm - new state machines for loaded and unloaded cart
#   rewrote collision avoidance function to stop motors within function
#   and to just be called

import read_PWM_functions
import time
import sys
import pigpio


def checkstate(sensor, sensor2, sensor3):
   # test file to take RGB values from sensors and print statments based on the values read

    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    #read and assign values from the sensors
        #sensor one values
    close_state1 = 0
    close_state2 = 0
    close_state3 = 0

    r1, g1, b1, clear1 = sensor.color_raw
    red1 = int(pow((int((r1 / clear1) * 256) / 255), 2.5) * 255)
    green1 = int((pow((int((g1 / clear1) * 256) / 255), 2.5) * 255)*1.36)
    blue1 = int((pow((int((b1 / clear1) * 256) / 255), 2.5) * 255)*1.56)

        #sensor two values
    r2, g2, b2, clear2 = sensor2.color_raw
    red2 = int(pow((int((r2 / clear2) * 256) / 255), 2.5) * 255)
    green2 = int((pow((int((g2 / clear2) * 256) / 255), 2.5) * 255)*1.36)
    blue2 = int((pow((int((b2 / clear2) * 256) / 255), 2.5) * 255)*1.56)

        #sensor three values
    r3, g3, b3, clear3 = sensor3.color_raw
    red3 = int(pow((int((r3 / clear3) * 256) / 255), 2.5) * 255)
    green3 = int((pow((int((g3 / clear3) * 256) / 255), 2.5) * 255)*1.36)
    blue3 = int((pow((int((b3 / clear3) * 256) / 255), 2.5) * 255)*1.56)

    #color_rgb = sensor.color_rgb_bytes
    #color_rgb2 = sensor2.color_rgb_bytes
    #color_rgb3 = sensor3.color_rgb_bytes

    #read the RGB and print values for sensor one
    #print("Sensor one is reading ")
    #print(color_rgb)
    #("/n")

    #check which RGB values are the greatest and set variables =1 to those that are the greatest
        #sensor one readings
    if ((red1 > green1) and (red1 > blue1)):
        redstate1 = 1
        bluestate1 = 0
        greenstate1 = 0
        if (red1 >= 70):
            curr_sensor1 = 1
        else:
            curr_sensor1 = 0
        #print("red is the greatest value read on sensor one")
    elif(((green1 > red1) and (green1 > blue1))):
        redstate1 = 0
        bluestate1 = 0
        greenstate1 = 1
        curr_sensor1 = 0
        if green1 >= 37:
            close_state1 = 1
        else:
            close_state1 = 0
        #print("green is the greatest value read on sensor one")
    elif(((blue1 > red1) and (blue1 > green1))):
        redstate1 = 0
        bluestate1 = 1
        greenstate1 = 0
        curr_sensor1 = 0
        #print("blue is the greatest value read on sensor one")
    elif(((blue1 == red1) and (blue1 > green1))):
        redstate1 = 1
        bluestate1 = 1
        greenstate1 = 0
        curr_sensor1 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue1 == green1) and (blue1 > red1))):
        redstate1 = 0
        bluestate1 = 1
        greenstate1 = 1
        curr_sensor1 = 0
        #print("blue and green values are the same and greater than red")
    elif(((red1 == green1) and (red1 > blue1))):
        redstate1 = 1
        bluestate1 = 0
        greenstate1 = 1
        curr_sensor1 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue1 == green1) and (blue1 == red1))):
        redstate1 = 1
        bluestate1 = 1
        greenstate1 =1
        curr_sensor1 = 0
        #print("red green and blue values are equal")
    else:
        redstate1 = 0
        bluestate1 = 0
        greenstate1 = 0
        curr_sensor1 = 0
        #print("i have no idea what values are being read")

    #("/n")

    #read the RGB and print values for sensor two
    #print("Sensor two is reading ")
    #print(color_rgb2)
    #("/n")

        #sensor two readings
    if ((red2 > green2) and (red2 > blue2)):
        redstate2 = 1
        bluestate2 = 0
        greenstate2 = 0
        if (red2 >= 70):
            curr_sensor2 = 1
        else:
            curr_sensor2 = 0
        #print("red is the greatest value read on sensor two")
    elif(((green2 > red2) and (green2 > blue2))):
        redstate2 = 0
        bluestate2 = 0
        greenstate2 = 1           
        curr_sensor2 = 0
        if green2 >= 37:
            close_state2 = 1
        else:
            close_state2 = 0
        #print("green is the greatest value read on sensor two")
    elif(((blue2 > red2) and (blue2 > green2))):
        redstate2 = 0
        bluestate2 = 1
        greenstate2 = 0
        curr_sensor2 = 0
        #print("blue is the greatest value read on sensor two")
    elif(((blue2 == red2) and (blue2 > green2))):
        redstate2 = 1
        bluestate2 = 1
        greenstate2 = 0
        curr_sensor2 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue2 == green2) and (blue2 > red2))):
        redstate2 = 0
        bluestate2 = 1
        greenstate2 = 1
        curr_sensor2 = 0
        #print("blue and green values are the same and greater than red")
    elif(((red2 == green2) and (red2 > blue2))):
        redstate2 = 1
        bluestate2 = 0
        greenstate2 = 1
        curr_sensor2 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue2 == green2) and (blue2 == red2))):
        redstate2 = 1
        bluestate2 = 1
        greenstate2 =1
        curr_sensor2 = 0
        #print("red green and blue values are equal")
    else:
        redstate2 = 0
        bluestate2 = 0
        greenstate2 = 0
        curr_sensor2 = 0
        #print("i have no idea what values are being read")

    #read the RGB and print values for sensor three
    #print("Sensor three is reading ")
    #print(color_rgb3)
    #("/n")

        #sensor three readings
    if ((red3 > green3) and (red3 > blue3)):
        redstate3 = 1
        bluestate3 = 0
        greenstate3 = 0
        if (red3 >= 70):
            curr_sensor3 = 1
        else:
            curr_sensor3 = 0
        #print("red is the greatest value read on sensor three")
    elif(((green3 > red3) and (green3 > blue3))):
        redstate3 = 0
        bluestate3 = 0
        greenstate3 = 1
        curr_sensor3 = 0
        if green3 >= 37:
            close_state3 = 1
        else:
            close_state3 = 0
        #print("green is the greatest value read on sensor three")
    elif(((blue3 > red3) and (blue3 > green3))):
        redstate3 = 0
        bluestate3 = 1
        greenstate3 = 0
        curr_sensor3 = 0
        #print("blue is the greatest value read on sensor three")
    elif(((blue3 == red3) and (blue3 > green3))):
        redstate3 = 1
        bluestate3 = 1
        greenstate3 = 0
        curr_sensor3 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue3 == green3) and (blue3 > red3))):
        redstate3 = 0
        bluestate3 = 1
        greenstate3 = 1
        curr_sensor3 = 0
       #print("blue and green values are the same and greater than red")
    elif(((red3 == green3) and (red3 > blue3))):
        redstate3 = 1
        bluestate3 = 0
        greenstate3 = 1
        curr_sensor3 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue3 == green3) and (blue3 == red3))):
        redstate3 = 1
        bluestate3 = 1
        greenstate3 =1
        curr_sensor3 = 0
        #print("red green and blue values are equal")
    else:
        redstate3 = 0
        bluestate3 = 0
        greenstate3 = 0
        curr_sensor3 = 0
        #print("i have no idea what values are being read")
    #("/n")
    print("printing sensor binary state values")
    print(curr_sensor1, curr_sensor2, curr_sensor3)
    

    #time.sleep(5.0)

    return(curr_sensor1, curr_sensor2, curr_sensor3, close_state1, close_state2, close_state3) #this manages the left IR sensor inputs

def checkstate2(sensor, sensor2, sensor3, counter, redcounter):
    close_state1 = 0
    close_state2 = 0
    close_state3 = 0

   # test file to take RGB values from sensors and print statments based on the values read

    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    #read and assign values from the sensors
        #sensor one values
    r1, g1, b1, clear1 = sensor.color_raw
    red1 = int(pow((int((r1 / clear1) * 256) / 255), 2.5) * 255)
    green1 = int((pow((int((g1 / clear1) * 256) / 255), 2.5) * 255)*1.36)
    blue1 = int((pow((int((b1 / clear1) * 256) / 255), 2.5) * 255)*1.56)

        #sensor two values
    r2, g2, b2, clear2 = sensor2.color_raw
    red2 = int(pow((int((r2 / clear2) * 256) / 255), 2.5) * 255)
    green2 = int((pow((int((g2 / clear2) * 256) / 255), 2.5) * 255)*1.36)
    blue2 = int((pow((int((b2 / clear2) * 256) / 255), 2.5) * 255)*1.56)

        #sensor three values
    r3, g3, b3, clear3 = sensor3.color_raw
    red3 = int(pow((int((r3 / clear3) * 256) / 255), 2.5) * 255)
    green3 = int((pow((int((g3 / clear3) * 256) / 255), 2.5) * 255)*1.36)
    blue3 = int((pow((int((b3 / clear3) * 256) / 255), 2.5) * 255)*1.56)

    #color_rgb = sensor.color_rgb_bytes
    #color_rgb2 = sensor2.color_rgb_bytes
    #color_rgb3 = sensor3.color_rgb_bytes

    #read the RGB and print values for sensor one
    #print("Sensor one is reading ")
    #print(color_rgb)
    #("/n")

    #check which RGB values are the greatest and set variables =1 to those that are the greatest
        #sensor one readings
    if ((red1 > green1) and (red1 > blue1)): #red is the highest value
        redstate1 = 1
        bluestate1 = 0
        greenstate1 = 0
        if (red1 >= 70):
            curr_sensor1 = 1
        else:
            curr_sensor1 = 0
        #print("red is the greatest value read on sensor one")
    elif(((green1 > red1) and (green1 > blue1))): #green is the highest value
        redstate1 = 0
        bluestate1 = 0
        greenstate1 = 1
        curr_sensor1 = 0
        if green1 >= 37:
            close_state1 = 1
        else:
            close_state1 = 0
        #print("green is the greatest value read on sensor one")
    elif(((blue1 > red1) and (blue1 > green1))): #blue is the highest value
        redstate1 = 0
        bluestate1 = 1
        greenstate1 = 0
        curr_sensor1 = 0
        #print("blue is the greatest value read on sensor one")
    elif(((blue1 == red1) and (blue1 > green1))): #blue and red are equal, and both greater than green
        redstate1 = 1
        bluestate1 = 1
        greenstate1 = 0
        curr_sensor1 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue1 == green1) and (blue1 > red1))): #blue and green are equal, and both are greater than red
        redstate1 = 0
        bluestate1 = 1
        greenstate1 = 1
        curr_sensor1 = 0
        #print("blue and green values are the same and greater than red")
    elif(((red1 == green1) and (red1 > blue1))): #red and green are equal, and both are greater than blue
        redstate1 = 1
        bluestate1 = 0
        greenstate1 = 1
        curr_sensor1 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue1 == green1) and (blue1 == red1))): #all values are equal
        redstate1 = 1
        bluestate1 = 1
        greenstate1 =1
        curr_sensor1 = 0
        #print("red green and blue values are equal")
    else: #no values are being read.
        redstate1 = 0
        bluestate1 = 0
        greenstate1 = 0
        curr_sensor1 = 0
        #print("i have no idea what values are being read")

    #("/n")

    #read the RGB and print values for sensor two
    #print("Sensor two is reading ")
    #print(color_rgb2)
    #("/n")

        #sensor two readings
    if ((red2 > green2) and (red2 > blue2)):
        redstate2 = 1
        bluestate2 = 0
        greenstate2 = 0
        if (red2 >= 70):
            curr_sensor2 = 1
        else:
            curr_sensor2 = 0
        #print("red is the greatest value read on sensor two")
    elif(((green2 > red2) and (green2 > blue2))):
        redstate2 = 0
        bluestate2 = 0
        greenstate2 = 1
        curr_sensor2 = 0
        if green2 >= 37:
            close_state2 = 1
        else:
            close_state2 = 0
        #print("green is the greatest value read on sensor two")
    elif(((blue2 > red2) and (blue2 > green2))):
        redstate2 = 0
        bluestate2 = 1
        greenstate2 = 0
        curr_sensor2 = 0
        #print("blue is the greatest value read on sensor two")
    elif(((blue2 == red2) and (blue2 > green2))):
        redstate2 = 1
        bluestate2 = 1
        greenstate2 = 0
        curr_sensor2 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue2 == green2) and (blue2 > red2))):
        redstate2 = 0
        bluestate2 = 1
        greenstate2 = 1
        curr_sensor2 = 0
        #print("blue and green values are the same and greater than red")
    elif(((red2 == green2) and (red2 > blue2))):
        redstate2 = 1
        bluestate2 = 0
        greenstate2 = 1
        curr_sensor2 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue2 == green2) and (blue2 == red2))):
        redstate2 = 1
        bluestate2 = 1
        greenstate2 =1
        curr_sensor2 = 0
        #print("red green and blue values are equal")
    else:
        redstate2 = 0
        bluestate2 = 0
        greenstate2 = 0
        curr_sensor2 = 0
        #print("i have no idea what values are being read")

    #read the RGB and print values for sensor three
    #print("Sensor three is reading ")
    #print(color_rgb3)
    #("/n")

        #sensor three readings
    if ((red3 > green3) and (red3 > blue3)):
        redstate3 = 1
        bluestate3 = 0
        greenstate3 = 0
        if (red3 >= 70):
            curr_sensor3 = 1
        else:
            curr_sensor3 = 0
        #print("red is the greatest value read on sensor three")
    elif(((green3 > red3) and (green3 > blue3))):
        redstate3 = 0
        bluestate3 = 0
        greenstate3 = 1
        curr_sensor3 = 0
        if green3 >= 37:
            close_state3 = 1
        else:
            close_state3 = 0
        #print("green is the greatest value read on sensor three")
    elif(((blue3 > red3) and (blue3 > green3))):
        redstate3 = 0
        bluestate3 = 1
        greenstate3 = 0
        curr_sensor3 = 0
        #print("blue is the greatest value read on sensor three")
    elif(((blue3 == red3) and (blue3 > green3))):
        redstate3 = 1
        bluestate3 = 1
        greenstate3 = 0
        curr_sensor3 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue3 == green3) and (blue3 > red3))):
        redstate3 = 0
        bluestate3 = 1
        greenstate3 = 1
        curr_sensor3 = 0
       #print("blue and green values are the same and greater than red")
    elif(((red3 == green3) and (red3 > blue3))):
        redstate3 = 1
        bluestate3 = 0
        greenstate3 = 1
        curr_sensor3 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue3 == green3) and (blue3 == red3))):
        redstate3 = 1
        bluestate3 = 1
        greenstate3 =1
        curr_sensor3 = 0
        #print("red green and blue values are equal")
    else:
        redstate3 = 0
        bluestate3 = 0
        greenstate3 = 0
        curr_sensor3 = 0
        #print("i have no idea what values are being read")
    #("/n")
    print("printing sensor binary state values")
    print(curr_sensor1, curr_sensor2, curr_sensor3)

    if(redcounter == 0):
        if(close_state1 == 1 and close_state2 == 1 and close_state3 ==1):
            counter -= 1
            redcounter +=1
            #print("counter value = ", counter)
        elif(close_state1 & close_state2 == 1) or (close_state1 & close_state3 == 1) or (close_state2 & close_state3 == 1):
            counter -=1
            redcounter +=1
            #print("counter value = ", counter)
        #else:
            #print("counter value = ", counter)
    else:
        if(curr_sensor1 or curr_sensor2 or curr_sensor3 == 1):
            redcounter -= 1

    # if close_state1 == 1:
    #     print(close_state1)
    # elif close_state2 == 1:
    #     print(close_state2)
    # elif close_state3 == 1:
    #     print(close_state3)

    return(curr_sensor1, curr_sensor2, curr_sensor3, counter, redcounter) #this manages the right IR sensor inputs

def checkstate3(sensor, sensor2, sensor3):
   # test file to take RGB values from sensors and print statments based on the values read

    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    #read and assign values from the sensors
        #sensor one values
    close_state1 = 0
    close_state2 = 0
    close_state3 = 0

    r1, g1, b1, clear1 = sensor.color_raw
    red1 = int(pow((int((r1 / clear1) * 256) / 255), 2.5) * 255)
    green1 = int(pow((int((g1 / clear1) * 256) / 255), 2.5) * 255)
    blue1 = int(pow((int((b1 / clear1) * 256) / 255), 2.5) * 255)

        #sensor two values
    r2, g2, b2, clear2 = sensor2.color_raw
    red2 = int(pow((int((r2 / clear2) * 256) / 255), 2.5) * 255)
    green2 = int(pow((int((g2 / clear2) * 256) / 255), 2.5) * 255)
    blue2 = int(pow((int((b2 / clear2) * 256) / 255), 2.5) * 255)

        #sensor three values
    r3, g3, b3, clear3 = sensor3.color_raw
    red3 = int(pow((int((r3 / clear3) * 256) / 255), 2.5) * 255)
    green3 = int(pow((int((g3 / clear3) * 256) / 255), 2.5) * 255)
    blue3 = int(pow((int((b3 / clear3) * 256) / 255), 2.5) * 255)

    #color_rgb = sensor.color_rgb_bytes
    #color_rgb2 = sensor2.color_rgb_bytes
    #color_rgb3 = sensor3.color_rgb_bytes

    #read the RGB and print values for sensor one
    #print("Sensor one is reading ")
    #print(color_rgb)
    #("/n")

    #check which RGB values are the greatest and set variables =1 to those that are the greatest
        #sensor one readings
    if ((red1 > green1) and (red1 > blue1)):
        redstate1 = 1
        bluestate1 = 0
        greenstate1 = 0
        curr_sensor1 = 0
        #print("red is the greatest value read on sensor one")
    elif(((green1 > red1) and (green1 > blue1))):
        redstate1 = 0
        bluestate1 = 0
        greenstate1 = 1
        curr_sensor1 = 0
        close_state1 = 1
        #print("green is the greatest value read on sensor one")
    elif(((blue1 > red1) and (blue1 > green1))):
        redstate1 = 0
        bluestate1 = 1
        greenstate1 = 0
        if (blue1 >= 25):
            curr_sensor1 = 1
        else:
            curr_sensor1 = 0
        #print("blue is the greatest value read on sensor one")
    elif(((blue1 == red1) and (blue1 > green1))):
        redstate1 = 1
        bluestate1 = 1
        greenstate1 = 0
        curr_sensor1 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue1 == green1) and (blue1 > red1))):
        redstate1 = 0
        bluestate1 = 1
        greenstate1 = 1
        curr_sensor1 = 0
        #print("blue and green values are the same and greater than red")
    elif(((red1 == green1) and (red1 > blue1))):
        redstate1 = 1
        bluestate1 = 0
        greenstate1 = 1
        curr_sensor1 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue1 == green1) and (blue1 == red1))):
        redstate1 = 1
        bluestate1 = 1
        greenstate1 =1
        curr_sensor1 = 0
        #print("red green and blue values are equal")
    else:
        redstate1 = 0
        bluestate1 = 0
        greenstate1 = 0
        curr_sensor1 = 0
        #print("i have no idea what values are being read")

    ("/n")

    #read the RGB and print values for sensor two
    #print("Sensor two is reading ")
    #print(color_rgb2)
    #("/n")

        #sensor two readings
    if ((red2 > green2) and (red2 > blue2)):
        redstate2 = 1
        bluestate2 = 0
        greenstate2 = 0
        curr_sensor2 = 0
        #print("red is the greatest value read on sensor two")
    elif(((green2 > red2) and (green2 > blue2))):
        redstate2 = 0
        bluestate2 = 0
        greenstate2 = 1
        curr_sensor2 = 0
        close_state2 = 1
        #print("green is the greatest value read on sensor two")
    elif(((blue2 > red2) and (blue2 > green2))):
        redstate2 = 0
        bluestate2 = 1
        greenstate2 = 0
        if (blue2 >= 25):
            curr_sensor2 = 1
        else:
            curr_sensor2 = 0
        #print("blue is the greatest value read on sensor two")
    elif(((blue2 == red2) and (blue2 > green2))):
        redstate2 = 1
        bluestate2 = 1
        greenstate2 = 0
        curr_sensor2 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue2 == green2) and (blue2 > red2))):
        redstate2 = 0
        bluestate2 = 1
        greenstate2 = 1
        curr_sensor2 = 0
        #print("blue and green values are the same and greater than red")
    elif(((red2 == green2) and (red2 > blue2))):
        redstate2 = 1
        bluestate2 = 0
        greenstate2 = 1
        curr_sensor2 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue2 == green2) and (blue2 == red2))):
        redstate2 = 1
        bluestate2 = 1
        greenstate2 =1
        curr_sensor2 = 0
        #print("red green and blue values are equal")
    else:
        redstate2 = 0
        bluestate2 = 0
        greenstate2 = 0
        curr_sensor2 = 0
        #print("i have no idea what values are being read")

    #read the RGB and print values for sensor three
    #print("Sensor three is reading ")
    #print(color_rgb3)
    #("/n")

        #sensor three readings
    if ((red3 > green3) and (red3 > blue3)):
        redstate3 = 1
        bluestate3 = 0
        greenstate3 = 0
        curr_sensor3 = 0
        #print("red is the greatest value read on sensor three")
    elif(((green3 > red3) and (green3 > blue3))):
        redstate3 = 0
        bluestate3 = 0
        greenstate3 = 1
        curr_sensor3 = 0
        close_state3 = 1
        #print("green is the greatest value read on sensor three")
    elif(((blue3 > red3) and (blue3 > green3))):
        redstate3 = 0
        bluestate3 = 1
        greenstate3 = 0
        if (blue3 >= 25):
            curr_sensor3 = 1
        else:
            curr_sensor3 = 0
        #print("blue is the greatest value read on sensor three")
    elif(((blue3 == red3) and (blue3 > green3))):
        redstate3 = 1
        bluestate3 = 1
        greenstate3 = 0
        curr_sensor3 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue3 == green3) and (blue3 > red3))):
        redstate3 = 0
        bluestate3 = 1
        greenstate3 = 1
        curr_sensor3 = 0
       #print("blue and green values are the same and greater than red")
    elif(((red3 == green3) and (red3 > blue3))):
        redstate3 = 1
        bluestate3 = 0
        greenstate3 = 1
        curr_sensor3 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue3 == green3) and (blue3 == red3))):
        redstate3 = 1
        bluestate3 = 1
        greenstate3 =1
        curr_sensor3 = 0
        #print("red green and blue values are equal")
    else:
        redstate3 = 0
        bluestate3 = 0
        greenstate3 = 0
        curr_sensor3 = 0
        #print("i have no idea what values are being read")
    ("/n")
    print("printing sensor binary state values")
    print(curr_sensor1, curr_sensor2, curr_sensor3)
    #time.sleep(5.0)
    print(blue1, blue2, blue3)
    return(curr_sensor1, curr_sensor2, curr_sensor3, close_state1, close_state2, close_state3) #this manages the middle IR sensor inputs



def checkstateBlue(sensor, sensor2, sensor3):
   # test file to take RGB values from sensors and print statments based on the values read

    # Raw data from the sensor in a 4-tuple of red, green, blue, clear light component values
    # print(sensor.color_raw)

    #read and assign values from the sensors
        #sensor one values
    close_state1 = 0
    close_state2 = 0
    close_state3 = 0

    r1, g1, b1, clear1 = sensor.color_raw
    red1 = int(pow((int((r1 / clear1) * 256) / 255), 2.5) * 255)
    green1 = int((pow((int((g1 / clear1) * 256) / 255), 2.5) * 255)*1.36)
    blue1 = int((pow((int((b1 / clear1) * 256) / 255), 2.5) * 255)*1.56)

        #sensor two values
    r2, g2, b2, clear2 = sensor2.color_raw
    red2 = int(pow((int((r2 / clear2) * 256) / 255), 2.5) * 255)
    green2 = int((pow((int((g2 / clear2) * 256) / 255), 2.5) * 255)*1.36)
    blue2 = int((pow((int((b2 / clear2) * 256) / 255), 2.5) * 255)*1.56)

        #sensor three values
    r3, g3, b3, clear3 = sensor3.color_raw
    red3 = int(pow((int((r3 / clear3) * 256) / 255), 2.5) * 255)
    green3 = int((pow((int((g3 / clear3) * 256) / 255), 2.5) * 255)*1.36)
    blue3 = int((pow((int((b3 / clear3) * 256) / 255), 2.5) * 255)*1.56)

    #color_rgb = sensor.color_rgb_bytes
    #color_rgb2 = sensor2.color_rgb_bytes
    #color_rgb3 = sensor3.color_rgb_bytes

    #read the RGB and print values for sensor one
    #print("Sensor one is reading ")
    #print(color_rgb)
    #("/n")

    #check which RGB values are the greatest and set variables =1 to those that are the greatest
        #sensor one readings
    if ((red1 > green1) and (red1 > blue1)):
        redstate1 = 1
        bluestate1 = 0
        greenstate1 = 0
        if (red1 >= 55):
            curr_sensor1 = 1
        else:
            curr_sensor1 = 0
        #print("red is the greatest value read on sensor one")
    elif(((green1 > red1) and (green1 > blue1))):
        redstate1 = 0
        bluestate1 = 0
        if green1 > 22:
            greenstate1 = 1
        else:
            greenstate = 0
        curr_sensor1 = 0
        #print("green is the greatest value read on sensor one")
    elif(((blue1 > red1) and (blue1 > green1))):
        redstate1 = 0
        bluestate1 = 1
        greenstate1 = 0
        curr_sensor1 = 0
        if blue1 >= 55:
            close_state1 = 1
        else:
            close_state1 = 0
        
        #print("blue is the greatest value read on sensor one")
    elif(((blue1 == red1) and (blue1 > green1))):
        redstate1 = 1
        bluestate1 = 1
        greenstate1 = 0
        curr_sensor1 = 0

        #print("blue and red values are the same and greater than green")
    elif(((blue1 == green1) and (blue1 > red1))):
        redstate1 = 0
        bluestate1 = 1
        greenstate1 = 1
        curr_sensor1 = 0

        #print("blue and green values are the same and greater than red")
    elif(((red1 == green1) and (red1 > blue1))):
        redstate1 = 1
        bluestate1 = 0
        greenstate1 = 1
        curr_sensor1 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue1 == green1) and (blue1 == red1))):
        redstate1 = 1
        bluestate1 = 1
        greenstate1 =1
        curr_sensor1 = 0
        if blue1 >= 55:
            close_state1 = 1
        else:
            close_state1 = 0
        

        #print("red green and blue values are equal")
    else:
        redstate1 = 0
        bluestate1 = 0
        greenstate1 = 0
        curr_sensor1 = 0
        #print("i have no idea what values are being read")

    #("/n")

    #read the RGB and print values for sensor two
    #print("Sensor two is reading ")
    #print(color_rgb2)
    #("/n")

        #sensor two readings
    if ((red2 > green2) and (red2 > blue2)):
        redstate2 = 1
        bluestate2 = 0
        greenstate2 = 0
        if (red2 >= 55):
            curr_sensor2 = 1
        else:
            curr_sensor2 = 0
        #print("red is the greatest value read on sensor two")
    elif(((green2 > red2) and (green2 > blue2))):
        redstate2 = 0
        bluestate2 = 0
        if green2 > 22:
            greenstate2 = 1
        else:
            greenstate2 = 0
        curr_sensor2 = 0
        #print("green is the greatest value read on sensor two")
    elif(((blue2 > red2) and (blue2 > green2))):
        redstate2 = 0
        bluestate2 = 1
        greenstate2 = 0
        curr_sensor2 = 0
        if blue2 >= 55:
            close_state2 = 1
        else:
            close_state2 = 0

        #print("blue is the greatest value read on sensor two")
    elif(((blue2 == red2) and (blue2 > green2))):
        redstate2 = 1
        bluestate2 = 1
        greenstate2 = 0
        curr_sensor2 = 0
        #print("blue and red values are the same and greater than green")
    elif(((blue2 == green2) and (blue2 > red2))):
        redstate2 = 0
        bluestate2 = 1
        greenstate2 = 1
        curr_sensor2 = 0
        #print("blue and green values are the same and greater than red")
    elif(((red2 == green2) and (red2 > blue2))):
        redstate2 = 1
        bluestate2 = 0
        greenstate2 = 1
        curr_sensor2 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue2 == green2) and (blue2 == red2))):
        redstate2 = 1
        bluestate2 = 1
        greenstate2 =1
        curr_sensor2 = 0
        #print("red green and blue values are equal")
    else:
        redstate2 = 0
        bluestate2 = 0
        greenstate2 = 0
        curr_sensor2 = 0
        #print("i have no idea what values are being read")

    #read the RGB and print values for sensor three
    #print("Sensor three is reading ")
    #print(color_rgb3)
    #("/n")

        #sensor three readings
    if ((red3 > green3) and (red3 > blue3)):
        redstate3 = 1
        bluestate3 = 0
        greenstate3 = 0
        if (red3 >= 55):
            curr_sensor3 = 1
        else:
            curr_sensor3 = 0
        #print("red is the greatest value read on sensor three")
    elif(((green3 > red3) and (green3 > blue3))):
        redstate3 = 0
        bluestate3 = 0
        if green3 > 22:
            greenstate3 = 1
        else:
            greenstate3 = 0
        curr_sensor3 = 0
        #print("green is the greatest value read on sensor three")
    elif(((blue3 > red3) and (blue3 > green3))):
        redstate3 = 0
        bluestate3 = 1
        greenstate3 = 0
        curr_sensor3 = 0
        if blue3 >= 55:
            close_state3 = 1
        else:
            close_state3 = 0

        #print("blue is the greatest value read on sensor three")
    elif(((blue3 == red3) and (blue3 > green3))):
        redstate3 = 1
        bluestate3 = 1
        greenstate3 = 0
        curr_sensor3 = 0
        
        #print("blue and red values are the same and greater than green")
    elif(((blue3 == green3) and (blue3 > red3))):
        redstate3 = 0
        bluestate3 = 1
        greenstate3 = 1
        curr_sensor3 = 0
        
       #print("blue and green values are the same and greater than red")
    elif(((red3 == green3) and (red3 > blue3))):
        redstate3 = 1
        bluestate3 = 0
        greenstate3 = 1
        curr_sensor3 = 0
        #print("red and green values are the same and greater than blue")
    elif(((blue3 == green3) and (blue3 == red3))):
        redstate3 = 1
        bluestate3 = 1
        greenstate3 =1
        curr_sensor3 = 0
        #print("red green and blue values are equal")
    else:
        redstate3 = 0
        bluestate3 = 0
        greenstate3 = 0
        curr_sensor3 = 0
        #print("i have no idea what values are being read")
    #("/n")
    print("printing sensor binary state values")
    print(curr_sensor1, curr_sensor2, curr_sensor3)
    

    #time.sleep(5.0)

    return(curr_sensor1, curr_sensor2, curr_sensor3, close_state1, close_state2, close_state3) #this manages the left IR sensor inputs


#new state machines to use - statemachine 1 for loaded cart pathfinding to customer, statemachine2 for no load


def statemachine(curr_sensor1, curr_sensor2, curr_sensor3, prev_sensor1, prev_sensor2, prev_sensor3): #this takes the sensor readings, and pathfinds

    if(curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 0):
    #if 000 do not update previous state with this value otherwise its REALLY lost
    #check previous state
        if((prev_sensor1 == 0 and prev_sensor2 == 0 and prev_sensor3 == 1) or (prev_sensor1 == 0 and prev_sensor2 == 1 and prev_sensor3 == 1)):
                #check if the value is 001 for a hard right
            if(prev_sensor1 == 0 and prev_sensor2 == 0 and prev_sensor3 == 1):
                #set pwm values for hard right turn
                # pwm.ChangeDutyCycle(52)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 55
                rightmotor = 49
                print('hard turn right lost /n')
                # return(52,52, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
            #values should be set to 011 so we should set pwm values for motors to slight right turn
                # pwm.ChangeDutyCycle(50)         #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 53.5
                rightmotor = 49
                print('slight turn right lost/n')
                # return(50,52, prev_sensor1, prev_sensor2, prev_sensor3)

        elif((prev_sensor1 == 1 and prev_sensor2 == 1 and prev_sensor3 == 0) or (prev_sensor1 == 1 and prev_sensor2 == 0 and prev_sensor3 == 0)):
            #check if the value is 100 for a hard left turn
            if(prev_sensor1 == 1 and prev_sensor2 == 0 and prev_sensor3 == 0):
                #set pwm values for hard left turn
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)    #right motor
                leftmotor = 51
                rightmotor = 45
                print('hardleft lost /n')
                # return(48,48, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
                #values should be 110 so we should set the pwm values for the motors to turn slightly right
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(50)    #right motor
                leftmotor = 51
                rightmotor = 46.5
                print('slightleft lost /n')
                # return(48,50, prev_sensor1, prev_sensor2, prev_sensor3)
        else:
            leftmotor = 55
            rightmotor = 45
            print('lost-lost?', prev_sensor1, prev_sensor2, prev_sensor3)
    elif(curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 1 or curr_sensor1 == 1 and curr_sensor2 == 1 and curr_sensor3 == 1):
        leftmotor = 55
        rightmotor = 45
        print('temp foward state')
    else:
        prev_sensor1 = curr_sensor1
        prev_sensor2 = curr_sensor2
        prev_sensor3 = curr_sensor3
         #check if the sensor values are either 001 or 011 for either slight or hard left
        if((curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 1) or (curr_sensor1 == 0 and curr_sensor2 == 1 and curr_sensor3 == 1)):
            #check if the value is 001 for a hard right
            if(curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 1):
                #set pwm values for hard right turn
                # pwm.ChangeDutyCycle(52)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 55
                rightmotor = 47
                print('hardright \n')
                # return(52,52, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
                #values should be set to 011 so we should set pwm values for motors to slight right turn
                # pwm.ChangeDutyCycle(50)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 54
                rightmotor = 47
                print('slightright \n')
                # return(50,52, prev_sensor1, prev_sensor2, prev_sensor3)

        elif((curr_sensor1 == 1 and curr_sensor2 == 1 and curr_sensor3 == 0) or (curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 0)):
            #check if the value is 100 for a hard left turn

            if(curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 0):
                #set pwm values for hard left turn
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)               #right motor
                leftmotor = 53
                rightmotor = 44
                print('hardleft \n')
                # return(48,48, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
            #values should be 110 so we should set the pwm values for the motors to turn slightly left
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)               #right motor
                leftmotor = 53
                rightmotor = 45
                print('slightleft \n')
                # return(48,50, prev_sensor1, prev_sensor2, prev_sensor3)

        elif(curr_sensor1 == 0 and curr_sensor2 == 1 and curr_sensor3 == 0):
            #this is a valid reading and should mean we path straight
            #set pwm values to move our robot foward
            # pwm.ChangeDutyCycle(48)     #left motor
            # pwm2.ChangeDutyCycle(52)    #right motor
            leftmotor = 55
            rightmotor = 45
            print('forwards')
            # return(48,52, prev_sensor1, prev_sensor2, prev_sensor3)
        else:
            #if none of the previous values are met then the only possible options should be 111 (shouldnt happen) or 101 (shouldnt happen)
            #in either case we should just keep pathing foward til we find more valid values
            #set pwm for motors to move straight
            # pwm.ChangeDutyCycle(48)     #left motor
            # pwm2.ChangeDutyCycle(52)    #right motor
            leftmotor = 55
            rightmotor = 45
            print('lost?', curr_sensor1, curr_sensor2, curr_sensor3)
            # return(48,52, prev_sensor1, prev_sensor2, prev_sensor3)

    return(leftmotor,rightmotor, prev_sensor1, prev_sensor2, prev_sensor3)

    #check to see if the cart has reached the end point

def statemachine2(curr_sensor1, curr_sensor2, curr_sensor3, prev_sensor1, prev_sensor2, prev_sensor3): #this takes the sensor readings, and pathfinds

    if(curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 0):
    #if 000 do not update previous state with this value otherwise its REALLY lost
    #check previous state
        if((prev_sensor1 == 0 and prev_sensor2 == 0 and prev_sensor3 == 1) or (prev_sensor1 == 0 and prev_sensor2 == 1 and prev_sensor3 == 1)):
                #check if the value is 001 for a hard right
            if(prev_sensor1 == 0 and prev_sensor2 == 0 and prev_sensor3 == 1):
                #set pwm values for hard right turn
                # pwm.ChangeDutyCycle(52)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 53
                rightmotor = 0
                print('hard turn right lost /n')
                # return(52,52, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
            #values should be set to 011 so we should set pwm values for motors to slight right turn
                # pwm.ChangeDutyCycle(50)         #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 53
                rightmotor = 49
                print('slight turn right lost/n')
                # return(50,52, prev_sensor1, prev_sensor2, prev_sensor3)

        elif((prev_sensor1 == 1 and prev_sensor2 == 1 and prev_sensor3 == 0) or (prev_sensor1 == 1 and prev_sensor2 == 0 and prev_sensor3 == 0)):
            #check if the value is 100 for a hard left turn
            if(prev_sensor1 == 1 and prev_sensor2 == 0 and prev_sensor3 == 0):
                #set pwm values for hard left turn
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)    #right motor
                leftmotor = 49
                rightmotor = 47
                print('hardleft lost /n')
                # return(48,48, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
                #values should be 110 so we should set the pwm values for the motors to turn slightly right
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(50)    #right motor
                leftmotor = 0
                rightmotor = 47
                print('slightleft lost /n')
                # return(48,50, prev_sensor1, prev_sensor2, prev_sensor3)
        else:
            leftmotor = 52
            rightmotor = 48
            print('lost - lost?', prev_sensor1, prev_sensor2, prev_sensor3)

    elif(curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 1 or curr_sensor1 == 1 and curr_sensor2 == 1 and curr_sensor3 == 1):
        leftmotor = 52.25
        rightmotor = 47.75
        print('temp foward state')
    else:
        prev_sensor1 = curr_sensor1
        prev_sensor2 = curr_sensor2
        prev_sensor3 = curr_sensor3
         #check if the sensor values are either 001 or 011 for either slight or hard left
        if((curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 1) or (curr_sensor1 == 0 and curr_sensor2 == 1 and curr_sensor3 == 1)):
            #check if the value is 001 for a hard right
            if(curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 1):
                #set pwm values for hard right turn
                # pwm.ChangeDutyCycle(52)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 54
                rightmotor = 0
                print('hardright \n')
                # return(52,52, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
                #values should be set to 011 so we should set pwm values for motors to slight right turn
                # pwm.ChangeDutyCycle(50)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 54
                rightmotor = 49
                print('slightright \n')
                # return(50,52, prev_sensor1, prev_sensor2, prev_sensor3)

        elif((curr_sensor1 == 1 and curr_sensor2 == 1 and curr_sensor3 == 0) or (curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 0)):
            #check if the value is 100 for a hard left turn

            if(curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 0):
                #set pwm values for hard left turn
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)               #right motor
                leftmotor = 0
                rightmotor = 46
                print('hardleft \n')
                # return(48,48, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
            #values should be 110 so we should set the pwm values for the motors to turn slightly left
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)               #right motor
                leftmotor = 51
                rightmotor = 46
                print('slightleft \n')
                # return(48,50, prev_sensor1, prev_sensor2, prev_sensor3)

        elif(curr_sensor1 == 0 and curr_sensor2 == 1 and curr_sensor3 == 0):
            #this is a valid reading and should mean we path straight
            #set pwm values to move our robot foward
            # pwm.ChangeDutyCycle(48)     #left motor
            # pwm2.ChangeDutyCycle(52)    #right motor
            leftmotor = 52.25
            rightmotor = 47.75
            print('forwards')
            # return(48,52, prev_sensor1, prev_sensor2, prev_sensor3)
        else:
            #if none of the previous values are met then the only possible options should be 111 (shouldnt happen) or 101 (shouldnt happen)
            #in either case we should just keep pathing foward til we find more valid values
            #set pwm for motors to move straight
            # pwm.ChangeDutyCycle(48)     #left motor
            # pwm2.ChangeDutyCycle(52)    #right motor
            leftmotor = 52.25
            rightmotor = 47.75
            print('lost?', curr_sensor1, curr_sensor2, curr_sensor3)
            # return(48,52, prev_sensor1, prev_sensor2, prev_sensor3)


    return(leftmotor,rightmotor, prev_sensor1, prev_sensor2, prev_sensor3)

    #check to see if the cart has reached the end point




def collision_avoidance(pwi,pwi2,pwi3, ultrasonic_repeat):
    if ultrasonic_repeat == False:
        
        print("reverse, ultrasonic is true")
        left_motor = 45
        right_motor= 55
        sleeptime = .7
        if(pwi <= 15):
            print("Right Sensor = inches={}".format(pwi))
        elif(pwi2 <= 15):
            print("Left Sensor = inches={}".format(pwi2))
        elif(pwi3 <= 10):
            print("Middle Sensor = inches={}".format(pwi3))
        truefalse = True
        
    if ultrasonic_repeat == True:
        sleeptime = 0
        left_motor = 0
        right_motor = 0
        print("collision avoidance has stopped the robot")
        if(pwi <= 15):
            print("Right Sensor = inches={}".format(pwi))
        elif(pwi2 <= 15):
            print("Left Sensor = inches={}".format(pwi2))
        elif(pwi3 <= 10):
            print("Middle Sensor = inches={}".format(pwi3))
        truefalse = True


    return(left_motor, right_motor, truefalse, sleeptime)

#statemachine3 is the file for motors once it has momentum for stage 2 ----

def statemachine3(curr_sensor1, curr_sensor2, curr_sensor3, prev_sensor1, prev_sensor2, prev_sensor3): #this takes the sensor readings, and pathfinds

    if(curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 0):
    #if 000 do not update previous state with this value otherwise its REALLY lost
    #check previous state
        if((prev_sensor1 == 0 and prev_sensor2 == 0 and prev_sensor3 == 1) or (prev_sensor1 == 0 and prev_sensor2 == 1 and prev_sensor3 == 1)):
                #check if the value is 001 for a hard right
            if(prev_sensor1 == 0 and prev_sensor2 == 0 and prev_sensor3 == 1):
                #set pwm values for hard right turn
                # pwm.ChangeDutyCycle(52)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 53
                rightmotor = 52
                print('hard turn right lost /n')
                # return(52,52, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
            #values should be set to 011 so we should set pwm values for motors to slight right turn
                # pwm.ChangeDutyCycle(50)         #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 53
                rightmotor = 51
                print('slight turn right lost/n')
                # return(50,52, prev_sensor1, prev_sensor2, prev_sensor3)

        elif((prev_sensor1 == 1 and prev_sensor2 == 1 and prev_sensor3 == 0) or (prev_sensor1 == 1 and prev_sensor2 == 0 and prev_sensor3 == 0)):
            #check if the value is 100 for a hard left turn
            if(prev_sensor1 == 1 and prev_sensor2 == 0 and prev_sensor3 == 0):
                #set pwm values for hard left turn
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)    #right motor
                leftmotor = 49
                rightmotor = 47
                print('hardleft lost /n')
                # return(48,48, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
                #values should be 110 so we should set the pwm values for the motors to turn slightly right
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(50)    #right motor
                leftmotor = 49.5
                rightmotor = 47
                print('slightleft lost /n')
                # return(48,50, prev_sensor1, prev_sensor2, prev_sensor3)
        else:
            leftmotor = 52
            rightmotor = 48
            print('lost - lost?', prev_sensor1, prev_sensor2, prev_sensor3)

    elif(curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 1 or curr_sensor1 == 1 and curr_sensor2 == 1 and curr_sensor3 == 1):
        leftmotor = 52.25
        rightmotor = 47.75
        print('temp foward state')
    else:
        prev_sensor1 = curr_sensor1
        prev_sensor2 = curr_sensor2
        prev_sensor3 = curr_sensor3
         #check if the sensor values are either 001 or 011 for either slight or hard left
        if((curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 1) or (curr_sensor1 == 0 and curr_sensor2 == 1 and curr_sensor3 == 1)):
            #check if the value is 001 for a hard right
            if(curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 1):
                #set pwm values for hard right turn
                # pwm.ChangeDutyCycle(52)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 54
                rightmotor = 52
                print('hardright \n')
                # return(52,52, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
                #values should be set to 011 so we should set pwm values for motors to slight right turn
                # pwm.ChangeDutyCycle(50)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 54
                rightmotor = 51
                print('slightright \n')
                # return(50,52, prev_sensor1, prev_sensor2, prev_sensor3)

        elif((curr_sensor1 == 1 and curr_sensor2 == 1 and curr_sensor3 == 0) or (curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 0)):
            #check if the value is 100 for a hard left turn

            if(curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 0):
                #set pwm values for hard left turn
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)               #right motor
                leftmotor = 48
                rightmotor = 46
                print('hardleft \n')
                # return(48,48, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
            #values should be 110 so we should set the pwm values for the motors to turn slightly left
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)               #right motor
                leftmotor = 48
                rightmotor = 45
                print('slightleft \n')
                # return(48,50, prev_sensor1, prev_sensor2, prev_sensor3)

        elif(curr_sensor1 == 0 and curr_sensor2 == 1 and curr_sensor3 == 0):
            #this is a valid reading and should mean we path straight
            #set pwm values to move our robot foward
            # pwm.ChangeDutyCycle(48)     #left motor
            # pwm2.ChangeDutyCycle(52)    #right motor
            leftmotor = 52.25
            rightmotor = 47.75
            print('forwards')
            # return(48,52, prev_sensor1, prev_sensor2, prev_sensor3)
        else:
            #if none of the previous values are met then the only possible options should be 111 (shouldnt happen) or 101 (shouldnt happen)
            #in either case we should just keep pathing foward til we find more valid values
            #set pwm for motors to move straight
            # pwm.ChangeDutyCycle(48)     #left motor
            # pwm2.ChangeDutyCycle(52)    #right motor
            leftmotor = 52.25
            rightmotor = 47.75
            print('lost?', curr_sensor1, curr_sensor2, curr_sensor3)
            # return(48,52, prev_sensor1, prev_sensor2, prev_sensor3)


    return(leftmotor,rightmotor, prev_sensor1, prev_sensor2, prev_sensor3)


def statemachinepathbacksecstage(curr_sensor1, curr_sensor2, curr_sensor3, prev_sensor1, prev_sensor2, prev_sensor3): #this takes the sensor readings, and pathfinds

    if(curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 0):
    #if 000 do not update previous state with this value otherwise its REALLY lost
    #check previous state
        if((prev_sensor1 == 0 and prev_sensor2 == 0 and prev_sensor3 == 1) or (prev_sensor1 == 0 and prev_sensor2 == 1 and prev_sensor3 == 1)):
                #check if the value is 001 for a hard right
            if(prev_sensor1 == 0 and prev_sensor2 == 0 and prev_sensor3 == 1):
                #set pwm values for hard right turn
                # pwm.ChangeDutyCycle(52)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 53.5
                rightmotor = 52.5
                print('hard turn right lost /n')
                # return(52,52, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
            #values should be set to 011 so we should set pwm values for motors to slight right turn
                # pwm.ChangeDutyCycle(50)         #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 52
                rightmotor = 51
                print('slight turn right lost/n')
                # return(50,52, prev_sensor1, prev_sensor2, prev_sensor3)

        elif((prev_sensor1 == 1 and prev_sensor2 == 1 and prev_sensor3 == 0) or (prev_sensor1 == 1 and prev_sensor2 == 0 and prev_sensor3 == 0)):
            #check if the value is 100 for a hard left turn
            if(prev_sensor1 == 1 and prev_sensor2 == 0 and prev_sensor3 == 0):
                #set pwm values for hard left turn
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)    #right motor
                leftmotor = 47
                rightmotor = 47
                print('hardleft lost /n')
                # return(48,48, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
                #values should be 110 so we should set the pwm values for the motors to turn slightly right
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(50)    #right motor
                leftmotor = 48
                rightmotor = 47
                print('slightleft lost /n')
                # return(48,50, prev_sensor1, prev_sensor2, prev_sensor3)
        else:
            leftmotor = 51
            rightmotor = 49
            print('lost - lost?', prev_sensor1, prev_sensor2, prev_sensor3)
    elif(curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 1 or curr_sensor1 == 1 and curr_sensor2 == 1 and curr_sensor3 == 1):
        leftmotor = 52.5 
        rightmotor = 47.5
        print('temp foward state')
    else:
        prev_sensor1 = curr_sensor1
        prev_sensor2 = curr_sensor2
        prev_sensor3 = curr_sensor3
         #check if the sensor values are either 001 or 011 for either slight or hard left
        if((curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 1) or (curr_sensor1 == 0 and curr_sensor2 == 1 and curr_sensor3 == 1)):
            #check if the value is 001 for a hard right
            if(curr_sensor1 == 0 and curr_sensor2 == 0 and curr_sensor3 == 1):
                #set pwm values for hard right turn
                # pwm.ChangeDutyCycle(52)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 52
                rightmotor = 50.5
                print('hardright \n')
                # return(52,52, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
                #values should be set to 011 so we should set pwm values for motors to slight right turn
                # pwm.ChangeDutyCycle(50)     #left motor
                # pwm2.ChangeDutyCycle(52)    #right motor
                leftmotor = 52
                rightmotor = 49.5
                print('slightright \n')
                # return(50,52, prev_sensor1, prev_sensor2, prev_sensor3)

        elif((curr_sensor1 == 1 and curr_sensor2 == 1 and curr_sensor3 == 0) or (curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 0)):
            #check if the value is 100 for a hard left turn

            if(curr_sensor1 == 1 and curr_sensor2 == 0 and curr_sensor3 == 0):
                #set pwm values for hard left turn
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)               #right motor
                leftmotor = 48.5
                rightmotor = 47.75
                print('hardleft \n')
                # return(48,48, prev_sensor1, prev_sensor2, prev_sensor3)
            else:
            #values should be 110 so we should set the pwm values for the motors to turn slightly left
                # pwm.ChangeDutyCycle(48)     #left motor
                # pwm2.ChangeDutyCycle(48)               #right motor
                leftmotor = 49.25
                rightmotor = 48
                print('slightleft \n')
                # return(48,50, prev_sensor1, prev_sensor2, prev_sensor3)

        elif(curr_sensor1 == 0 and curr_sensor2 == 1 and curr_sensor3 == 0):
            #this is a valid reading and should mean we path straight
            #set pwm values to move our robot foward
            # pwm.ChangeDutyCycle(48)     #left motor
            # pwm2.ChangeDutyCycle(52)    #right motor
            leftmotor = 52.5
            rightmotor = 47.5
            print('forwards')
            # return(48,52, prev_sensor1, prev_sensor2, prev_sensor3)
        else:
            #if none of the previous values are met then the only possible options should be 111 (shouldnt happen) or 101 (shouldnt happen)
            #in either case we should just keep pathing foward til we find more valid values
            #set pwm for motors to move straight
            # pwm.ChangeDutyCycle(48)     #left motor
            # pwm2.ChangeDutyCycle(52)    #right motor
            leftmotor = 48.5
            rightmotor = 47.5
            print('lost?', curr_sensor1, curr_sensor2, curr_sensor3)
            # return(48,52, prev_sensor1, prev_sensor2, prev_sensor3)

    return(leftmotor,rightmotor, prev_sensor1, prev_sensor2, prev_sensor3)



# def read_pwm():
#     class reader:
#     #    """
#     #    A class to read PWM pulses and calculate their frequency
#     #    and duty cycle.  The frequency is how often the pulse
#     #    happens per second.  The duty cycle is the percentage of
#     #    pulse high time per cycle.
#     #    """
#         def __init__(self, pi, gpio, weighting=0.0):
#                 #   """
#                 #   Instantiate with the Pi and gpio of the PWM signal
#                 #   to monitor.

#                 #   Optionally a weighting may be specified.  This is a number
#                 #   between 0 and 1 and indicates how much the old reading
#                 #   affects the new reading.  It defaults to 0 which means
#                 #   the old reading has no effect.  This may be used to
#                 #   smooth the data.
#                 #   """
#             self.pi = pi
#             self.gpio = gpio

#             if weighting < 0.0:
#                 weighting = 0.0
#             elif weighting > 0.99:
#                 weighting = 0.99

#             self._new = 1.0 - weighting # Weighting for new reading.
#             self._old = weighting       # Weighting for old reading.

#             self._high_tick = None
#             self._period = None
#             self._high = None

#             pi.set_mode(gpio, pigpio.INPUT)

#             self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

#         def _cbf(self, gpio, level, tick):

#             if level == 1:

#                 if self._high_tick is not None:
#                     t = pigpio.tickDiff(self._high_tick, tick)

#                     if self._period is not None:
#                         self._period = (self._old * self._period) + (self._new * t)
#                     else:
#                         self._period = t

#                     self._high_tick = tick

#             elif level == 0:

#                 if self._high_tick is not None:
#                     t = pigpio.tickDiff(self._high_tick, tick)

#                     if self._high is not None:
#                         self._high = (self._old * self._high) + (self._new * t)
#                     else:
#                         self._high = t

#         def frequency(self):
#                 #   """
#                 #   Returns the PWM frequency.
#                 #   """
#             if self._period is not None:
#                 return 1000000.0 / self._period
#             else:
#                 return 0.0

#         def pulse_width(self):
#                 #   """
#                 #   Returns the PWM pulse width in microseconds.
#                 #   """
#             if self._high is not None:
#                 return self._high
#             else:
#                 return 0.0

#         def duty_cycle(self):
#                 #   """
#                 #   Returns the PWM duty cycle percentage.
#                 #   """
#             if self._high is not None:
#                 return 100.0 * self._high / self._period
#             else:
#                 return 0.0

#         def cancel(self):
#                 #   """
#                 #   Cancels the reader and releases resources.
#                 #   """
#             self._cb.cancel()

