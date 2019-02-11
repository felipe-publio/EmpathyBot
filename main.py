# -*- coding: utf-8 -*-
# pip install cognitive_face
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
    try:
        KEY = ''  #Chave gerada pela MS para conexão com sua conta
        CF.Key.set(KEY)

        BASE_URL = 'https://brazilsouth.api.cognitive.microsoft.com/face/v1.0'           #URL da API Cognitive Face do Brasil
        CF.BaseUrl.set(BASE_URL)

        image = takephoto()                                                                 #Chama a função TakePhoto e Recebe a ultima imagem fotografada
        faces = CF.face.detect(image, face_id=False, landmarks=False, attributes='emotion') #Imagem é enviada para a API Congnitive Faces junto aos parametros esperados para o retorno
    
        emotion(faces)                                  #Função emotion é chamada e valor recebido pelo Azure é enviado
    except:
        print "**** ERROR - Não consegui conectar na internet!!! ****"
        os.system('aplay /home/pi/EmpathyBot/audio/internet.wav')

def emotion(faces):
    try:
        for x in faces:                                 #São separados apenas os atributos 'faceAttributes'
            emotionsCat = (x['faceAttributes'])

        for x in emotionsCat.values():                  #É gerado uma lib com as emoções e seus valores proporcionais
            emotions = x

        # x['neutral'] = 0                               #Opção para zerar o valor 'neutro'
    
        predominante = max(emotions, key=emotions.get)  #Expressão com maior valor é definida como predominante

        vozes(predominante)                             #Função vozes é chamada e valor da emoção predominante é enviado

        print '\n *****************************************************************************'
        print '\n O Resultado Geral da sua Expressão Foi: \n' 
        print  emotions           
        print '\n A expressão predominante é de: \n'                        
        print predominante
        print '\n ***************************************************************************** \n\n'

    except:
        print "**** ERROR - Não consegui identificar seu rosto!!! ****"
        os.system('aplay /home/pi/EmpathyBot/audio/error.wav')

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

def tempo(qt):

    ot = time.time()
    while(time.time() - ot < qt):  
        BrickPiUpdateValues()    
        time.sleep(.1)
            
def main():

     tempo(5)
     
     while True:
         
        tempo(1.8)
        
        if sensor_toque():
            
            print '\n Olá, Mané! Vou descobrir suas emoções!'
            os.system('aplay /home/pi/EmpathyBot/audio/hello.wav')
            
            tempo(0.6)
            
            andar(-70)
            BrickPiUpdateValues()
            
            tempo(0.8)
                
            andar(0)
            BrickPiUpdateValues()
            
            tempo(1)
            
            azure()

            andar(70)
            BrickPiUpdateValues()

            tempo(0.8)
            andar(0)
            BrickPiUpdateValues()


            
if __name__ == '__main__':

    main()
