#updated 11/2/2021 11:58pm -Micah
#updated 11/3/2021 6:30pm -Jared
#updated 11/3/2021 11:00pm -Jared and Micah
#update 11/14/2021 7:15pm removed pwm.stop and replaced with pwm.changedutycycle(0).

from helper import checkstate, statemachine,statemachine2,statemachine3, collision_avoidance, checkstate2, checkstate3 #import helper file
import read_PWM_functions #import Ultrasonic functions
#importing GUI libraries
#from updatedUI import Employee_Class, Customer_Class
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys
import time

#importing dependencies for raspberry pi functionality
import board
import adafruit_tcs34725
import busio
import pigpio
import RPi.GPIO as GPIO   # Import the GPIO library.
from adafruit_extended_bus import ExtendedI2C as I2C

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
i2c2 = I2C(4)
i2c3 = I2C(3)

#setting up IR sensors
sensor = adafruit_tcs34725.TCS34725(i2c)
sensor2 = adafruit_tcs34725.TCS34725(i2c2)
sensor3 = adafruit_tcs34725.TCS34725(i2c3)


GPIO.setup(18, GPIO.OUT)  # Set GPIO 18 to output mode.
GPIO.setup(12, GPIO.OUT)  # Set GPIO 12 to output mode.
pwm = GPIO.PWM(18, 350)   # Initialize PWM on pwmPin 350Hz frequency
pwm2 = GPIO.PWM(12, 350)   # Initialize PWM on pwmPin 350Hz frequency

#initialize pwm motor values to start at 0 -- do nothing basically
dc=0                               # set dc variable to 0 for 0%
pwm.start(dc)                      # Start PWM withS 0% duty cycle
pwm2.start(dc)

#initialize previous sensor states to default value
prev_sensor1 = 0
prev_sensor2 = 0
prev_sensor3 = 0

#read_pwm setup for collision avoidance
PWM_GPIO = 26
RUN_TIME = 60.0
SAMPLE_TIME = 2.0

PWM_GPIO2 = 19    #gpio pin for ultrasonic 2
PWM_GPIO3 = 6    #gpio pin for ultrasonic 3

pi = pigpio.pi()

p = read_PWM_functions.reader(pi, PWM_GPIO)      #pwm for ultrasonic 1
p2 = read_PWM_functions.reader(pi, PWM_GPIO2)    #pwm for ultrasonic 2
p3 = read_PWM_functions.reader(pi, PWM_GPIO3)    #pwm for ultrasonic 3

# global customer_location
DURATION_INT = 300

