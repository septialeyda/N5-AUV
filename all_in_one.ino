#include <Wire.h>
#include "Timer.h"
#include "Command.h"
#include "Motor.h"
#include "Motor2.h"
#include "LiquidCrystal_I2C.h"
#include "MS5837.h"

LiquidCrystal_I2C lcd(0x3F, 16, 2);
Timer motor_time, check_time, kedalaman_time, lcd_timer, servo_time, kedalaman_timer;
Command cmd;
Motor motor2(2);
Motor motor3(6);
Motor2 motor4(4);
Motor2 motor5(5);
Motor motor6(7);
Motor motor7(3);

Servo servo1, servo2;
MS5837 sensor;
int pos1, pos2, pos3, da, y, cmps, depth_now, rpi;
int pwm_motor2 = 1500;
int new_pwm_motor2 = 1500;
int pwm_motor3 = 1500;
int new_pwm_motor3 = 1500;
int pwm_motor4 = 1800;
int new_pwm_motor4 = 1800;
int pwm_motor5 = 1800;
int new_pwm_motor5 = 1800;
int pwm_motor6 = 1500;
int new_pwm_motor6 = 1500;
int pwm_motor7 = 1500;
int new_pwm_motor7 = 1500;
int pwm_motorh = 1500;
int new_pwm_motorh = 1500;
int pwm_motorv = 1800;
int new_pwm_motorv = 1800;
int pwm_motorkanan = 1500;
int new_pwm_motorkanan = 1500;
int pwm_motorkiri = 1500;
int new_pwm_motorkiri = 1500;

void setup()
{
  Serial.begin(115200);
  servo1.attach(8);
  servo2.attach(9);
  lcd.init();
  lcd.backlight();
  Wire.begin();
  lcd.clear();
  motor_set_deadzone();
}

void loop()
{
  cmd.get();
  DoEverything(cmd);
  tulis();
  if (lcd_timer.elapsed(1000)) {
    lcd.clear();
  }
  sensor_kedalaman();
  kondisi_kedalaman();
  kontrol_motor();
  servoo();
}

void sensor_kedalaman() {

  while (!sensor.init()) {
    Serial.println("Init failed!");
    Serial.println("Are SDA/SCL connected correctly?");
    Serial.println("Blue Robotics Bar30: White=SDA, Green=SCL");
    Serial.println("\n\n\n");
    delay(5000);
  }
  if (kedalaman_timer.elapsed(100)) {
    sensor.read();
  }
}

void motor_set_deadzone() {
  motor2.motor_deadzone_negative = 50;
  motor2.motor_deadzone_positive = 50;
  motor3.motor_deadzone_negative = 50;
  motor3.motor_deadzone_positive = 50;
  motor4.motor2_deadzone_negative = 50;
  motor4.motor2_deadzone_positive = 50;
  motor5.motor2_deadzone_negative = 50;
  motor5.motor2_deadzone_positive = 50;
  motor6.motor_deadzone_negative = 50;
  motor6.motor_deadzone_positive = 50;
  motor7.motor_deadzone_negative = 50;
  motor7.motor_deadzone_positive = 50;

  motor2.reset();
  motor3.reset();
  motor4.reset();
  motor5.reset();
  motor6.reset();
  motor7.reset();

  motor2.goms(MIDPOINT);
  motor3.goms(MIDPOINT);
  motor4.goms2(MIDPOINT);
  motor5.goms2(MIDPOINT);
  motor6.goms(MIDPOINT);
  motor7.goms(MIDPOINT);
  delay(600);

  motor2.goms(1500);
  motor3.goms(1500);
  motor4.goms2(1800);
  motor5.goms2(1800);
  motor6.goms(1500);
  motor7.goms(1500);
  delay(600);
}

void kontrol_motor() {
  if (pwm_motor2 != new_pwm_motor2 ) {
    pwm_motor2 = new_pwm_motor2;
    motor2.goms(pwm_motor2);
  }
  if (pwm_motor3 != new_pwm_motor3 ) {
    pwm_motor3 = new_pwm_motor3;
    motor3.goms(pwm_motor3);
  }
  if (pwm_motor4 != new_pwm_motor4 ) {
    pwm_motor4 = new_pwm_motor4;
    motor4.goms2(pwm_motor4);
  }
  if (pwm_motor5 != new_pwm_motor5 ) {
    pwm_motor5 = new_pwm_motor5;
    motor5.goms2(pwm_motor5);
  }
  if (pwm_motor6 != new_pwm_motor6 ) {
    pwm_motor6 = new_pwm_motor6;
    motor6.goms(pwm_motor6);
  }
  if (pwm_motor7 != new_pwm_motor7 ) {
    pwm_motor7 = new_pwm_motor7;
    motor7.goms(pwm_motor7);
  }
  //  if (pwm_motorv != new_pwm_motorv ) {
  //    pwm_motorv = new_pwm_motorv;
  //    motor4.goms2(pwm_motorv);
  //    motor5.goms2(pwm_motorv);
  //  }
}

