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
            self.menu = result['menu']

            if 'menu' in result:
                self.show_menu_screen(result['menu'])
            elif 'requests' in result:
                self.show_requests_screen(result['requests'])

        except:
            print("Erro ao efetuar o login")

    def request(self):
        try:

            user = self.user
            product = self.menu[self.list_menu.curselection()[0]]

            # Envia o pedido
            result = self.server.request(user['id'], product['id'])

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
            self.screen_menu.title("Cardápio")
            self.screen_menu.geometry("300x300")

            # List
            self.list_menu = tk.Listbox(self.screen_menu)

            for i in range(len(productList)):
                v = str(productList[i]['name']) + \
                    ' (R$ ' + str(productList[i]['value']) + ')'
                self.list_menu.insert(
                    i, v)

            self.list_menu.grid(row=1, column=1)

            # Button
            self.button_request = tk.Button(self.screen_menu)
            self.button_request['text'] = 'Fazer pedido'
            self.button_request['command'] = self.request
            self.button_request.grid(row=2, column=1)

            # Balance
            balance = "Saldo: " + str(self.user['balance'])
            self.label_balance = tk.Label(
                self.screen_menu, text=str(balance))
            self.label_balance.grid(row=2, column=2)

        except:
            print("Erro ao carregar os produtos")

    def show_requests_screen(self, requestList):
        try:

            self.screen_requests = tk.Toplevel(self)
            self.screen_requests.title("Pedidos")
            self.screen_requests.geometry("300x300")
            self.list_requests = tk.Listbox(self.screen_requests)

            for i in range(len(requestList)):
                self.list_requests.insert(i, requestList[i]['user']['name'] + " pediu 1 " +
                                          requestList[i]['product']['name'] + ' | ' + requestList[i]['product']['value'])

            self.list_requests.grid(row=1, column=1)
            self.list_requests.config(width="300")

        except:
            print("Erro ao carregar os pedidos")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
