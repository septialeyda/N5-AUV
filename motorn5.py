import serial
import time

class motor():
    def __init__(self, port, baudrate):
        self.arduino=serial.Serial(port, baudrate)
        self.arduino.close()
        self.arduino.open()
        # self.new_condition = 'ok'
    
    # def co_serial(self, command):
    #     self.arduino.flushInput()
    #     self.arduino.write(command)
    #     self.arduino.flush()

    def send_command(self, perintah):
        self.arduino.flushInput()
        self.arduino.write(bytes(perintah,'utf-8'))
        self.arduino.flush()
        
    def send_command_serial_once(self, perintah,hasil):
        cek_ino = False
        data =""
        self.arduino.flush()
        while cek_ino == False:
            self.arduino.write(bytes(perintah,'utf-8'))
            data = self.arduino.readline().strip().decode()
            print (data)
            if data == hasil:
                cek_ino = True
        self.arduino.flush()

    def arah_config(self, arah1, arah2, arah3, arah4):
        self.dir1 = 'target ' +str(arah1)+';'
        self.dir2 = 'target ' +str(arah2)+';'
        self.dir3 = 'target ' +str(arah3)+';'
        self.dir4 = 'target ' +str(arah4)+';'
        
    def wait_result(self,result):
        check = True
        while check:
            self.arduino.flush()
            data1 = self.arduino.readline().strip().decode()
            if data1 == result:
                print (data1)
                check = False
        self.arduino.flush()

    # def target2(self, target, kedalaman):
    #     self.send_target = 'target '+str(target)+';'
    #     self.send_kedalaman = 'kedalaman'+str(kedalaman)+';'
    #     self.arduino.flush()
        # self.send_starth
        # self.send_startv


