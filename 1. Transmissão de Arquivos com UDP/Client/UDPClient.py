import socket
import os

serverName = "localhost"
serverPort = 12000
buffer_size = 1024
path = "../Files/"

print("Digite o nome do arquivo:")
for file in os.listdir(path):
    print("- " + file)
filename = input()  # Nome do arquivo que será enviado

# Criar socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enviar nome do arquivo primeiro
client_socket.sendto(filename.encode(), (serverName, serverPort))

# Abrir e enviar arquivo
with open(path+filename, "rb") as file:
    while chunk := file.read(buffer_size):
        client_socket.sendto(chunk, (serverName, serverPort))

# Indicar fim da transmissão
client_socket.sendto(b"EOF", (serverName, serverPort))

# Diretório para salvar o arquivo modificado
new_path = "../ModifiedFiles/" 

# Receber novo nome e arquivo de volta
new_filename, _ = client_socket.recvfrom(buffer_size)
new_filename = new_filename.decode()

# Cria diretório de arquivos modificados se não existir
if not os.path.exists(new_path): 
    os.mkdir(new_path)

# Receber arquivo modificado
with open(new_path+new_filename, "wb") as file:
    while True:
        data, _ = client_socket.recvfrom(buffer_size)
        if data == b"EOF":
            break
        file.write(data)

print(f"Arquivo '{new_filename}' recebido com sucesso!")