from configparser import SectionProxy
from motorn5 import motor
from manuvercommand import manuver
import time
import imutils
import cv2
import numpy as np

try:
    arduino         = motor ('/dev/ttyACM0', 115200)
except:
    arduino         = motor ('/dev/ttyACM1', 115200)

# ------------------------------ MOTOR -----------------------------------
def arah (target_heading, next_loop):
    global sec_loop
    arduino.send_command(target_heading)
    arduino.wait_result('targetdapet')
    arduino.send_command('starth;')
    arduino.wait_result('arah_ok')
    sec_loop = next_loop
def kedalaman (depth_heading, next_loop):
    global sec_loop
    arduino.send_command(depth_heading)
    arduino.wait_result('kedalamandapet')
    arduino.send_command('startv;')
    arduino.wait_result('depthok')
    sec_loop = next_loop
def stoph():
    arduino.send_command('stoph;')
    arduino.wait_result('motorh_stop')
def next(next_loop):
    global sec_loop
    sec_loop = next_loop
def motor_h(kecepatan_h,times,next_loop):
    global sec_loop
    arduino.send_command(str('motorh '+(kecepatan_h)+';'))
    arduino.wait_result('h_jalan')
    time.sleep(times)
    stoph
    sec_loop = next_loop
    
def motor_v(kecepatan_v,times,next_loop):
    global sec_loop, stop
    arduino.send_command(str('motorv '+(kecepatan_v)+';'),'v_jalan')
    
    time.sleep(times)
    
    sec_loop = next_loop
def motor_maju(kecepatan_h):
    arduino.send_command(str('motorh '+(kecepatan_h)+';'))
    arduino.wait_result('h_jalan')
def motor_naik(kecepatan_v):
    arduino.send_command(str('motorv '+(kecepatan_v)+';'))
    arduino.wait_result('v_jalan')
def motor_nyamping(v_kiri, v_kanan):
    arduino.send_command(str('side '+(v_kiri)+' '+(v_kanan)+';'),'nyamping_ok')
