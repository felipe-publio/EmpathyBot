# -*- coding: utf-8 -*-
from BrickPi import *
BrickPiSetup()
BrickPi.SensorType[PORT_4] = TYPE_SENSOR_TOUCH
BrickPi.SensorType[PORT_1] = TYPE_SENSOR_ULTRASONIC_CONT
BrickPi.MotorEnable[PORT_A] = 1
BrickPi.MotorEnable[PORT_D] = 1
BrickPiSetupSensors()

#Porta 04 - Sensor de toque
#Porta 01 - Sensor de ultrasom
#Porta A - Motor Direito
#Porta D - Motor Esquerdo

def sensor_toque():
    if BrickPi.Sensor[PORT_4] == 1:
        print "Touch Sensor = True"
        return True
    else:
        print "Touch Sensor = False"
        return False
    
    
def andar(power):
    print "Andando Para Frente."
    BrickPi.MotorSpeed[PORT_A] = power
    BrickPi.MotorSpeed[PORT_D] = power

def tempo_de_espera(tempo): #usar .15 como padrão
    time.sleep(tempo)
    
def sensor_ultrasonico():
    distancia = BrickPi.Sensor[PORT_1]
    return distancia #0 - 255 

while True:
    BrickPiUpdateValues()
    
    if sensor_toque():
        
        andar(200)
        
        ot = time.time()
        while(time.time() - ot < 3):    #running while loop for 3 seconds
            BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            time.sleep(.1)
    
        andar(0)

    
