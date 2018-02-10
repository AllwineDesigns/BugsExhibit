from serial import Serial

ser = Serial('/dev/ttyACM0', 9600);

ser.write(bytearray([255,0,0,1, 4, 0, 5 ]))
