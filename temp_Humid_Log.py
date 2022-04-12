# imports
from time import sleep, strftime, time
import serial
import sys, os


ser = serial.Serial('COM4', 115200, timeout=20)  # sets active serial port and baud rate, CHANGE to desired port

ser.readline()
ser.readline()
ser.readline()  # pulls out board acknowledgement inputs

fileName = "sensorData.csv"
filePath = os.getcwd().replace('\\', '/') + '/' + fileName
# filePath = "C:/Users/Erik Porter/Desktop/SensorCode/humidity.csv"

errCount = 0  # counts how many errors have been thrown
threshold = 10  # stops program if too many errors are thrown
with open(filePath, "a") as log:    
  print('><><><><><><><><><><><><><><><')
  print('>---COLLECTING SENSOR DATA---<')
  print('><><><><><><><><><><><><><><><')
  print('Writing Data To: ' + filePath)
  while errCount < threshold:
    try:
      # ensures data is being collected in correct order, throws assertion error otherwise
      t = ser.readline()
      assert str(t)[2:13] == 'Temperature'

      h = ser.readline()
      assert str(h)[2:10] == 'Humidity'

      p = ser.readline()
      assert str(p)[2:10] == 'Pressure'

      temp = float(str(t).lstrip("b'Temperature: ").rstrip("\\r\\n'"))
      humidity = float(str(h).lstrip("b'Humidity: ").rstrip("\\r\\n'"))
      press = float(str(p).lstrip("b'Pressure: ").rstrip("\\r\\n'"))

      print(f"Temperature: {temp}")
      print(f"Humidity: {humidity}")
      print(f"Pressure: {press}")
      log.write("{0},{1},{2},{3}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp), str(humidity), str(press)))
    except (ValueError, AssertionError) as e:
      print(e)
      errCount += 1
      pass

  ser.close()     
    
