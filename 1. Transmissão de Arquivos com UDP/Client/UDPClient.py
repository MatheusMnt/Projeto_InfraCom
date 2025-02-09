import socket
from os import listdir

server_IP = "localhost"  # Substitua pelo IP do servidor
serverPort = 12000
buffer_size = 1024
path = "../Files/"

print("Digite o nome do arquivo:")
for file in listdir(path):
    print("- " + file)
filename = input()  # Nome do arquivo que será enviado

# Criar socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enviar nome do arquivo primeiro
client_socket.sendto(filename.encode(), (server_IP, serverPort))

# Abrir e enviar arquivo
with open(path+filename, "rb") as file:
    while chunk := file.read(buffer_size):
        client_socket.sendto(chunk, (server_IP, serverPort))

# Indicar fim da transmissão
client_socket.sendto(b"EOF", (server_IP, serverPort))

# Receber novo nome e arquivo de volta
new_path = "../ModifiedFiles/" # Diretório para salvar o arquivo modificado
new_filename, _ = client_socket.recvfrom(buffer_size)
new_filename = new_filename.decode()

with open(new_path+new_filename, "wb") as file:
    while True:
        data, _ = client_socket.recvfrom(buffer_size)
        if data == b"EOF":
            break
        file.write(data)

print(f"Arquivo '{new_filename}' recebido com sucesso!")