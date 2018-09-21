# Author : Mr.Nontachai  Yoothai

import sys, os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import cv2
import numpy as np
import requests, json
import base64
import json
import operator
import microgear.client as client
import time
import random
import string
import math

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.IN) # Button Capture
GPIO.setup(6, GPIO.OUT) # LED RED
GPIO.setup(5, GPIO.OUT) # LED YELLOW
GPIO.setup(21, GPIO.OUT) # LED GREEN
GPIO.setup(13, GPIO.OUT) # Buzzer

qtCreatorFile = "/home/pi/peas1/skill-contest/main_final_new.ui"  # Enter file here.
#qtCreatorFile = "/home/pea/Desktop/skill-contest/main_final.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Sensor:
        def __init__(self):
            # self.gpio = GPIO
            self.delay = 2

        def pressed(self):
            status = GPIO.input(26)
            
            if status:
                return True
            else:
                return False
            
        def led(self, status):
            # print("Action LED")
            if status:
                GPIO.output(21,True)
                GPIO.output(6,False)
            else:
                GPIO.output(6,True)
                GPIO.output(21,False)

        def buzzer(self, mode):
            print("Action Buzzer")
            period = 1.0/650.0
            delay = period/4
            cycle = int(0.1*650.0)
            if mode :
                for i in range(cycle):
                    GPIO.output(13, True)
                    time.sleep(delay)
                    GPIO.output(13, False)
                    time.sleep(delay)
                    GPIO.output(13, True)
                    time.sleep(delay)
                    GPIO.output(13, False)
                    time.sleep(delay)
                time.sleep(0.5)
                for i in range(cycle):
                    GPIO.output(13, True)
                    time.sleep(delay)
                    GPIO.output(13, False)
                    time.sleep(delay)
                    GPIO.output(13, True)
                    time.sleep(delay)
                    GPIO.output(13, False)
                    time.sleep(delay)
            else:
                period = 1.0/650.0
                delay = period/4
                cycle = int(0.4*650.0)
                for i in range(cycle):
                    GPIO.output(13, True)
                    time.sleep(delay)
                    GPIO.output(13, False)
                    time.sleep(delay)
                    GPIO.output(13, True)
                    time.sleep(delay)
                    GPIO.output(13, False)
                    time.sleep(delay)


class Capture:
        def __init__(self, parent):
            self.capturing = False
            self.c = cv2.VideoCapture(0)
            self.frame = None
            self.live_flag = None
            
            self.sensor = Sensor()
            self.parent = parent

        def startCapture(self):
            print "pressed start"
            # self.MyApp.Live.start(500)
            # self.MyApp.Live.start(500)

            self.capturing = True
            cap = self.c
            while self.capturing:
                ret, frame = cap.read()
                frame = cv2.resize(frame, (431, 281))
		if self.live_flag:
                    cv2.imshow("Capture", frame)
                else:
                    cv2.destroyWindow("Capture")
		    pass
                # cv2.rectangle(frame, (215, 200), (480, 400), (255, 0, 0), 2)
                self.frame = frame
		cv2.waitKey(1)
                #flag = self.sensor.pressed() # TODO : Uncomment
                #if not flag:
                #    print("Capture from sensor")
                #    self.parent.snap_handler()

                    # self.endCapture()
                #cv2.imwrite('~/peas1/skill-contest/live.png', cv2.resize(self.frame, (431, 281)), [cv2.IMWRITE_PNG_COMPRESSION, 9])
            cv2.destroyAllWindows()

        def endCapture(self):
            print "pressed End"
            os.system('rm -rf /tmp/live.png')
            self.capturing = False
            self.c.release()
            cv2.destroyAllWindows()

        def quitCapture(self):
            print "pressed Quit"
            self.capturing = False
            cap = self.c
            cv2.destroyAllWindows()
            cap.release()
            QtCore.QCoreApplication.quit()


