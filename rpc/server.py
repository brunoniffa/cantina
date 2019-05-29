# -*- coding: utf-8 -*-
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from models.User import User
from models.Request import Request
from models.Product import Product


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


users = [
    User(0, 'Rafael Cruz', 'rafael', '123', 100.00),
    User(1, 'Bruno', 'bruno', '456', 50.00),
    User(2, 'Atendente 01', 'atendente', '111', 0)
]

menu = [
    Product(0, 'Pão', 10),
    Product(1, 'Vinho', 20)
]

requests = []


# Create server
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def login(username, password):
        for user in users:
            if username == user.username and password == user.password:
                if str(username) == str('atendente'):
                    return {'requests': requests, 'user': user}
                else:
                    return {'menu': menu, 'user': user}

        return {'erro': ''}

    def send_request(userIndex, productIndex):
        try:

            if users[userIndex].balance >= menu[productIndex].value:

                users[userIndex].balance = users[userIndex].balance - \
                    menu[productIndex].value

                requests.append(
                    Request(len(requests), users[userIndex], menu[productIndex]))

                return {'user': users[userIndex]}

            return {'erro': ''}

        except:
            print("Erro ao inserir um pedido")

    def get_requests():
        try:

            return {'requests': requests}

        except:
            print("Erro ao devolver os pedidos")

    def finish_request(requestIndex):
        try:

            if requests[requestIndex] in requests:
                requests.pop(requestIndex)
                print("Sucesso ao dar baixa no pedido")
                return {'requests': requests}

            return {'erro': ''}

        except:
            print("Erro ao dar baixa no pedido")

    server.register_function(login)
    server.register_function(send_request)
    server.register_function(get_requests)
    server.register_function(finish_request)

    print('Start server on port:8000')
    server.serve_forever()
