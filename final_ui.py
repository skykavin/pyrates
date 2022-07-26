# pyqt5 classes
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import *

#database and mqtt
import pymongo
import paho.mqtt.client as paho

# hardware function modules
import time
import random
from getpass import getpass
from datetime import datetime
from smbus import SMBus
import datetime as d
import RPi.GPIO as GPIO

# files in folder classes
import idr_read
from max6675 import MAX6675, MAX6675Error



#thermocouple
cs_1_pin = 17
cs_pin = 24
clock_pin = 23
data_pin = 22
units = "c"
#global temp_list = []
#global time_list = []

# client variables
client = pymongo.MongoClient("mongodb+srv://sgk2303:gokul1234@cluster0.dsp9o.mongodb.net/?retryWrites=true&w=majority")
db=client.pyrates
coll2=db.temp
coll1=db.feed

# gpio and declared pins 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(13, GPIO.IN)
GPIO.setup(6, GPIO.IN)

# max6675 objects
thermocouple = MAX6675(cs_pin, clock_pin, data_pin, units)
thermocouple_1 = MAX6675(cs_1_pin, clock_pin, data_pin, units)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(469, 244)
        MainWindow.setStyleSheet("background-color: rgb(23, 23, 23);")
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 461, 31))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 47, 31))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../Downloads/plasticpyrolysisplantindia-removebg-preview.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.team_name = QtWidgets.QLabel(self.frame)
        self.team_name.setGeometry(QtCore.QRect(170, 0, 131, 31))
        self.team_name.setStyleSheet("color: rgb(255, 137, 3);\n"
"font-family: \'Staatliches\', cursive;")
        self.team_name.setAlignment(QtCore.Qt.AlignCenter)
        self.team_name.setObjectName("team_name")
        self.main_value_frame = QtWidgets.QFrame(self.centralwidget)
        self.main_value_frame.setGeometry(QtCore.QRect(10, 30, 111, 201))
        self.main_value_frame.setObjectName("main_value_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_value_frame)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.reactor_tem = QtWidgets.QLabel(self.main_value_frame)
        self.reactor_tem.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.reactor_tem.setAlignment(QtCore.Qt.AlignCenter)
        self.reactor_tem.setObjectName("reactor_tem")
        self.verticalLayout.addWidget(self.reactor_tem)
        self.catalyst_tem = QtWidgets.QLabel(self.main_value_frame)
        self.catalyst_tem.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.catalyst_tem.setAlignment(QtCore.Qt.AlignCenter)
        self.catalyst_tem.setObjectName("catalyst_tem")
        self.verticalLayout.addWidget(self.catalyst_tem)
        self.motor_1 = QtWidgets.QLabel(self.main_value_frame)
        self.motor_1.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.motor_1.setAlignment(QtCore.Qt.AlignCenter)
        self.motor_1.setObjectName("motor_1")
        self.verticalLayout.addWidget(self.motor_1)
        self.motor_2 = QtWidgets.QLabel(self.main_value_frame)
        self.motor_2.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.motor_2.setAlignment(QtCore.Qt.AlignCenter)
        self.motor_2.setObjectName("motor_2")
        self.verticalLayout.addWidget(self.motor_2)
        self.reactor_induction_2 = QtWidgets.QLabel(self.main_value_frame)
        self.reactor_induction_2.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.reactor_induction_2.setAlignment(QtCore.Qt.AlignCenter)
        self.reactor_induction_2.setObjectName("reactor_induction_2")
        self.verticalLayout.addWidget(self.reactor_induction_2)
        self.feed_pressure_frame = QtWidgets.QFrame(self.centralwidget)
        self.feed_pressure_frame.setGeometry(QtCore.QRect(150, 120, 81, 111))
        self.feed_pressure_frame.setObjectName("feed_pressure_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.feed_pressure_frame)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.motor_1_indi = QtWidgets.QLCDNumber(self.feed_pressure_frame)
        self.motor_1_indi.setStyleSheet("color:  rgb(255, 137, 3);\n"
"border-color:  rgb(255, 137, 3);")
        self.motor_1_indi.setObjectName("motor_1_indi")
        self.verticalLayout_2.addWidget(self.motor_1_indi)
        self.motor_2_indi = QtWidgets.QLCDNumber(self.feed_pressure_frame)
        self.motor_2_indi.setStyleSheet("color:  rgb(255, 137, 3);\n"
"border-color:  rgb(255, 137, 3);")
        self.motor_2_indi.setObjectName("motor_2_indi")
        self.verticalLayout_2.addWidget(self.motor_2_indi)
        self.reactor_induction = QtWidgets.QLCDNumber(self.feed_pressure_frame)
        self.reactor_induction.setObjectName("reactor_induction")
        self.verticalLayout_2.addWidget(self.reactor_induction)
        self.motors_frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.motors_frame_2.setGeometry(QtCore.QRect(250, 120, 91, 101))
        self.motors_frame_2.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.motors_frame_2.setObjectName("motors_frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.motors_frame_2)
        self.verticalLayout_3.setSpacing(13)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pressure_label = QtWidgets.QLabel(self.motors_frame_2)
        self.pressure_label.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.pressure_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pressure_label.setObjectName("pressure_label")
        self.verticalLayout_3.addWidget(self.pressure_label)
        self.Feed_label = QtWidgets.QLabel(self.motors_frame_2)
        self.Feed_label.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.Feed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Feed_label.setObjectName("Feed_label")
        self.verticalLayout_3.addWidget(self.Feed_label)
        self.motors_frame = QtWidgets.QFrame(self.centralwidget)
        self.motors_frame.setGeometry(QtCore.QRect(360, 120, 91, 101))
        self.motors_frame.setObjectName("motors_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.motors_frame)
        self.verticalLayout_4.setSpacing(20)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pressure_value = QtWidgets.QLCDNumber(self.motors_frame)
        self.pressure_value.setObjectName("pressure_value")
        self.verticalLayout_4.addWidget(self.pressure_value)
        self.Feed_rate = QtWidgets.QLCDNumber(self.motors_frame)
        self.Feed_rate.setStyleSheet("color:  rgb(255, 137, 3);\n"
"border-color:  rgb(255, 137, 3);")
        self.Feed_rate.setObjectName("Feed_rate")
        self.verticalLayout_4.addWidget(self.Feed_rate)
        self.progress_bar_frame = QtWidgets.QFrame(self.centralwidget)
        self.progress_bar_frame.setGeometry(QtCore.QRect(140, 40, 111, 81))
        self.progress_bar_frame.setObjectName("progress_bar_frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.progress_bar_frame)
        self.verticalLayout_5.setSpacing(20)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tem_rt_bar = QtWidgets.QProgressBar(self.progress_bar_frame)
        self.tem_rt_bar.setStyleSheet("background-color: rgb(107, 107, 107);\n"
"border-color: rgb(99, 99, 99);\n"
"")
        self.tem_rt_bar.setMaximum(10)
        self.tem_rt_bar.setProperty("value", 1)
        self.tem_rt_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.tem_rt_bar.setTextVisible(True)
        self.tem_rt_bar.setObjectName("tem_rt_bar")
        self.verticalLayout_5.addWidget(self.tem_rt_bar)
        self.tem_rt_bar_2 = QtWidgets.QProgressBar(self.progress_bar_frame)
        self.tem_rt_bar_2.setStyleSheet("background-color: rgb(107, 107, 107);\n"
"border-color: rgb(99, 99, 99);\n"
"")
        self.tem_rt_bar_2.setMaximum(10)
        self.tem_rt_bar_2.setProperty("value", 1)
        self.tem_rt_bar_2.setAlignment(QtCore.Qt.AlignCenter)
        self.tem_rt_bar_2.setTextVisible(True)
        self.tem_rt_bar_2.setObjectName("tem_rt_bar_2")
        self.verticalLayout_5.addWidget(self.tem_rt_bar_2)
        self.hmi_feed_enter = QtWidgets.QSpinBox(self.centralwidget)
        self.hmi_feed_enter.setGeometry(QtCore.QRect(260, 50, 91, 22))
        self.hmi_feed_enter.setStyleSheet("background-color: rgb(107, 107, 107);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.hmi_feed_enter.setMaximum(200)
        self.hmi_feed_enter.setSingleStep(5)
        self.hmi_feed_enter.setObjectName("hmi_feed_enter")
        self.hmi_temperature_enter = QtWidgets.QSpinBox(self.centralwidget)
        self.hmi_temperature_enter.setGeometry(QtCore.QRect(260, 90, 91, 22))
        self.hmi_temperature_enter.setStyleSheet("background-color: rgb(107, 107, 107);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.hmi_temperature_enter.setMinimum(200)
        self.hmi_temperature_enter.setMaximum(1600)
        self.hmi_temperature_enter.setSingleStep(5)
        self.hmi_temperature_enter.setObjectName("hmi_temperature_enter")
        self.set_feed_btn = QtWidgets.QPushButton(self.centralwidget)
        self.set_feed_btn.setGeometry(QtCore.QRect(370, 50, 81, 23))
        self.set_feed_btn.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px\n"
"")
        self.set_feed_btn.clicked.connect(self.manual_overwrite_for_feed)
        self.set_feed_btn.setObjectName("set_feed_btn")
        self.set_temp_btn = QtWidgets.QPushButton(self.centralwidget)
        self.set_temp_btn.setGeometry(QtCore.QRect(374, 90, 81, 23))
        self.set_temp_btn.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"color:  rgb(255, 137, 3);\n"
"border-radius: 15px")
        self.set_temp_btn.clicked.connect(self.manual_overwrite_for_temp)
        
        self.set_temp_btn.setObjectName("set_temp_btn")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # mqtt objects
        self.broker = 'broker.hivemq.com'
        self.port = 1883
        self.topic = "ppm/#"
        self.client = paho.Client()
        self.client.on_connect=self.on_connect_mqtt
        self.client.on_message=self.on_message_mqtt
        self.client.connect(self.broker,self.port,60)
        self.client.loop_start()
        
        
        
        
        #getdata objects and connection
        self.start = GetData()
        self.start.start()
        self.start.update_temperature.connect(self.progress_bar_1)
        self.start.update_temperature_1.connect(self.progress_bar_2)
        self.start.update_pressure.connect(self.pressure_fun)
        self.start.update_motor_1.connect(self.motor_change)
        self.start.error_emit.connect(self.notification)
        
        #data base retrive class
        self.data_class = MiniDataClass()
        base_outcome = self.data_class.data_base()
        last_feed = base_outcome[0]
        self.Feed_rate.display(last_feed)
        self.feed_time = FeedSet(last_feed,"offmessage")
        self.feed_time.start()
        self.feed_time.given_feed.connect(self.motor_change)
        base_outcome_temp = self.data_class.data_base()
        
        # temperature check object
        last_temp = base_outcome_temp[1]
        self.inductor_pid = InductionOperator(last_temp)
        self.inductor_pid.start()
        
    def on_message_mqtt(self,client,userdata,msg):
         if msg.topic == "ppm/set_feed": 
             given_feed = int(msg.payload.decode())
             self.Feed_rate.display(given_feed)
             self.feed_time = FeedSet(given_feed, "onmessage")
             self.feed_time.start()
             self.feed_time.given_feed.connect(self.motor_change)
         if msg.topic == "ppm/set_temp":
             given_temp = int(msg.payload.decode())
             self.inductor_pid.set_temp = given_temp
   
    def manual_overwrite_for_feed(self):
        last_feed = self.hmi_feed_enter.value()
        self.Feed_rate.display(last_feed)
        self.data_class.data_push_feed(last_feed)
        self.feed_time.stop()
        self.feed_time = FeedSet(last_feed, "onmessage")
        self.feed_time.start()
        
    def manual_overwrite_for_temp(self):
        last_temp = self.hmi_temperature_enter.value()
        self.inductor_pid.set_temp = last_temp
    
    def notification(self, notification_flag):
        if notification_flag==1:
            msg = QMessageBox(self.centralwidget)
            msg.setStyleSheet("background-color: rgb(18, 18, 18);\n"
            "color:  rgb(255, 137, 3);\n")
            msg.setWindowTitle("Connection Warning")
            msg.setText("Loose Connection: Please check the thermocouple Connection")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            msg.setInformativeText("Correct the connection and click 'Cancel'")
            msg.buttonClicked.connect(self.notification_flag_change)
            x = msg.exec_()
           
        
    def notification_flag_change(self,i):
        self.start.notification_flag=1
        
        
    def motor_change(self, indication):
        
        if indication == 1 :
            self.motor_1_indi.display(1)
            
            self.motor_2_indi.display(0)
        else:
            
            self.motor_1_indi.display(0)
            self.motor_2_indi.display(1)
            
            
    def progress_bar_1(self, val):
        self.tem_rt_bar.setProperty("value", val)
        self.tem_rt_bar.setFormat(f"{val}")
    
    def progress_bar_2(self, val_1):
        self.tem_rt_bar_2.setProperty("value", val_1)
        self.tem_rt_bar_2.setFormat(f"{val_1}")
    def pressure_fun(self, val_2):
        self.pressure_value.display(round(val_2, 3))
    
    def feed_indication(self, feed_val):
        self.Feed_rate.setProperty("value", feed_val)
    
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.team_name.setText(_translate("MainWindow", "PyRox Monitor"))
        self.reactor_tem.setText(_translate("MainWindow", "Reactor Tem"))
        self.catalyst_tem.setText(_translate("MainWindow", "Catalyst Tem"))
        self.motor_1.setText(_translate("MainWindow", "Convey motor"))
        self.motor_2.setText(_translate("MainWindow", "Feed motor"))
        self.reactor_induction_2.setText(_translate("MainWindow", "Induction"))
        self.pressure_label.setText(_translate("MainWindow", "Pressure"))
        self.Feed_label.setText(_translate("MainWindow", "Feed"))
        self.set_feed_btn.setText(_translate("MainWindow", "Set Feed"))
        self.set_temp_btn.setText(_translate("MainWindow", "Set Temp"))

    
    
    def on_connect_mqtt(self,client,userdata,flags,rc):
           
           self.client.subscribe(self.topic)
        
class MiniDataClass():
    def __init__(self):
        pass
    def data_base(self):
        
        fetch_feed=coll1.find_one({},{'_id':0,'set_feed':1},sort=[( '_id', pymongo.DESCENDING )])
        last_feed=int(fetch_feed["set_feed"])
        fetch_temp=coll2.find_one({},{'_id':0,'set_temp':1},sort=[( '_id', pymongo.DESCENDING )])
        last_temp=int(fetch_temp["set_temp"])
        
        return [last_feed, last_temp]
    def data_push_feed(self,given_feed):
        coll1.insert_one({"set_feed":given_feed,"on":datetime.now()})
    def data_push_temp(self,given_temp):
        coll2.insert_one({"set_temp":given_temp,"on":datetime.now()})
   
    
class GetData(QThread):
    update_temperature = pyqtSignal(float)
    update_temperature_1 = pyqtSignal(float)
    update_pressure = pyqtSignal(float)
    update_motor_1 = pyqtSignal(int)
    error_emit = pyqtSignal(int)
    
    
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.active = True
        self.notification_flag = 1
        self.pressure = idr_read.PressurePrograme()
    def run(self):
        
        while True:
            pressure = self.pressure.pressure_return()
            motor_1 = GPIO.input(6)
            motor_2 = GPIO.input(13)
            try:
                x = thermocouple.get()
                y = thermocouple_1.get()
            except:
                print(self.notification_flag)
                self.error_emit.emit(self.notification_flag)
                self.notification_flag+=1
            time.sleep(1)
            self.update_temperature.emit(x)
            self.update_temperature_1.emit(y)
            self.update_pressure.emit(pressure)
            self.update_motor_1.emit(motor_1)
        
class InductionOperator(QThread):
    def __init__(self,temp, parent = None):
        QThread.__init__(self, parent)
        self.set_temp = temp
        self.active = True
        self.x = 0
    def run(self):
        while True:
            try:
                self.x = thermocouple.get()
            except:
                pass
            print(self.set_temp)
            if self.x < self.set_temp :
                    GPIO.output(27,1)
            else:
                    GPIO.output(27,0)
    def stop(self):
        print(f"stop:{self.message}")
        self.active = False
        self.terminate()
        
        
class FeedSet(QThread):
    given_feed = pyqtSignal(float)
    def __init__(self,feed,message, parent = None):
        QThread.__init__(self, parent)
        self.feed = feed
        self.message = message
        self.active = True
    def run(self):
        time_ = self.feed * (1.2)
        while True :
            GPIO.output(26,1)
            GPIO.output(16,0)
            time.sleep(round(time_))
            GPIO.output(26,0)
            GPIO.output(16,1)
            self.given_feed.emit(0)
            time.sleep(round(time_))
            
    def stop(self):
        self.active = False
        self.terminate()
            

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())