#gui classes setup
class Employee_Class(QMainWindow):
    def __init__(self):
        super(Employee_Class, self).__init__()
        loadUi("EmployeeUI.ui", self)

        self.EnterButton.clicked.connect(lambda: button_press("Enter"))
        self.EnterButton.clicked.connect(self.go_page2)

        self.OneButton.clicked.connect(lambda: button_press("1"))
        self.TwoButton.clicked.connect(lambda: button_press("2"))
        self.ThreeButton.clicked.connect(lambda: button_press("3"))
        self.FourButton.clicked.connect(lambda: button_press("4"))
        self.FiveButton.clicked.connect(lambda: button_press("5"))
        self.SixButton.clicked.connect(lambda: button_press("6"))
        self.SevenButton.clicked.connect(lambda: button_press("7"))
        self.EightButton.clicked.connect(lambda: button_press("8"))
        self.NineButton.clicked.connect(lambda: button_press("9"))
        self.ClearButton.clicked.connect(lambda: button_press("Clear"))

        def button_press(pressed):
            #checks if clear is pressed, if so then set the label to nothing
            if pressed == "Clear":
                self.displaylabel.setText("")

            elif pressed == "Enter":
                self.displaylabel.setText(f'{self.LettercomboBox.currentText()}{self.displaylabel.text()}')

                self.customer_location = self.displaylabel.text()

                #printlocation(self.curbsideposition)       #used to call the function in main file which takes string and prints the customer location


                #return self.customer_location

            else:
                self.displaylabel.setText(f'{self.displaylabel.text()}{pressed}')

    def go_page2(self):

        if(self.customer_location == "A865"):
            self.curbsideposition = 1
            pathfinding(self.curbsideposition)

            page2.Deliverylabel.setText(self.customer_location)
            self.displaylabel.setText("")
            page2.timer_start()
            page2.update_gui()
            widget.setCurrentIndex(widget.currentIndex()+1)
        elif(self.customer_location == "B865"):
            self.curbsideposition = 2
            pathfinding(self.curbsideposition)

            page2.Deliverylabel.setText(self.customer_location)
            self.displaylabel.setText("")
            page2.timer_start()
            page2.update_gui()
            widget.setCurrentIndex(widget.currentIndex()+1)
        elif(self.customer_location == "C865"):
            self.curbsideposition =3
            pathfinding(self.curbsideposition)

            page2.Deliverylabel.setText(self.customer_location)
            self.displaylabel.setText("")
            page2.timer_start()
            page2.update_gui()
            widget.setCurrentIndex(widget.currentIndex()+1)
        # elif(self.customer_location == "D865"):
        #     self.curbsideposition =4
        #     pathfinding(self.curbsideposition)

        #     page2.Deliverylabel.setText(self.customer_location)
        #     self.displaylabel.setText("")
        #     page2.timer_start()
        #     page2.update_gui()
        #     widget.setCurrentIndex(widget.currentIndex()+1)
        # elif(self.customer_location == "E865"):
        #     self.curbsideposition =5
        #     pathfinding(self.curbsideposition)

        #     page2.Deliverylabel.setText(self.customer_location)
        #     self.displaylabel.setText("")
        #     page2.timer_start()
        #     page2.update_gui()
        #     widget.setCurrentIndex(widget.currentIndex()+1)
        # elif(self.customer_location == "F865"):
        #     self.curbsideposition =6
        #     pathfinding(self.curbsideposition)

        #     page2.Deliverylabel.setText(self.customer_location)
        #     self.displaylabel.setText("")
        #     page2.timer_start()
        #     page2.update_gui()
        #     widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            self.displaylabel.setText("")



        # countdown(10)


class Customer_Class(QMainWindow):
    def __init__(self):

        super(Customer_Class, self).__init__()
        loadUi("customerUI.ui", self)
        self.completionButton.clicked.connect(self.go_page1)

        self.extensionButton.clicked.connect(self.extend_timer)


        # self.Deliverylabel.setText(customer_location)
    def timer_start(self):
        self.time_left_int = DURATION_INT


        self.my_qtimer = QtCore.QTimer(self)
        self.my_qtimer.timeout.connect(self.timer_timeout)
        self.my_qtimer.start(1000)

        self.update_gui()

    def timer_timeout(self):

        self.time_left_int -= 1
        #print("here", self.time_left_int)

        if self.time_left_int == 0:
            self.go_page1()
            widget.setCurrentIndex(widget.currentIndex()-1)

        self.update_gui()

    def update_gui(self):
        mins, secs = divmod(self.time_left_int, 60)
        self.timeformat = '{:02d}:{:02d}'.format(mins, secs)
        self.timerLabel.setText(str(self.timeformat))

    def  extend_timer(self):
         self.time_left_int += 60


    def go_page1(self):
        self.my_qtimer.stop()
        pathfinding_back()
        widget.setCurrentIndex(widget.currentIndex()-1)
        


#gui setup here
app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
widget.setFixedHeight(600)
widget.setFixedWidth(700)
ui=Employee_Class()
widget.addWidget(ui)
page2=Customer_Class()
widget.addWidget(page2)
widget.show()

