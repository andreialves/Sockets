# Tassiana Carneiro Rios de Oliveira - 85249
# Andrei Alef de Oliveira Alves - 85280

import threading, socket, sys, pickle, time

HOST = ''       #endereço do servidor
PORT = 20000    #porta do servidor

class Server:

    user = {}
    arquivos = []
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.udp.bind((HOST, PORT))
        self.tcp.bind((HOST, PORT))
        self.tcp.listen(1)

    def chat(self, msg, endereco):
        data_string = msg.decode('utf-8')
        if data_string == "/bye":
            m = str(self.user[endereco]) + " saiu"
            print(m)
            del self.user[endereco]
            for user in self.user.keys():
                self.udp.sendto(m.encode(), user)
        elif data_string == "/list":
            m = "Clientes conectados: " + ", ".join(["%s" % v for v in self.user.values()])
            self.udp.sendto("LIST".encode(), endereco)
            self.udp.sendto(m.encode(), endereco)
        else:
            m = str(self.user[endereco]) + " disse: " + data_string
            for user in self.user.keys():
                if(user == endereco):
                    continue
                self.udp.sendto(m.encode(), user)

    def envioArq(self):
        con, cliente = self.tcp.accept()
        while True:
            try:
                info_bin = b''
                while True:
                    arq = con.recv(2048)
                    if not arq:
                        break
                    info_bin += arq
                info = pickle.loads(info_bin)
                if info['file']:
                    dest = 'files/{}'.format(info['nome'])
                    with open(dest, 'wb') as f:
                        f.write(info['file'])
                    print('success on receiving and saving {} for {}'.format(info['nome'], con.getpeername()))
                    self.arquivos.append(info['nome'])
                '''
                m = info['usuario'] + " enviou " + info['nome']
                for user in self.user.keys():
                    if (info['usuario'] in self.user):
                        continue
                    self.udp.sendto(m.encode(), user)
                '''
            except Exception as e:
                print(e)
                print(sys.exc_info())
                break
        #con.close()

    def download(self, con, cliente):
        print("Ei")

    def run(self):
        print("Aguardando conexões: ")
        while True:
            msg, endereco = self.udp.recvfrom(1024)
            if msg.decode() != '':
                a = msg.decode().split()
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
            elif a[0] == "/file":
                serverT = threading.Thread(target=self.envioArq)
                serverT.start()
            elif a[0] == "/get":
                con, cliente = self.tcp.accept()
                serverT = threading.Thread(target=self.download, args=(con, cliente))
                serverT.start()
            else:
                serverT = threading.Thread(target=self.chat, args=(msg, endereco))
                serverT.start()
            
           
servidor = Server()
servidor.run()
