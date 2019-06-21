import socket, threading, sys

HOST = "127.0.0.1"      #Endereço ip do Servidor
PORT = 20000            #Porta do Servidor´

class Client:
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def __init__(self, usuario):
        self.udp.sendto(usuario.encode(), (HOST, PORT))
        try:
            msg, serv = self.udp.recvfrom(1024)
            if (msg.decode('utf-8') != "ACK"):
                print("Servidor indisponível no momento.")
                sys.exit()
        except:
            print("Servidor não encontrado.")        
            sys.exit()
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
            print(data_string)
    
    def chat(self):
        while True:
            msg = input()
            self.udp.sendto(msg.encode(), (HOST, PORT))
            if msg == "/bye":
                self.udp.close()
                break

usr = input('Nome do Usuário: ')
cliente = Client(usr)
