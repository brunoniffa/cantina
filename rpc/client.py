# -*- coding: utf-8 -*-
import xmlrpc.client
import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.server = xmlrpc.client.ServerProxy('http://localhost:8000')

        self.screen_login = master
        self.screen_login.title("Login")
        self.screen_login.geometry("300x100")
        self.pack()
        self.show_login_screen()

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

        # Login
        self.button_login = tk.Button(self)
        self.button_login['text'] = 'Entrar'
        self.button_login['command'] = self.login
        self.button_login.grid(row=3, column=2)

    def login(self):
        result = self.server.login(self.entry_username.get(),
                                   self.entry_password.get())

        if 'menu' in result:
            self.show_menu_screen(result['menu'])
        elif 'requests' in result:
            self.show_requests_screen(result['requests'])

    def show_menu_screen(self, list):
        self.screen_menu = tk.Toplevel(self)
        self.screen_menu.title("Cardápio")
        self.screen_menu.geometry("300x300")
        self.menu = tk.Listbox(self.screen_menu)

        for i in range(len(list)):
            self.menu.insert(i, list[i])

        self.menu.grid(row=4, column=1)

    def show_requests_screen(self, list):
        self.screen_requests = tk.Toplevel(self)
        self.screen_requests.title("Pedidos")
        self.screen_requests.geometry("300x300")
        self.requests = tk.Listbox(self.screen_requests)

        for i in range(len(list)):
            self.requests.insert(i, list[i])

        self.requests.grid(row=4, column=1)


root = tk.Tk()
app = Application(master=root)
app.mainloop()
