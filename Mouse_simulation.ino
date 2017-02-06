#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
//#include <Mouse.h>

String data = "";
MPU6050 mpu;

int ax, ay, az;
int gx, gy, gz;
int x,y;

int angleToDistance(int a)
{
  if      (a < -80) return -40;
  else if (a < -65) return -20;
  else if (a < -50) return -10;
  else if (a < -15) return -5;
  else if (a < -5)  return -1;
  else if (a > 80)  return 40;
  else if (a > 65)  return 20;
  else if (a > 50)  return 10;
  else if (a > 15)  return 5;
  else if (a > 5)   return 1;
  else              return 0;
}

void setup()
{
  Serial.begin(9600);
  Wire.begin();
  //Mouse.begin();
  mpu.initialize();
  if (!mpu.testConnection())
  {
    while (1);
  }
}
void loop()
{
  //if (digitalRead(2) == LOW).
  //{
    data = "";
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    x = angleToDistance(map(gx, -16000, 16000, -90, 90));
    y = angleToDistance(map(gy, -16000, 16000, -90, 90));

    data += x;
    data += " ";
    data += y;
    Serial.println(data);
    //Mouse.move(x,y);
  //}
}