class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.peano_flag =None
        self.sensor = Sensor()
        self.setupUi(self)
        self.config = None
        self.capture = Capture(self)
        self.fileDiag = QFileDialog()
        self.img_path = None
        self.live_flag = None
        # self.thread_2 = self.v2_sl.value()
        # self.thread_1 = self.v1_sl.value()
        # self.tableWidget.setColumnCount(3)
        # self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()

        self.start_cam_btn.clicked.connect(self.capture.startCapture)
        self.stop_cam_btn.clicked.connect(self.capture.endCapture)
        self.snap_btn.clicked.connect(self.snap_handler)
        self.exit_btn.clicked.connect(exit_handler)
        self.pick_btn.clicked.connect(self.get_file)
        self.detect_btn.clicked.connect(self.detect_api)
        self.detect_btn.setDisabled(True)
        # self.v1_sl.valueChanged.connect(self.v1_changed)
        # self.v2_sl.valueChanged.connect(self.v2_changed)

        # self.measure_btn.clicked.connect(self.measure)
        # self.count_btn.clicked.connect(self.count)

        self.circle_radio.toggled.connect(lambda: self.btnstate(self.circle_radio))
        self.unknow_radio.toggled.connect(lambda: self.btnstate(self.unknow_radio))
        self.livepreview.toggled.connect(lambda: self.btnstate(self.livepreview))
        self.peano_chk.toggled.connect(lambda: self.btnstate(self.peano_chk))


        self.object_type = None

        self.label.setAutoFillBackground(True)
        self.label.setText("Wait for Connection ..")
        self.label.setStyleSheet('color: blue')

        self.Timer = QTimer()
        #self.Timer.timeout.connect(self.check_status)
        #self.Timer.start(5000)

        self.gearkey = 'liLGrIH0WZdAKT0'  # key
        self.gearsecret = 'OfFLXs2NlqL3ecjkaClXhEUli'  # secret
        self.appid = 'ImageRaspi'
        #try: # TODO : Uncomment if need netpie.
        #    client.create(self.gearkey, self.gearsecret, self.appid, {'debugmode': True})
        #    client.on_connect = self.callback_connect
        #    client.setalias("doraemon")
        #    client.on_message = self.callback_message
        #    client.on_error = self.callback_error
        #    client.subscribe("/mails")
        #    client.connect()
        #except Exception as e:
        #    pass
        
    def callback_error(self):
        print("Error Netpie")

    def callback_connect(self):
        print("Now I am connected with netpie")

    def callback_message(topic, message):
        print("Incoming")
        pass

    def check_status(self):
        try:
            res = requests.get('http://www.google.com')
            if res.status_code == 200:
                # print res.status_code
                self.label.setText("STATUS : CONNECTED")
                self.label.setStyleSheet('color: green')
                self.sensor.led(status=True)
            else:
                # print res.status_code
                self.label.setText("STATUS : DISCONNECTED")
                self.label.setStyleSheet('color: red')
                self.sensor.led(status=True)

        except Exception as Err:
            self.label.setText("STATUS : DISCONNECTED")
            self.label.setStyleSheet('color: red')
            self.sensor.led(status=False)
            pass

    def rest_call(self, img):
        print("Prediction")

        url = self.config.get("Url")
        body = img
        headers = self.config.get("Header")

        response = requests.request("POST", url, data=body, headers=headers)
        print(response.status_code)
        print('Debug')
        # TODO : Utilize Response Here.
        if response.status_code == 200:
            self.sensor.buzzer(mode=True)
        else:
            self.sensor.buzzer(mode=False)
        result = json.loads(response.content)
        predictions = result.get('predictions')  # prediction is a List of Dict.
        # Try to drop less prob.
        output = []
        for pred in predictions:
            if int(pred.get('probability')*100) >= 85:
                output.append(pred)
        # Try to count object that found in images
        tmp = []
        for tag in output:
            tmp.append(tag.get('tagName'))
        found = set(tmp)  # Now known how many type of found.
        detect = {}
        box =[]
        for f in found:
            box = []
            for i in output:
                if f == i.get('tagName'):
                    box.append(i.get('boundingBox'))
            detect.update({f: box})
            del box

        if self.peano_flag :
            print("Detect PEANO")

            # TODO : Do stuff OCR HERE
            try:
                res = requests.post(
                    url="https://southeastasia.api.cognitive.microsoft.com/vision/v2.0/ocr",
                    params={
                        "language": "unk",
                        "detectOrientation ": "true",
                    },
                    headers={
                        "Content-Type": "application/octet-stream",
                        "Ocp-Apim-Subscription-Key": "03c4947c97f0483dbd4e53e8984fad10",
                    },
                    data=body
                )
                print('Response HTTP Status Code: {status_code}'.format(
                    status_code=response.status_code))
                print('Response HTTP Response Body: {content}'.format(
                    content=response.content))
                peano= json.loads(res.content)
                self.peano = peano.get('regions')[0].get('lines')[0].get('words')[0].get('text')

            except requests.exceptions.RequestException:
                print('HTTP Request failed')

        else:
            self.peano = None

        self.plotBox(detect)
        self.update_table(info=detect, peano=self.peano)

    def rest_call_2(self, img):
        print("Prediction")

        url = self.config.get("Url")
        body = img
        headers = self.config.get("Header")

        response = requests.request("POST", url, data=body, headers=headers)
        print(response.status_code)
        print('Debug')
        # TODO : Utilize Response Here.
        if response.status_code == 200:
            self.sensor.buzzer(mode=True)
        else:
            self.sensor.buzzer(mode=False)
        result = json.loads(response.content)
        print("Debug")
        score_0 = result.get("predictions")[0]
        score_1 = result.get("predictions")[1]
        if score_0.get('probability') >= score_1.get('probability'):
            # label_result = score_0.get("tagName")
            # confident = score_0.get("probability")
            info = {score_0.get("tagName"): score_0.get("probability")}
        else:
            # label_result = score_1.get("tagName")
            # confident = score_1.get("probability")
            info = {score_1.get("tagName"): score_1.get("probability")}
        self.update_table_2(info=info)

    def update_table_2(self, info): # TODO : Argent Require

        horHeaders = ['Prediction', 'Confident (%)']

        ind = 0
        # self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(info.keys()))
        self.tableWidget.setColumnWidth(0, 400)
        self.tableWidget.setColumnWidth(1, 142)


        for k, v in info.items():
            KeyItem = QTableWidgetItem(k)
            ValItem = QTableWidgetItem(str(v*100))
            self.tableWidget.setItem(ind, 0, KeyItem)
            self.tableWidget.setItem(ind, 1, ValItem)
            ind += 1
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)
        # TODO : Stuff for netpie

        client.publish('/risk', str(v*100))
        client.publish('/risk_lb', str(k))
        filestuff = self.img_tmp
        img = str(filestuff[0])
        with open(img,'rb') as img_file :
            encoded_string = base64.b64encode(img_file.read())
        img_file.close()
        str_img = str('<center><img src="data:image/png;base64,' + encoded_string.decode(
            'utf-8') + '" width="300" height="300"/><center>')
        client.publish('/snap', str_img)


    def update_table(self, info, peano= '99-999999'): # TODO : Argent Require

        horHeaders = ['Device-Type', 'UNIT', 'PEANO']

        ind = 0
        # self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(info.keys()))
        self.tableWidget.setColumnWidth(0, 320)
        self.tableWidget.setColumnWidth(1, 142)
        self.tableWidget.setColumnWidth(2, 160)

        for k, v in info.items():
            KeyItem = QTableWidgetItem(k)
            ValItem = QTableWidgetItem(str(len(v)))
            PEAItem = QTableWidgetItem(str(peano))
            self.tableWidget.setItem(ind, 0, KeyItem)
            self.tableWidget.setItem(ind, 1, ValItem)
            self.tableWidget.setItem(ind, 2, PEAItem)
            ind += 1
        self.tableWidget.setHorizontalHeaderLabels(horHeaders)

        #for numRow in range(len(info.keys())):
        #     for key, val in info.items():
        #         newitem = QTableWidgetItem(key)
        #         self.tableWidget.setItem(0, 1, newitem)
        #         newitem = QTableWidgetItem(len(val))
        #         self.tableWidget.setItem(1, 1, newitem)

    def plotBox(self, info):
        frame = cv2.imread(str(self.img_path))
        for item in info.keys():
            print("Found : Number of {0} = {1}".format(item, len(info.get(item))))
            for box in info.get(item):

                x1 = int(320*box.get('left'))
                y1 = int(240*box.get('top'))
                x2 = x1 + int(320*box.get('width'))
                y2 = y1 + int(240*box.get('height'))

                cv2.rectangle(frame, (x1,y1), (x2,y2), (0, 128, 250), 2)
            cv2.imwrite('./output/result.png', frame)
            image = QtGui.QImage(QtGui.QImageReader("./output/result.png").read())
            self.result_lb.setPixmap(QtGui.QPixmap(image))
            self.result_lb.show()

    def detect_api(self):
        print("Detect by API")
        if self.object_type == "Transformer":
            self.config = None
            self.config = json.load(open("./config_1.json", 'r'))
            self.rest_call(open(str(self.img_path), 'rb').read())  # Call Function rest_call by passing BinaryByte
            # of Image

        elif self.object_type == "Patrol":
            self.config = None
            self.config = json.load(open("./config_2.json", 'r'))
            self.rest_call_2(open(str(self.img_path), 'rb').read())

    def btnstate(self, b):  # For handle State of Radio Button Selected
        # TODO : remove print()
        if b.text() == "Transformer":
            if b.isChecked():
                print b.text() + " is selected"
                self.object_type = "Transformer"
                self.detect_btn.setEnabled(True)
        if b.text() == "Patrol":
            if b.isChecked():
                print b.text() + " is selected"
                self.object_type = "Patrol"
                self.detect_btn.setEnabled(True)
        if b.text() == "Live Preview":
            if b.isChecked():
                print b.text() + " is Checked"
                self.capture.live_flag = True
            else:
                print "Not Check"
                self.capture.live_flag = False
        if b.text() == "PEANO":
            if b.isChecked():
                print b.text() + " is Checked"
                self.peano_flag = True
            else:
                print "Not Check"
                self.peano_flag = False

    def get_file(self):  # Function Handle on OpenDialog Button.

        self.fileDiag.setFileMode(QFileDialog.AnyFile)
        # self.fileDiag.setFilter("Image files (*.png,*.jpg)")
        filenames = QStringList()
        if self.fileDiag.exec_():  # Check File Dialog Choosing
            filenames = self.fileDiag.selectedFiles()
            self.img_tmp = filenames
            tmp = cv2.imread(str(filenames[0]))
            tmp = cv2.resize(tmp, (320, 240))
            cv2.imwrite(str(filenames[0]), tmp)  # Open Resize and Replace file
            img = QtGui.QImage(QtGui.QImageReader(filenames[0]).read())
            self.origin_lb.setPixmap(QtGui.QPixmap(img))
            self.origin_lb.show()
            self.img_path = filenames[0]

    def snap_handler(self): # Capture Function
        print("Button Clicked")
        resize = cv2.resize(self.capture.frame, (320, 240))
        cv2.imwrite('./output/snap.png', resize)
        self.img_path = './output/snap.png'
        self.capture.capturing = False
        cv2.destroyAllWindows()
        self.capture.c.release()
        self.capture.endCapture()
        image = QtGui.QImage(QtGui.QImageReader("./output/snap.png").read())
        self.origin_lb.setPixmap(QtGui.QPixmap(image))
        self.origin_lb.show()



# Static Method for Handle Exit Task.
def exit_handler():
    print("Terminate by User !!!")
    exit()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
