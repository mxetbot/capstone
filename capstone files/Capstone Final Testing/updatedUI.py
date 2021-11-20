import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow 
import time

# global customer_location
DURATION_INT = 300

# class employeeinput(object):
#     customer_location = ""

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
        widget.setCurrentIndex(widget.currentIndex()-1)


# def customer_curbside_location(customer_location):
#     if(customer_location == "A865"):
#         curbsideposition = 1
#     elif(customer_location == "B865"):
#         curbsideposition = 2
#     elif(customer_location == "C865"):
#         curbsideposition =3
#     else:
#         print("not valid input")
#     print(customer_location)
#     print(curbsideposition)
#     return curbsideposition 


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
    # * run loop
    # Driver Code
    
    # Bring up window
    # def printlocation(curbsideposition):
        
    #     print(curbsideposition)
    

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting") 