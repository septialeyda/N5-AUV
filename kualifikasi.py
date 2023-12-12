from motorn5 import motor
import time

try:
    arduino = motor('/dev/ttyACM0', 115200)
except:
    arduino = motor('/dev/ttyACM1', 115200)

targetarah1 = str('target '+ input('Target Arah 1:') + ';')
#targetarah2 = str('target '+ input('Target Arah 2:') + ';')
# targetarah3 = str('target '+ input('Target Arah 3:') + ';')
depth_1 = str('kedalaman '+input('Kedalaman 1:')+';')
#depth_2 = str('kedalaman '+input('Kedalaman 2:')+';')
motorh1 = str('motorh '+input('power maju 1:')+';')

main_loop = True
sec_loop = 'loop_turun'

while main_loop:
    if sec_loop == 'loop_turun':
        print (sec_loop)
        arduino.send_command_serial_once(depth_1, "depthok")
        sec_loop = 'loop_maju1'
    
    if sec_loop == 'loop_maju1':
        print (sec_loop)
        arduino.send_command(targetarah1)
        arduino.wait_result("arahok")
        sec_loop = 'loop_maju'
        
    if sec_loop == 'loop_maju':
        arduino.send_command(motorh1)
        time.sleep(2)
        sec_loop = 'loop_naik'
        
    if sec_loop == 'loop_naik':
        print(sec_loop)
        arduino.send_command('stoph;')
        arduino.send_command('motorv 1620;')
        print('Sudah Naik :)')
        time.sleep(3)
        arduino.send_command('kill;')
        main_loop = False