# -----------------------------  KAMERA  ----------------------------------
def manuver1(red_lower,red_upper):
    arduino.camera = cv2.VideoCapture(0)
    state=0
    while True:
        ret, image = arduino.camera.read()
        image = imutils.resize(image, width=480, height=480)
        if not ret:
            break
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        merah = cv2.inRange(frame_to_thresh, (red_lower), (red_upper))
        cnts1 = cv2.findContours(merah.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        arduino.center1 = None
        # //--MERAH--//
        try:
            c1 = max(cnts1, key=cv2.contourArea)
            ((x1, y1), arduino.radius1) = cv2.minEnclosingCircle(c1)
            M1 = cv2.moments(c1)
            arduino.center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
            x_center = arduino.center1 [0]
            y_center = arduino.center1 [-1]
            if arduino.radius1 > 10:
                cv2.circle(image, (int(x1), int(y1)),
                        int(arduino.radius1), (0, 255, 255), 2)
                cv2.circle(image, arduino.center1, 5, (0, 0, 255), -1)
                if state==0:
                    if arduino.radius1<100:
                        print("Maju")
                        motor_maju(1510)
                        print(arduino.radius1)
                    else:
                        print("Berhenti")
                        stoph
                        state=1
                if state==1:
                    if x_center>20:
                        print("Strafe Kanan")
                        motor_nyamping(1610,1600)
                    else:
                        stoph
                        state=2
        except:
            arduino.radius1 = None
            arduino.center1 = None
            if state==2:
                print("Maju")
                motor_maju(1510)
                stoph
                break
        cv2.imshow("Original", image)
        if cv2.waitKey(1) & 0xFF is ord("q"):
            break
        # cv2.imshow("merah", merah)
def manuver2 (green_lower,green_upper): #Gate
    arduino.camera = cv2.VideoCapture(0)
    state=0
    while True:
        ret, image = arduino.camera.read()
        image = imutils.resize(image, width=480, height=480)
        if not ret:
            break
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hijau = cv2.inRange(frame_to_thresh, (green_lower), (green_upper))
        cnts = cv2.findContours(hijau.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        arduino.center1 = None
        arduino.center = None
        # --//Hijau//--
        try:
            c = max(cnts, key=cv2.contourArea)
            ((x2, y2), arduino.radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            arduino.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            xh_center = arduino.center [0]
            yh_center = arduino.center [-1]


            if arduino.radius > 10:
                cv2.circle(image, (int(x2), int(y2)),
                        int(arduino.radius), (0, 255, 255), 2)
                cv2.circle(image, arduino.center, 5, (0, 0, 255), -1)
                print (yh_center)
                if state==0:
                    if arduino.radius<190:
                        print("Maju")
                        motor_maju(1510)
                    if arduino.radius>190:
                        print("Berhenti")
                        stoph
                        state=1
                if state==1:
                    if xh_center<470:
                        print("Strafe Kiri")
                        motor_nyamping(1600, 1610)
                    else:
                        state=2

        except:
            arduino.radius = None
            arduino.center = None
            if state==2:
                print("Maju")
                print("Maju")
                motor_maju(1510)
                time.sleep(2), stoph
                break

        cv2.imshow("Original", image)
        if cv2.waitKey(1) & 0xFF is ord("q"):
            break
        # cv2.imshow("hijau", hijau)
        # cv2.imshow("merah", merah)
        # cv2.imshow("biru",biru)
        # cv2.imshow("kuning",kuning)
def manuver3 (yellow_lower,yellow_upper):
    arduino.camera = cv2.VideoCapture(0)
    state=0
    while True:
        ret, image = arduino.camera.read()
        image = imutils.resize(image, width=480, height=480)
        if not ret:
            break
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        kuning = cv2.inRange(frame_to_thresh, (yellow_lower), (yellow_upper))
        cnts1 = cv2.findContours(kuning.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        arduino.center1 = None
        # //--KUNING--//
        try:
            c1 = max(cnts1, key=cv2.contourArea)
            ((x1, y1), arduino.radius1) = cv2.minEnclosingCircle(c1)
            M1 = cv2.moments(c1)
            arduino.center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
            x_center = arduino.center1 [0]
            y_center = arduino.center1 [-1]
            if arduino.radius1 > 10:
                cv2.circle(image, (int(x1), int(y1)),
                        int(arduino.radius1), (0, 255, 255), 2)
                cv2.circle(image, arduino.center1, 5, (0, 0, 255), -1)
                print (arduino.radius1)
                if state==0:
                    if arduino.radius1<140:
                        print("Maju")
                        motor_maju(1520)
                    if arduino.radius1>140:
                        print("Maju_lambat")
                        motor_maju(1510)
                        state=1
                if state==1:
                    if x_center>5:
                        print("Maju_lambat")
                        motor_maju(1510)
                        break
                    else:
                        state=2
        except:
            arduino.radius1 = None
            arduino.center1 = None
            if state==2:
                print("Maju")
                motor_maju(1510)
                stoph
                break
        # cv2.imshow("Original", image)
        # if cv2.waitKey(1) & 0xFF is ord("q"):
        #     break
        # # cv2.imshow("hijau", hijau)
        # cv2.imshow("merah", kuning)
        # # cv2.imshow("biru",biru)
        # # cv2.imshow("kuning",kuning)
def manuver4 (blue_lower,blue_upper):
    arduino.camera = cv2.VideoCapture(0)
    state=0
    while True:
        ret, image = arduino.camera.read()
        image = imutils.resize(image, width=480, height=480)
        if not ret:
            break
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        kuning = cv2.inRange(frame_to_thresh, (blue_lower), (blue_upper))
        cnts1 = cv2.findContours(kuning.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        arduino.center1 = None
        # //--Biru--//
        try:
            c1 = max(cnts1, key=cv2.contourArea)
            ((x1, y1), arduino.radius1) = cv2.minEnclosingCircle(c1)
            M1 = cv2.moments(c1)
            arduino.center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
            x_center = arduino.center1 [0]
            y_center = arduino.center1 [-1]
            if arduino.radius1 > 10:
                cv2.circle(image, (int(x1), int(y1)),
                        int(arduino.radius1), (0, 255, 255), 2)
                cv2.circle(image, arduino.center1, 5, (0, 0, 255), -1)
                if state==0:
                    if x_center<250:
                        print("Belok Kiri")
                        motor_nyamping(1600,1610)
                    if x_center>250:
                        print("Belok Kanan")
                        motor_nyamping(1610,1600)
                    if y_center<220:
                        print("Maju")
                        motor_maju(1510)
                    if y_center>220:
                        print("Mundur")
                        motor_maju(1490)
                    if ((x_center>245 and x_center<255) and (y_center>215 and y_center<225)) :
                        print("Koordinat oke!")
                        stoph
                        state=1
                if state==1:
                    print("Turun")
                    motor_naik(1790)
                    time.sleep(2)
                    stoph
                    state=2
                if state==2:
                    print("Jatohin bola")
                    arduino.send_command('drop;')
                    arduino.wait_result('drop_bola')
                    break
        except:
            arduino.radius1 = None
            arduino.center1 = None
            motor_maju(1810)

        cv2.imshow("Original", image)
        if cv2.waitKey(1) & 0xFF is ord("q"):
            break
        # cv2.imshow("hijau", hijau)
        # cv2.imshow("merah", kuning)
        # cv2.imshow("biru",biru)
        # cv2.imshow("kuning",kuning)
def manuver5 (blue_lower,blue_upper):
    arduino.camera = cv2.VideoCapture(0)
    state=0

    while True:
        ret, image = arduino.camera.read()
        image = imutils.resize(image, width=480, height=480)
        if not ret:
            break
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        biru = cv2.inRange(frame_to_thresh, (blue_lower), (blue_upper))
        cnts1 = cv2.findContours(biru.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        arduino.center1 = None
        

        # //--Biru--//
        try:
            c1 = max(cnts1, key=cv2.contourArea)
            ((x1, y1), arduino.radius1) = cv2.minEnclosingCircle(c1)
            M1 = cv2.moments(c1)
            arduino.center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
            x_center = arduino.center1 [0]
            y_center = arduino.center1 [-1]


            if arduino.radius1 > 10:
                cv2.circle(image, (int(x1), int(y1)),
                        int(arduino.radius1), (0, 255, 255), 2)
                cv2.circle(image, arduino.center1, 5, (0, 0, 255), -1)                
                if state==0:
                    if x_center<250:
                        print("Belok Kiri")
                        motor_nyamping(1800,1810)
                    if x_center>250:
                        print("Belok Kanan")
                        motor_nyamping(1810,1800)
                    if y_center>30:
                        print("Maju")
                        motor_maju(1810)
                    if y_center<30:
                        print("Mundur")
                        motor_maju(1810)
                    if ((x_center>245 and x_center<255) and (y_center>25 and y_center<35)) :
                        print("Koordinat oke!")
                        stoph
                        state=1
                if state==1:
                    print("Drop manipulator")
                    arduino.send_command('buka;')
                    arduino.wait_result('buka_servo')
                    time.sleep(3)
                    state=2
                if state==2:
                    print("Turun")
                    motor_naik(1790)
                    time.sleep(2)
                    stoph
                    print("Naik_pelan")
                    motor_naik(1810)
                    time.sleep(2)
                    break

        except:
            arduino.radius1 = None
            arduino.center1 = None
        cv2.imshow("Original", image)
        if cv2.waitKey(1) & 0xFF is ord("q"):
            break
        # cv2.imshow("hijau", hijau)
        # cv2.imshow("merah", kuning)
        # cv2.imshow("biru",biru)
        # cv2.imshow("kuning",kuning)

targetarah1 = str('target '+ input('Arah 1:') + ';')
targetarah2 = str('target '+ input('Arah 2:') + ';')
targetarah3 = str('target '+ input('Arah 3:') + ';')
targetarah4 = str('target '+ input('Arah 4:') + ';')
targetarah5 = str('target '+ input('Arah 5:') + ';')
targetarah6 = str('target '+ input('Arah 6:') + ';')
depth_1 = str('kedalaman '+input('Kedalaman 1:')+';')
depth_2 = str('kedalaman '+input('Kedalaman 2:')+';')

red_lower = np.array([164,108,59])
red_upper = np.array([255,255,255])
yellow_lower = np.array([23,64,141])
yellow_upper = np.array([35,255,255])
green_lower = np.array([23,64,141])
green_upper = np.array([35,255,255])
blue_lower = np.array([23,64,141])
blue_upper = np.array([35,255,255])

main_loop = True
sec_loop = 'loop_turun1'

while main_loop:
    if sec_loop == 'loop_turun1':
        print(sec_loop)
        kedalaman(depth_1,'loop_arah1')

    if sec_loop == 'loop_arah1':
        print(sec_loop)
        arah(targetarah1,'loop_maju1')

    if sec_loop == 'loop_maju1':
        print(sec_loop)
        motor_h(1850, 5, 'loop_arah1n2')

    if sec_loop == 'loop_arah1n2':
        print(sec_loop)
        arah(targetarah2,'loop_cam1')
    
    if sec_loop == 'loop_cam1':
        print(sec_loop)
        manuver1(red_lower,red_upper)
        next('loop_arah2')        
    
    if sec_loop == 'loop_arah2':
        print(sec_loop)
        arah(targetarah2,'loop_maju2')
    
    if sec_loop == 'loop_maju2':
        print(sec_loop)
        motor_h(1850,5,'loop_arah3')
    
    if sec_loop == 'loop_arah3':
        print(sec_loop)
        arah(targetarah3,'loop_maju3')
    
    if sec_loop == 'loop_maju3':
        print(sec_loop)
        motor_h(1850,3,'loop_cam2')

    if sec_loop == 'loop_cam2':
        print(sec_loop)
        manuver3(yellow_lower,yellow_upper)
        next('loop_arah4')

    if sec_loop == 'loop_arah4':
        print(sec_loop)
        arah(targetarah4,'loop_maju4')
    
    if sec_loop == 'loop_maju4':
        print(sec_loop)
        motor_h(1850,5,'loop_arah5')

    if sec_loop == 'loop_arah5':
        print(sec_loop)
        arah(targetarah5,'loop_maju5')

    if sec_loop == 'loop_maju5':
        print(sec_loop)
        motor_h(1850,5,'loop_cam4')

    if sec_loop == 'loop_cam4':
        print(sec_loop)
        manuver4(blue_lower,blue_upper)
        motor_maju(1810), time.sleep(3), stoph
        next('loop_arah6')

    if sec_loop == 'loop_arah6':
        print(sec_loop)
        arah(targetarah6,'loop_cam5')

    if sec_loop == 'loop_cam5':
        print(sec_loop)
        manuver5(blue_lower,blue_upper)
        next('loop_naik')

    if sec_loop == 'loop_naik':
        print(sec_loop)
        motor_naik(1850)
        time.sleep(10)
        main_loop = False