if __name__ == "__main__":

    def pathfinding(curbsideposition):
        counter = curbsideposition
        close_state1 = 0
        close_state2 = 0
        close_state3 = 0

        prev_sensor1 = 0
        prev_sensor2 = 0
        prev_sensor3 = 0
        leftmotor = 50
        rightmotor = 50


        #initialize the motor with higher pwm values to start off the robot with weight
        #pwm.ChangeDutyCycle(56)
        #pwm2.ChangeDutyCycle(44)
        #time.sleep(.1)
        endloop = 1
        redcounter = 0
      #this portion of the code paths from the store to the general curbside location
             #needs to constantly be checking
        while(endloop != 0):
        #setting up ultrasonics
        #ultrasonic pwi=Right sensor, pwi2=Left sensor, pwi3=Middle Sensor
            #time.sleep(SAMPLE_TIME)
            pw = p.pulse_width()             #ultrasonic
            pwi = (pw+.5)/147
            pw2 = p2.pulse_width()           #ultrasonic 2
            pwi2 = (pw2+.5)/147
            pw3 = p3.pulse_width()           #ultrasonic 3
            pwi3 = (pw3+.5)/147
#             print("Right Sensor = inches={}".format(pwi))
#             print("Left Sensor = inches={}".format(pwi2))
#             print("Middle Sensor = inches={}".format(pwi3))

            if pwi <= 0 or pwi2 <= 0 or pwi3 <= 0: #collision avoidance
                leftmotor, rightmotor = collision_avoidance(pwi, pwi2, pwi3)
                if(pwi <= 0):
                    print("Right Sensor = inches={}".format(pwi))
                elif(pwi2 <= 0):
                    print("Left Sensor = inches={}".format(pwi2))
                elif(pwi3 <= 0):
                    print("Middle Sensor = inches={}".format(pwi3))
                pwm.ChangeDutyCycle(0)                  # stop PWM
                pwm2.ChangeDutyCycle(0)                 # stop PWM
                time.sleep(1)
            else:
            #needs to constantly be checking
                curr_sensor1, curr_sensor2, curr_sensor3, close_state1, close_state2, close_state3 = checkstate(sensor, sensor2, sensor3)
            #needs to constantly be pathfinding until reaches endstate
                leftmotor, rightmotor, prev_sensor1, prev_sensor2, prev_sensor3 = statemachine(curr_sensor1, curr_sensor2, curr_sensor3, prev_sensor1, prev_sensor2, prev_sensor3)

            #Control motor from pathfinding values
                pwm.ChangeDutyCycle(rightmotor)
                pwm2.ChangeDutyCycle(leftmotor)
                print("checkstate 1 is active")
                     
            if(redcounter == 0):
                if(close_state1 == 1 and close_state2 == 1 and close_state3 ==1):
                    endloop -= 1
                    redcounter +=1
                    print("counter value = ", endloop)
                    print("redcounter value = ", redcounter)
                elif(close_state1 & close_state2 == 1) or (close_state1 & close_state3 == 1) or (close_state2 & close_state3 == 1):
                    endloop -=1
                    redcounter +=1
                    print("counter value = ", endloop)
                    print("redcounter value = ", redcounter)
                else:
                    print("counter value = ", endloop)
                    print("redcounter value = ", redcounter)
            else:
                if(curr_sensor1 or curr_sensor2 or curr_sensor3 == 1):
                    redcounter -= 1

        print(close_state1, close_state2, close_state3)
            #this portion of the code paths to the correct curbside position marker once its at the general curbside location

        prev_sensor1 = 0
        prev_sensor2 = 1
        prev_sensor3 = 0

        close_state1 = 0
        close_state2 = 0
        close_state3 = 0

        pwm.ChangeDutyCycle(45)
        pwm2.ChangeDutyCycle(55)

        while(counter != 0):
            #time.sleep(SAMPLE_TIME)
            pw = p.pulse_width()             #ultrasonic
            pwi = (pw+.5)/147
            pw2 = p2.pulse_width()           #ultrasonic 2
            pwi2 = (pw2+.5)/147
            pw3 = p3.pulse_width()           #ultrasonic 3
            pwi3 = (pw3+.5)/147


            if pwi <= 0 or pwi2 <= 0 or pwi3 <= 0:
                #leftmotor, rightmotor = collision_avoidance(pwi, pwi2, pwi3)
                if(pwi <= 0):
                    print("Right Sensor = inches={}".format(pwi))
                elif(pwi2 <= 0):
                    print("Left Sensor = inches={}".format(pwi2))
                elif(pwi3 <= 0):
                    print("Middle Sensor = inches={}".format(pwi3))
                pwm.ChangeDutyCycle(0)                  # stop PWM
                pwm2.ChangeDutyCycle(0)                 # stop PWM                 # stop PWM
                time.sleep(1)

            else:
                curr_sensor1, curr_sensor2, curr_sensor3, counter, redcounter = checkstate2(sensor, sensor2, sensor3, counter,redcounter)


                leftmotor, rightmotor, prev_sensor1, prev_sensor2, prev_sensor3 = statemachine3(curr_sensor1, curr_sensor2, curr_sensor3, prev_sensor1, prev_sensor2, prev_sensor3)

                pwm.ChangeDutyCycle(rightmotor)
                pwm2.ChangeDutyCycle(leftmotor)
                print("checkstate 2 is active")

        print("finished state 2")
        print("finished state 2")
        print("finished state 2")
        print("finished state 2")
        print("finished state 2")
        print("finished state 2")
        print("-------------------------------------")

        #slow down the motor after it reaches the end state
