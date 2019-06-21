import threading, socket, sys

HOST = ''       #endereço do servidor
PORT = 20000    #porta do servidor

class Server:

    user = {}

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.udp.bind((HOST, PORT))

    def chat(self, msg, endereco):
        data_string = msg.decode('utf-8')
        if data_string == "/bye":
            m = "Cliente " + str(self.user[endereco]) + " desconectou"
            print(m)
            del self.user[endereco]
            for user in self.user.keys():
                self.udp.sendto(m.encode(), user)
        elif data_string == "/list":
            m = "Clientes conectados: " + ", ".join(["%s" % v for v in self.user.values()])
            self.udp.sendto(m.encode(), endereco)
        else:
            m = str(self.user[endereco]) + " disse: " + data_string
            for user in self.user.keys():
                if(user == endereco):
                    continue
                self.udp.sendto(m.encode(), user)
            
            
    def run(self):
        print("Aguardando conexões: ")
        while True:
            msg, endereco = self.udp.recvfrom(1024)
            if endereco not in self.user:
                nome = msg.decode()
                self.user[endereco] = nome
                self.udp.sendto("ACK".encode(), endereco)
                m = str(self.user[endereco]) + " entrou" 
                print(m)
                for user in self.user.keys():
                    if(user == endereco):
                        continue
                    self.udp.sendto(m.encode(), user)
            else:
                serverT = threading.Thread(target=self.chat, args=(msg, endereco))
                serverT.start()
            
           
            
            
            
servidor = Server()
servidor.run()