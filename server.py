# Tassiana Carneiro Rios de Oliveira - 85249
# Andrei Alef de Oliveira Alves - 85280

import threading, socket, sys, pickle, time

HOST = ''       #endereço do servidor
PORT = 20000    #porta do servidor

class Server:

    user = {}
    info = 0
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

    def envioArq(self, con, cliente):
        while True:
            try:
                info_bin = b''
                st = time.time()
                while True:
                    arq = con.recv(1024)
                    if not arq:
                        break
                    info_bin += arq
                    if time.time - st >= 2:
                        print ('bytes downloaded: ', len(info_bin))
                        st = time.time()
                info = pickle.loads(info_bin)
                if info['file']:
                    dest = 'files/{}'.format(info['name'])
                    with open(dest, 'wb') as f:
                        f.write(info['file'])
                    con.close()
            except Exception as e:
                print(e)
                break


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
                con, cliente = self.tcp.accept()
                serverT = threading.Thread(target=self.envioArq, args=(con, cliente))
                serverT.start()
            else:
                serverT = threading.Thread(target=self.chat, args=(msg, endereco))
                serverT.start()
            
           
servidor = Server()
servidor.run()
