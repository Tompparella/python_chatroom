# Tommi Kunnari 23.2.2021

import threading
import socket

host = '127.0.0.1' # The server's ip and port
port = 5000

username = input("Username: ")

print("Welcome!\nSimply type a message to broadcast, or use the form '/w username message' for private messages.\nHave fun!")

user = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # We're using the TCP protocol.

user.connect((host, port))

def receive():
    while True:
        try:
            msg = user.recv(1024).decode('utf-8')
            if msg == "NAME":
                user.send(username.encode('utf-8'))
                pass
            else:
                print(msg)
        except:
            print("Error with the connction.")
            user.close()
            break

def write_msg():
    while True:
        msg = f'{username}: {input("")}'
        user.send(msg.encode('utf-8'))

r_thread = threading.Thread(target=receive)
r_thread.start()

w_thread = threading.Thread(target=write_msg)
w_thread.start()

