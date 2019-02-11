# -*- coding: utf-8 -*-
# pip install cognitive_face
#

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

    def main():

        azure()
            
if __name__ == '__main__':

    main()
