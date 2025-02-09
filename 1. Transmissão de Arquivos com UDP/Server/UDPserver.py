import socket

# Configuração do servidor
HOST = "localhost"
PORT = 12000
BUFFER_SIZE = 1024

# Criar socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Servidor UDP aguardando conexões na porta {PORT}...")

while True:
    # Receber dados do cliente
    data, client_address = server_socket.recvfrom(BUFFER_SIZE)
    filename = data.decode()  # Nome do arquivo enviado
    print(f"Recebendo arquivo '{filename}' de {client_address}")

    # Criar e abrir arquivo para escrita
    with open("servidor_" + filename, "wb") as file:
        while True:
            data, _ = server_socket.recvfrom(BUFFER_SIZE)
            if data == b"EOF":  # Verifica se o cliente terminou de enviar
                break
            file.write(data)

    print(f"Arquivo '{filename}' salvo no servidor.")

    # Modificar nome e enviar de volta
    new_filename = "modificado_" + filename
    with open("servidor_" + filename, "rb") as file:
        server_socket.sendto(new_filename.encode(), client_address)  # Enviar novo nome
        while chunk := file.read(BUFFER_SIZE):
            server_socket.sendto(chunk, client_address)
        server_socket.sendto(b"EOF", client_address)  # Indicar fim da transmissão

    print(f"Arquivo '{new_filename}' enviado de volta para {client_address}\n")
