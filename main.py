# -*- coding: utf-8 -*-
# pip install cognitive_face
#
# **************************
# https://brazilsouth.api.cognitive.microsoft.com/face/v1.0
# 7b111ef8ee564500afb07f87fe402f7b
# **************************
#

from BrickPi import *
BrickPiSetup()
BrickPi.SensorType[PORT_4] = TYPE_SENSOR_TOUCH
BrickPi.MotorEnable[PORT_A] = 1
BrickPi.MotorEnable[PORT_D] = 1
BrickPiSetupSensors()
import os
import cognitive_face as CF
import picamera
	
def takephoto():                        #Função que realiza a fotografia e retorna imagem
    camera = picamera.PiCamera()       
    camera.capture('image.jpg')         #Inicia câmera e salva arquivo como 'image.jpg'
    camera.close()                      #Fechamos a câmera 
    captura = open('image.jpg','r')     #A fotografia é atribuida a variavel captura 
    return captura                      #Retorna ultima imagem capturada

def azure():                                                                             #Função Responsavel pela conexão com o MicrosoftAzure
    KEY = '7b111ef8ee564500afb07f87fe402f7b'                                             #Chave gerada pela MS para conexão com sua conta
    CF.Key.set(KEY)

    BASE_URL = 'https://brazilsouth.api.cognitive.microsoft.com/face/v1.0'               #URL da API Cognitive Face do Brasil
    CF.BaseUrl.set(BASE_URL)

    image = takephoto()                                                                 #Chama a função TakePhoto e Recebe a ultima imagem fotografada
    faces = CF.face.detect(image, face_id=False, landmarks=False, attributes='emotion') #Imagem é enviada para a API Congnitive Faces junto aos parametros esperados para o retorno

    emotion(faces)                                  #Função emotion é chamada e valor recebido pelo Azure é enviado


def emotion(faces):
    try:
        for x in faces:                                 #São separados apenas os atributos 'faceAttributes'
            emotionsCat = (x['faceAttributes'])

        for x in emotionsCat.values():                  #É gerado uma lib com as emoções e seus valores proporcionais
            emotions = x
    except:
        print "This is an error message!"    

   # x['neutral'] = 0                               #Opção para zerar o valor 'neutro'
    
    predominante = max(emotions, key=emotions.get)  #Expressão com maior valor é definida como predominante

    vozes(predominante)                             #Função vozes é chamada e valor da emoção predominante é enviado

    print '***************************************************************************************'
    print 'O Resultado Geral da sua Expressão Foi: ' 
    print  emotions           
    print 'A expressão predominante é de: '                        
    print predominante
    print '*************************************************************************************** \n\n\n\n\n\n'

def vozes(predominante):                            #Com o valor da emoção predominante recebido o audio com a conrrespodente será executado
    if   predominante == 'anger':
        os.system('aplay /home/pi/EmpathyBot/audio/anger.wav')

    elif predominante == 'contempt':
        os.system('aplay /home/pi/EmpathyBot/audio/contempt.wav')

    elif predominante == 'disgust':
        os.system('aplay /home/pi/EmpathyBot/audio/disgust.wav')

    elif predominante == 'fear':
        os.system('aplay /home/pi/EmpathyBot/audio/fear.wav')

    elif predominante == 'happiness':
        os.system('aplay /home/pi/EmpathyBot/audio/happiness.wav')

    elif predominante == 'neutral':
        os.system('aplay /home/pi/EmpathyBot/audio/neutral.wav')

    elif predominante == 'sadness':
        os.system('aplay /home/pi/EmpathyBot/audio/sadness.wav')

    elif predominante == 'surprise':
        os.system('aplay /home/pi/EmpathyBot/audio/surprise.wav')

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
    
def main():

     while True:
         
        ot = time.time()
        while(time.time() - ot < 3):    #running while loop for 3 seconds
            BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
            time.sleep(.1)
    
        if sensor_toque():

            andar(150)
            BrickPiUpdateValues()
            os.system('aplay /home/pi/EmpathyBot/audio/hello.wav')
            andar(0)
            BrickPiUpdateValues()
            azure()
            
            
if __name__ == '__main__':

    main()
