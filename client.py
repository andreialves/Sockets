# Tassiana Carneiro Rios de Oliveira - 85249
# Andrei Alef de Oliveira Alves - 85280

import socket, threading, sys, pickle
from datetime import datetime

HOST = "127.0.0.1"      #Endereço ip do Servidor
PORT = 20000            #Porta do Servidor´

class Client:
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log = []
    user = ''
    
    def __init__(self, usuario):
        self.udp.sendto(usuario.encode(), (HOST, PORT))
        self.user = usuario
        cThread = threading.Thread(target=self.chat)
        cThread.start()

        while True:
            try:
                msg, serv = self.udp.recvfrom(1024)
            except:
                break
            data_string = msg.decode('utf-8')
            if not msg:
                break
            if (data_string == "ACK"):
                self.log.append("Log: " + str(datetime.now()) + " - ACK")
            elif (data_string == "LIST"):
                self.log.append("Log: " + str(datetime.now()) + " - LIST")
            elif (data_string ==  "BYE"):
                self.log.append("Log: " + str(data_string.now()) + " - BYE")
            else:
                print(data_string)
    
    def chat(self):
        while True:
            msg = input()
            self.udp.sendto(msg.encode(), (HOST, PORT))
            
            if msg.count('/file') == 1:
                #Melhorar isso aqui ou só testar na abertura
                if len(msg) < 11 and msg.count('.') != 1:
                    print("Especifique um nome válido para o arquivo")
                else:
                    varqName = msg.split()                   
                    try:
                        arq = open(str(varqName[1]), 'rb')
                        info = {'nome': str(varqName[1]), 'file': arq.read(), 'opcao': 1, 'usuario': self.user}
                    except:
                        print("Arquivo inválido, tente novamente")
                    
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((HOST, PORT))
                            s.sendall(pickle.dumps(info))
                            s.close()
                        arq.close()

                    except:
                        print (sys.exc_info())
            elif msg.count('/get') == 1:
                if len(msg) < 10 and msg.count('.') != 1:
                    print("Especifique um nome válido para o arquivo")
                else:
                    print("OI")

            if msg == "/log":
                print (self.log)

            if msg == "/bye":
                self.udp.close()
                break

usr = input('Nome do Usuário: ')
cliente = Client(usr)