#         pwm.ChangeDutyCycle(52)
#         pwm2.ChangeDutyCycle(48)
# 
#         time.sleep(0.3)

        #pwm.ChangeDutyCycle(48)
        #pwm2.ChangeDutyCycle(52)

        #time.sleep(0.4)

        # pwm.ChangeDutyCycle()
        # pwm2.ChangeDutyCycle()

        pwm.ChangeDutyCycle(52)                  # turn left
        pwm2.ChangeDutyCycle(45.75)                 # turn left
        time.sleep(.25)
            #this portion of the code should pathfinding from the curbside beginning spot to the actual customer position aka the final destination
        close_state1 = 0
        close_state2 = 0
        close_state3 = 0
        endloop = 1
             # while close_state1 & close_state2 & close_state3 == 0:
             #needs to constantly be checking
        while(endloop != 0):
            #time.sleep(SAMPLE_TIME)
            pw = p.pulse_width()             #ultrasonic
            pwi = (pw+.5)/147
            pw2 = p2.pulse_width()           #ultrasonic 2
            pwi2 = (pw2+.5)/147
            pw3 = p3.pulse_width()           #ultrasonic 3
            pwi3 = (pw3+.5)/147


            if pwi <= 0 or pwi2 <= 0 or pwi3 <= 0:
                #leftmotor, rightmotor = collision_avoidance(pwi, pwi2, pwi3)
                if(pwi <= 0):
                    print("Right Sensor = inches={}".format(pwi))
                elif(pwi2 <= 0):
                    print("Left Sensor = inches={}".format(pwi2))
                elif(pwi3 <= 0):
                    print("Middle Sensor = inches={}".format(pwi3))
                pwm.ChangeDutyCycle(0)                  # stop PWM
                pwm2.ChangeDutyCycle(0)                 # stop PWM
                time.sleep(1)
            else:
                curr_sensor1, curr_sensor2, curr_sensor3, close_state1, close_state2, close_state3 = checkstate3(sensor, sensor2, sensor3)
        #             #needs to constantly be pathfinding until reaches endstate
                leftmotor, rightmotor, prev_sensor1, prev_sensor2, prev_sensor3 = statemachine3(curr_sensor1, curr_sensor2, curr_sensor3, prev_sensor1, prev_sensor2, prev_sensor3)

        #             #Control motor from pathfinding values
                pwm.ChangeDutyCycle(rightmotor)
                pwm2.ChangeDutyCycle(leftmotor)
                print("checkstate 3 is active")
                        
            if(redcounter == 0):
                if(close_state1 == 1 and close_state2 == 1 and close_state3 ==1):
                    endloop -= 1
                    redcounter +=1
                    print("counter value = ", endloop)
                    print("redcounter value = ", redcounter)
                elif(close_state1 & close_state2 == 1) or (close_state1 & close_state3 == 1) or (close_state2 & close_state3 == 1):
                    endloop -=1
                    redcounter +=1
                    print("counter value = ", endloop)
                    print("redcounter value = ", redcounter)
                else:
                    print("counter value = ", endloop)
                    print("redcounter value = ", redcounter)
            else:
                if(curr_sensor1 or curr_sensor2 or curr_sensor3 == 1):
                    redcounter -= 1
        print("CHECKSTATE 3 IS COMPLETE")
        print("-----------------")
        print("-----------------")
        print("-----------------")
        pwm.ChangeDutyCycle(55)
        pwm2.ChangeDutyCycle(45)

        time.sleep(.8)


        pwm.ChangeDutyCycle(0)                  # stop PWM
        pwm2.ChangeDutyCycle(0)              # stop PWM

        print(curbsideposition)

    # needs to constantly be checking for obstacles
    def pathfinding_back():
        close_state1 = 0
        close_state2 = 0
        close_state3 = 0
        prev_sensor1 = 0
        prev_sensor2 = 0
        prev_sensor3 = 0
    #         # while close_state1 & close_state2 & close_state3 == 0:
    #         #needs to constantly be checking
        while close_state1 & close_state2 & close_state3 == 0:
            #time.sleep(SAMPLE_TIME)
            pw = p.pulse_width()             #ultrasonic
            pwi = (pw+.5)/147
            pw2 = p2.pulse_width()           #ultrasonic 2
            pwi2 = (pw2+.5)/147
            pw3 = p3.pulse_width()           #ultrasonic 3
            pwi3 = (pw3+.5)/147


            if pwi <= 15 or pwi2 <= 0 or pwi3 <= 0:
                #leftmotor, rightmotor = collision_avoidance(pwi, pwi2, pwi3)
                if(pwi <= 15):
                    print("Right Sensor = inches={}".format(pwi))
                elif(pwi2 <= 0):
                    print("Left Sensor = inches={}".format(pwi2))
                elif(pwi3 <= 0):
                    print("Middle Sensor = inches={}".format(pwi3))
                pwm.ChangeDutyCycle(0)                  # stop PWM
                pwm2.ChangeDutyCycle(0)                 # stop PWM
                time.sleep(1)
            else:
                curr_sensor1, curr_sensor2, curr_sensor3, close_state1, close_state2, close_state3 = checkstate(sensor, sensor2, sensor3)
                #needs to constantly be pathfinding until reaches endstate
                leftmotor, rightmotor, prev_sensor1, prev_sensor2, prev_sensor3 = statemachine2(curr_sensor1, curr_sensor2, curr_sensor3, prev_sensor1, prev_sensor2, prev_sensor3)

    #             #Control motor from pathfinding values
                pwm.ChangeDutyCycle(rightmotor)
                pwm2.ChangeDutyCycle(leftmotor)
                print("running")

        #slow down to a stop
        pwm.ChangeDutyCycle(52)
        pwm2.ChangeDutyCycle(48)

        time.sleep(0.3)

        pwm.ChangeDutyCycle(48)
        pwm2.ChangeDutyCycle(52)

        time.sleep(0.5)

        # pwm.ChangeDutyCycle()
        # pwm2.ChangeDutyCycle()

        pwm.ChangeDutyCycle(0)                 # stop PWM
        pwm2.ChangeDutyCycle(0)                # stop PWM

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

