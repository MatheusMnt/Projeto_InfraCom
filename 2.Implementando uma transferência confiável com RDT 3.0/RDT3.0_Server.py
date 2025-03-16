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
    global num_seq, rcv_base, send_base, client_address
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    msg = data.decode()
    print(f"Recebendo arquivo '{msg}' de {client_address}")
    return msg

def rdt_snd(msg, client_address):
      server_socket.sendto(msg.encode(), client_address)  

def state0():
    global num_seq, send_base, rcv_base, client_address
    rcv_msg = rdt_rcv() 
    # se a mensagem não é a esperada, reenvia o ACK
    if rcv_msg[:2] != rcv_base:
       ACK0 = str(num_seq).zfill(2) + str(rcv_base).zfill(2)
       rdt_snd(ACK0, client_address)
    else:
      #TODO implementar o deliver(data)
      rcv_base+=1
      num_seq+=1
      ACK1 = str(num_seq).zfill(2) + str(rcv_base).zfill(2)
      rdt_snd(ACK1, client_address)

def state1():
    global num_seq, send_base, rcv_base, client_address
    rcv_msg = rdt_rcv()
    # se a mensagem não é a esperada, reenvia o ACK
    if rcv_msg[:2] != rcv_base:
         ACK1 = str(num_seq).zfill(2) + str(rcv_base).zfill(2)
         rdt_snd(ACK1, client_address)
    else:
      #TODO implementar o deliver(data)
      rcv_base-=1
      num_seq-=1
      ACK0 = str(num_seq).zfill(2) + str(rcv_base).zfill(2)
      rdt_snd(ACK0, client_address)

