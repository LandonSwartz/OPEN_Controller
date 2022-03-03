# serial communicator test

try:
    from Util.Serial_Communicator_Class import Serial_Communicator
    from time import sleep
    import sys
except ImportError:
    print("failure to import")
    
ser_com = Serial_Communicator('/dev/ttyACM0', '50060')
sleep(2)
ser_com.Send('$H\n')
while True:
    read = ser_com.Read()
    if read:
        sleep(0.5)
        ser_com.Send('$H\n')