void DoEverything(Command command) {
  if (command.cmp("go")) {
    new_pwm_motor2 = int(command.args[1]);
    new_pwm_motor3 = int(command.args[2]);
    new_pwm_motor6 = int(command.args[3]);
    new_pwm_motor7 = int(command.args[4]);
    Serial.print(new_pwm_motor2);
    Serial.print(" ");
    Serial.print(new_pwm_motor3);
    Serial.print(" ");
    Serial.print(new_pwm_motor6);
    Serial.print(" ");
    Serial.println (new_pwm_motor7);
    Serial.println("motorh_nyala");
  }

  if (command.cmp("motorv")) {
    new_pwm_motor4 = int(command.args[1]);
    new_pwm_motor5 = int(command.args[2]);
    Serial.print(new_pwm_motor4);
    Serial.print(" ");
    Serial.print(new_pwm_motor5);
    Serial.println("motorv_nyala");
  }

  if (command.cmp("stop")) {
    new_pwm_motor2 = 1500;
    new_pwm_motor3 = 1500;
    new_pwm_motor4 = 1800;
    new_pwm_motor5 = 1800;
    new_pwm_motor6 = 1500;
    new_pwm_motor7 = 1500;
    new_pwm_motorh = 1500;
    new_pwm_motorv = 1800;
    new_pwm_motorkanan = 1500;
    new_pwm_motorkiri = 1500;
    Serial.println("stop");
  }

  if (command.cmp("stoph")) {
    new_pwm_motor2 = 1500;
    new_pwm_motor3 = 1500;
    new_pwm_motor6 = 1500;
    new_pwm_motor7 = 1500;
    new_pwm_motorh = 1500;
    Serial.println("motorh_stop");
  }

  if (command.cmp("stopv")) {
    new_pwm_motor4 = 1800;
    new_pwm_motor5 = 1800;
    new_pwm_motorv = 1800;
    Serial.println("motorv_stop");
  }

  if (command.cmp("da")) {
    da = bool(command.args[1]);
    Serial.println(da);
  }

  if (command.cmp("dt")) {
    y = int(command.args[1]);
    Serial.println(y);
    Serial.println("target_accepted");
  }

  if (command.cmp("compass")) {
    cmps = int(command.args[1]);
    Serial.println(cmps);
    Serial.println("compass_accepted");
  }

  if (command.cmp("servo1")) {
    pos1 = int(command.args[1]);
    Serial.println(pos1);
    Serial.println("servo1_nyala");
  }
  if (command.cmp("servo2")) {
    pos2 = int(command.args[1]);
    Serial.println(pos2);
    Serial.println("servo2_nyala");
  }
  if (command.cmp("rpi")) {
    rpi = bool(command.args[1]);
  }
}

void tulis() {
  depth_now = (sensor.depth() * 100);
  if (pwm_motor2 > 1500 && pwm_motor3 > 1500 && pwm_motor6 > 1500 && pwm_motor7 > 1500) {
    lcd.setCursor(9, 0);
    lcd.print("Maju");
  }
  if (pwm_motor2 < 1500 && pwm_motor3 < 1500 && pwm_motor6 < 1500 && pwm_motor7 < 1500) {
    lcd.setCursor(9, 0);
    lcd.print("Mundur");
  }
  if (pwm_motorv > 1800) {
    lcd.setCursor(9, 0);
    lcd.print("Turun");
    Serial.print(depth_now);
  }
  if (pwm_motorv < 1800) {
    lcd.setCursor(9, 0);
    lcd.print("Naik");
    Serial.print(depth_now);
  }
  if (pwm_motor2 > 1500 && pwm_motor3 < 1500 && pwm_motor6 > 1500 && pwm_motor7 < 1500) {
    lcd.setCursor(9, 0);
    lcd.print("Kiri");
  }
  if (pwm_motor2 < 1500 && pwm_motor3 > 1500 && pwm_motor6 < 1500 && pwm_motor7 > 1500) {
    lcd.setCursor(9, 0);
    lcd.print("Kanan");
  }
  if (pwm_motorv == 1800 && pwm_motor2 == 1500 && pwm_motor3 == 1500 && pwm_motor6 == 1500 && pwm_motor7 == 1500) {
    lcd.setCursor(9, 0);
    lcd.print("Diam");
  }
  lcd.setCursor(9, 1);
  lcd.print(depth_now);
  lcd.setCursor(1, 0);
  lcd.print("N5-AUV");
  lcd.setCursor(1, 1);
  lcd.print(cmps);
}

void servoo() {
  servo1.write(pos1);
  servo2.write(pos2);
}

void kondisi_kedalaman() {
  depth_now = (sensor.depth() * 100);
  if (da == 1) {
    if (y > depth_now) {
      new_pwm_motor4 = 1800;
      new_pwm_motor5 = 1800;
      new_pwm_motor4 = 1830;
      new_pwm_motor5 = 1830;
      Serial.println("adjusting");
    }
    else if (y < depth_now) {
      new_pwm_motor4 = 1800;
      new_pwm_motor5 = 1800;
      new_pwm_motor4 = 1790;
      new_pwm_motor5 = 1790;
      Serial.println("adjusting");
    }
    else if (y == (depth_now + 2) && y == (depth_now - 2)) {
      new_pwm_motor4 = 1800;
      new_pwm_motor5 = 1800;
      Serial.println("depth_ok");
    }
  }
}
