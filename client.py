import socket, threading

HOST = "127.0.0.1"      #Endereço ip do Servidor
PORT = 20000            #Porta do Servidor´

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
'''
def chat(udp):
    while True:
        msg, cliente = udp.recvfrom(1024)
        data_string = msg.decode()
        if not msg:
            break
        print(str(cliente)+": " +data_string)
'''
msg = input('Nome do Usuário: ')
while msg != 'bye':
    udp.sendto(msg.encode(), (HOST, PORT))
    msg = input()
#clientT = threading.Thread(target=chat, args=(udp, ))
#clientT.start()


udp.close()