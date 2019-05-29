# -*- coding: utf-8 -*-
import xmlrpc.client
import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.screen_login = master
        self.screen_login.title("Login")
        self.screen_login.geometry("300x100")
        self.pack()
        self.show_login_screen()

        try:
            self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
        except:
            print("Erro ao conectar com o servidor")

    def login(self):
        try:

            result = self.server.login(
                self.entry_username.get(), self.entry_password.get())

            self.user = result['user']

            if 'menu' in result:
                self.menu = result['menu']
                self.show_menu_screen(result['menu'])
            elif 'requests' in result:
                self.requests = result['requests']
                self.show_requests_screen(result['requests'])

        except:
            print("Erro ao efetuar o login")

    def send_request(self):
        try:

            user = self.user
            product = self.menu[self.list_menu.curselection()[0]]

            # Send the request
            result = self.server.send_request(user['id'], product['id'])

            if 'user' in result:

                # Update User
                self.user = result['user']

                # Update Balance
                balance = "Saldo: " + str(result['user']['balance'])
                self.label_balance.config(text=str(balance))

                print("Pedido efetuado com sucesso")

            else:
                print("Saldo insuficiente")

        except:
            print("Erro ao efetuar o pedido")

    def get_requests(self):
        try:

            self.list_requests.delete(0, tk.END)

            # Get the Requests
            result = self.server.get_requests()

            if result['requests']:
                # Update list
                self.requests = result['requests']
                self.update_request_list(result['requests'])

                print("Pedidos carregados com sucesso")

            else:
                print("Não existe pedidos")

        except:
            print("Erro ao buscar os pedido")

    def finish_request(self):
        try:

            if self.list_requests.curselection():

                # Finish the request
                result = self.server.finish_request(
                    self.list_requests.curselection()[0])

                # Update list
                self.get_requests()

                print("Pedido finalizado com sucesso")

            else:
                print("Selecione um pedido")

        except:
            print("Erro ao finalizar o pedido")

    def update_request_list(self, requestList):
        try:

            # Update List
            for i in range(len(requestList)):
                if requestList[i] != None:
                    self.list_requests.insert(i, str(requestList[i]['user']['name']) + " pediu 1 " + str(
                        requestList[i]['product']['name']) + ' custando R$ ' + str(requestList[i]['product']['value']))

            print("Lista de pedidos atualizada com sucesso")

        except:
            print("Erro ao atualizar a lista de pedidos")

    def show_login_screen(self):

        # Username
        self.label_username = tk.Label(self, text="Username")
        self.label_username.grid(row=1, column=1)

        self.entry_username = tk.Entry(self, textvariable=tk.StringVar())
        self.entry_username.grid(row=1, column=2)

        # Password
        self.label_password = tk.Label(self, text="Senha")
        self.label_password.grid(row=2, column=1)

        self.entry_password = tk.Entry(
            self, textvariable=tk.StringVar(), show="*")
        self.entry_password.grid(row=2, column=2)

        # Login Button
        self.button_login = tk.Button(self)
        self.button_login['text'] = 'Entrar'
        self.button_login['command'] = self.login
        self.button_login.grid(row=3, column=2)

    def show_menu_screen(self, productList):
        try:

            # Screen
            self.screen_menu = tk.Toplevel(self)
            self.screen_menu.title(str(self.user['name']) + " \ Cardápio")
            self.screen_menu.geometry("300x300")

            # List
            self.list_menu = tk.Listbox(self.screen_menu)

            for i in range(len(productList)):
                v = str(productList[i]['name']) + \
                    ' (R$ ' + str(productList[i]['value']) + ')'
                self.list_menu.insert(
                    i, v)

            self.list_menu.grid(row=1, column=1)
            self.list_menu.config(width="50")

            # Button
            self.button_send_request = tk.Button(self.screen_menu)
            self.button_send_request['text'] = 'Fazer pedido'
            self.button_send_request['command'] = self.send_request
            self.button_send_request.grid(row=2, column=1)

            # Balance
            balance = "Saldo: R$ " + str(self.user['balance'])
            self.label_balance = tk.Label(
                self.screen_menu, text=str(balance))
            self.label_balance.grid(row=3, column=1)

        except:
            print("Erro ao carregar os produtos")

    def show_requests_screen(self, requestList):
        try:

            # Screen
            self.screen_requests = tk.Toplevel(self)
            self.screen_requests.title(str(self.user['name']) + " \ Pedidos")
            self.screen_requests.geometry("300x300")
            self.list_requests = tk.Listbox(self.screen_requests)

            # List
            self.update_request_list(requestList)

            self.list_requests.grid(row=1, column=1)
            self.list_requests.config(width="50")

            # Button
            self.button_get_requests = tk.Button(self.screen_requests)
            self.button_get_requests['text'] = 'Carregar pedidos'
            self.button_get_requests['command'] = self.get_requests
            self.button_get_requests.grid(row=2, column=1)

            # Button
            self.button_finish_request = tk.Button(self.screen_requests)
            self.button_finish_request['text'] = 'Finalizar pedido'
            self.button_finish_request['command'] = self.finish_request
            self.button_finish_request.grid(row=3, column=1)

        except:
            print("Erro ao carregar os pedidos")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
