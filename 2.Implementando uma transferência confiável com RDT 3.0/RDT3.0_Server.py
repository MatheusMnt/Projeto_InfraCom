import socket

# Configuração do servidor
HOST = "localhost"
PORT = 12000
BUFFER_SIZE = 1024

#Variáveis do RDT3.0
send_base = 0
num_seq = 0
rcv_base = 0

# Criar socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))
print(f"Servidor UDP aguardando conexões na porta {PORT}...")

def rdt_rcv():
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    msg = data.decode()
    print(f"Recebendo arquivo '{msg}' de {client_address}")
    return client_address, msg, msg[:2] #num_seq


def rdt_snd(msg, client_address):
      server_socket.sendto(msg.encode(), client_address)  
