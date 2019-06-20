import threading, socket, sys

HOST = ''       #endereço do servidor
PORT = 20000    #porta do servidor

class Server:

    usuarios_ativos = {}

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.udp.bind((HOST, PORT))

    def chat(self):
        while True:
            msg, endereco = self.udp.recvfrom(1024)
            data_string = msg.decode('utf-8')

            '''
            if not msg or data_string == "bye":
                m = "Cliente " + str(self.usuarios_ativos[msg]) + " desconectou"
                print(m)
                del self.usuarios_ativos[msg]
                udp.close()
                for usuarios_ativos in self.usuarios_ativos.keys():
                    usuarios_ativos.send(m.encode())
                break
            elif msg or data_string == "/list":
                m = "Clientes conectados: " + ", ".join(["%s" % v for v in self.usuarios_ativos.values()])
                endereco.send(m.encode)
            else:
            '''
            msg = str(self.usuarios_ativos[endereco]) + " disse: " + data_string
            print (msg)
            '''           
            for usuarios_ativos in self.usuarios_ativos.keys():
                if(usuarios_ativos == msg):
                    continue
                usuarios_ativos.send(msg.encode())
            '''
            self.udp.close()
            
    def run(self):
        print("Aguardando conexões: ")
        while True:
            msg, endereco = self.udp.recvfrom(1024)
            nome = msg.decode()
            serverT = threading.Thread(target=self.chat)
            serverT.start()
        
            self.usuarios_ativos[endereco] = nome
            m = str(self.usuarios_ativos[endereco]) + " entrou"
            print(m)
            '''
            for usuarios_ativos in self.usuarios_ativos.keys():
                if(usuarios_ativos == self.udp.recvfrom(1024)):
                    continue
                usuarios_ativos.send(m.encode())
            '''
        
            
servidor = Server()
servidor.run()