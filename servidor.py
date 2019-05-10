
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s conectou." % client_address)
        client.send(bytes("Seja bem-vindo(a) à Cantina!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Bem-vindo %s! Para sair da tela de pedidos, digite {quit}.' % name
    client.send(bytes(welcome, "utf8"))

    #msg = "%s ingressou no terminal!" % name
    #broadcast(bytes(msg, "utf8"))
    #clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            #broadcast(bytes("%s desconectou do terminal." % name, "utf8"))
            break

def broadcast(msg, prefix=""):  # prefix is for name identification.

    # Mensagem para todos os clients
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

clients = {}
addresses = {}

HOST = 'localhost'
PORT = 33334
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Aguardando por pedidos...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()