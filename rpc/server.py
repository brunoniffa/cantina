# -*- coding: utf-8 -*-
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password


users = [
    User('rafael', '123'),
    User('bruno', '456'),
    User('atendente', '000')
]

menu = [
    'Pão',
    'Vinho'
]

requests = [
    'Pedido 1'
]

# Create server
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def login(username, password):

        for user in users:
            if username == user.username and password == user.password:
                if username == 'atendente':
                    return {'requests': requests}
                else:
                    return {'menu': menu}

        return {'erro': ''}

    server.register_function(login)

    print('Start server...')
    server.serve_forever()
