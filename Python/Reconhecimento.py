#RECONHECIMENTO FACIAL

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pymssql

def ReconhecimentoFacial():
    path= 'Outros/imagem'  #CRIAÇÃO VAR DE CONTROLO.
    fotos=[]
    classNomes=[]
    myList=os.listdir(path)

    for cl in myList:
        imgAtual=cv2.imread(f'{path}/{cl}') #VAI AO PATH DAS IMAGENS E COMEÇA A LER AS IMAGENS, BEM COMO A ATRIBUIR NOMES
        fotos.append(imgAtual)              #A CADA UMA DE ACORDO COM A SUA DESCRIÇÃO.
        classNomes.append(os.path.splitext(cl)[0])
    print("\nNOMES PRESENTES NA BASE DE DADOS") #APRESENTA NA CONSOLA OS NOMES PARA CONTROLO
    print (classNomes)

    def descobrir(fotos):
        encodeLista=[]
        for img in fotos:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #CADA IMAGEM PRESENTE VAI SER CONVERTIDA DE BGR TO RGB
            encode = face_recognition.face_encodings(img)[0]   #A BIBLIOTECA CV2 FAZ O ENCODE DE CADA IMAGEM
            encodeLista.append(encode)  #FAZ O APPEND À LISTA DAS IMAGENS.
        return encodeLista

    def arquivar(nome):
        with open('Outros/Arquivo.csv', 'r+') as f:
            myDataList=f.readline()
            nameList= []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if nome not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{nome},{dtString}')

    encodeListaConhecidos=descobrir(fotos)
    print ("\nCODIFICAÇÃO COMPLETA") # INFORMAR QUE COMPLETOU COM SUCESSO A ATRIBUIÇÃO DE CADA IMAGEM AO NOME DA PESSOA

    cap = cv2.VideoCapture(0) #INICIAL WEBCAM PREDEFENIDA PELA PC. NO CASO DE TER 2, PODE HAVER ERRO.

    print("PRONTO A RECEBER CARAS")
    login="" #VAR DE CONTROLO PARA LOG IN NA DB
    while True:
        sucess, img=cap.read()  #FAZ UM CAPTURE DA IMAGEM PELA WEBCAM
        imgS=cv2.resize(img,(0,0),None,0.25,0.25)   #DIVIDE A IMAGEM POR 4,
        imgS= cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) #CONVERTE A IMAGEM QUE RECEBE DE BGR PARA RGB

        faceWebcam = face_recognition.face_locations(imgS)
        encodeWebcam = face_recognition.face_encodings(imgS,faceWebcam) # FAZ O ENCONDE DA IMEGEM DA WEBCAM
        controlo = True # VARIAVEL DE CONTROLO
        for encodeFace,faceLoc in zip(encodeWebcam,faceWebcam): #VE AS IMAGENS QUE TEM E COMPARA COM WEBCAM,
            iguais = face_recognition.compare_faces(encodeListaConhecidos,encodeFace)
            faceDis = face_recognition.face_distance(encodeListaConhecidos,encodeFace)
            iguaisIndex = np.argmin(faceDis)

            if iguais[iguaisIndex]: #CASO O INDICE SEJA SEMELHANTE INDICA IMAGEM IGUAL À PRESENTE NO PATH
                nome = classNomes[iguaisIndex].upper() #METE O NOME DA IMAGEM EM UPPER
                login = classNomes[iguaisIndex].upper() #VAR CONTROLO COM O MESMO NOME
                y1,x2,y2,x1=faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4 #FAZ UM REZISE DO QUADRADO PARA A IMAGEM QUE O USER VE.
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2) #RECTANGULO, CORES, FONTS
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,nome,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                arquivar(nome)
                controlo = False
        cv2.imshow('Webcam',img)
        cv2.waitKey(1)
        if controlo==True: #CASO NAO RECONHEÇA, A WEBCAM ESTA SEMPRE ABERTA ATE FECHAR O PROGRAMA.
            continue
        elif controlo==False:
            cv2.destroyAllWindows() #DESTROI A IMAGEM E PEGA NO NOME EM LOGIN PARA ENTRAR NA DB
            break
    if (login !=""): #ESCOLHE A PESSOA COM BASE NA IMAGEM
        if (login =="RICARDO"):
            Entrar("Ricardo")
        elif (login =="PEDRO"):
            Entrar("Pedro")
        elif (login =="FILIPE"):
            Entrar ("Filipe")
        elif (login =="LUIZ"):
            Entrar ("Luiz")
        elif (login =="FERNANDO"):
            Entrar ("Fernando")

def Entrar(x): #FAZ O LOG IN ESPECIFICO
    if (x=="Ricardo"):
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81750', '81750', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        nome=x
        cursor.execute('SELECT * FROM Marcas')
        for x in cursor:
            print(x)
        mydb.close()
    elif (x=="Pedro"):
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81817', '81817', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        nome = x
    elif (x=="Filipe"):
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81818', '81818', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
        nome = x
    elif (x=="Luiz"):
        mydb = pymssql.connect('srvsql-ipt.ddns.net', '81810', '81810', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
    elif (x=="Fernando"):
        nome = x
        mydb = pymssql.connect('srvsql-ipt.ddns.net', 'sa', 'P.1234567', "PA_81750_81810_81817_81818")
        cursor = mydb.cursor(as_dict=True)
