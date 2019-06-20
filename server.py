import threading, socket, sys

HOST = ''       #endereço do servidor
PORT = 20000    #porta do servidor

class Server:

    usuarios_ativos = {}

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.udp.bind((HOST, PORT))

    def chat(self, msg, endereco):
        data_string = msg.decode('utf-8')
        if data_string == "/bye":
            m = "Cliente " + str(self.usuarios_ativos[endereco]) + " desconectou"
            print(m)
            del self.usuarios_ativos[endereco]
            self.udp.close()
            for usuarios_ativos in self.usuarios_ativos.keys():
                self.udp.sendto(m.encode(), usuarios_ativos)
        elif data_string == "/list":
            m = "Clientes conectados: " + ", ".join(["%s" % v for v in self.usuarios_ativos.values()])
            self.udp.sendto(m.encode(), endereco)
        else:
            m = str(self.usuarios_ativos[endereco]) + " disse: " + data_string
            for usuarios_ativos in self.usuarios_ativos.keys():
                if(usuarios_ativos == endereco):
                    continue
                self.udp.sendto(m.encode(), usuarios_ativos)
            
            
    def run(self):
        print("Aguardando conexões: ")
        while True:
            msg, endereco = self.udp.recvfrom(1024)
            if endereco not in self.usuarios_ativos:
                nome = msg.decode()
                self.usuarios_ativos[endereco] = nome
                m = str(self.usuarios_ativos[endereco]) + " entrou" 
                print(m)
            serverT = threading.Thread(target=self.chat, args=(msg, endereco))
            serverT.start()
            '''
            for usuarios_ativos in self.usuarios_ativos.keys():
                if(usuarios_ativos == endereco):
                    continue
                self.udp.sendto(m.encode(), usuarios_ativos)
            '''
            
            
servidor = Server()
servidor.run()