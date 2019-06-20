import socket, threading

HOST = "127.0.0.1"      #Endereço ip do Servidor
PORT = 20000            #Porta do Servidor´

class Client:
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    def __init__(self, usuario):
        self.udp.sendto(usuario.encode(), (HOST, PORT))
        cThread = threading.Thread(target=self.chat)
        cThread.start()
        while True:
            try:
                msg, serv = self.udp.recvfrom(1024)
            except:
                print("Aconteceu alguma coisa.")
            data_string = msg.decode('utf-8')
            if not msg:
                break
            print(data_string)
    
    def chat(self):
        while True:
            msg = input()
            self.udp.sendto(msg.encode(), (HOST, PORT))

usr = input('Nome do Usuário: ')
cliente = Client(usr)
