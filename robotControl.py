import serial
import pyfirmata
from time import sleep
s = serial.Serial("com3",9600)
s2 = serial.Serial("com4",9600)
class RobotControl(object):            
    def MoveLeg(LF,RF,LB,RB):
        moveleg = "MoveLeg" + "," + str(LF) + "," + str(RF) + "," + str(LB) + "," + str(RB) +"\n"
        moveleg = str.encode(moveleg)
        s.write(moveleg)
        
    def getDistance():
        s.write(b'getDistance\n')
        message = s.readline()
        message = str(message, encoding = "utf-8")
        message = message.replace('\r\n', '')
        return message
        
    def getLegStatus():
        s.write(b'getLegStatus\n')
        message = s.readline()
        message = str(message, encoding = "utf-8")
        LF,RF,LB,RB = message.split(",",4)
        LF = LF.replace('\r\n', '')
        RF = RF.replace('\r\n', '')
        LB = LB.replace('\r\n', '')
        RB = RB.replace('\r\n', '')
        return LF,RF,LB,RB
    def resetLeg():
        s.write(b'reset\n')

    def reset():
        s2.write(b'reset\n')
        
    def start():
        s2.write(b'start\n')
