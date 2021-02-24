# Tommi Kunnari 23.2.2021

import threading
import socket

host = '127.0.0.1' # Running the server on localhost

port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # We're using the TCP protocol.

server.bind((host, port))

server.listen()

users = []

usernames = []

def global_msg(msg): # A simple broadcast message for all clients.
    for i in users:
        i.send(msg)

def handle_user(user): # Handles user sent messages.
    while True:

        try:    # If receiving a message...
            msg = user.recv(1024)
            clean = msg.decode('utf-8')
            clean_list = clean.split(":")

            if (clean_list[1][1:4] == "/w "): # The message has the /w tag, send private message
                target = clean_list[1].split(" ")
                index = usernames.index(target[2])
                rec_user = users[index]
                clean = ""

                for i in target[3:]:
                    clean = (clean + " " + i)
                private = ("(private) " + clean_list[0] + ":" + clean).encode('utf-8')

                private_msg(rec_user, private)
            else:                        # Else broadcast
                global_msg(msg)

        except: # If the user disconnects, terminate the connection.
            index = users.index(user)
            users.remove(user)
            user.close()
            username = usernames[index]
            global_msg(f'{username} left the chat'.encode('utf-8'))
            usernames.remove(username)
            break

def receive():  # Receive new connections/users
    while True:
        user, address = server.accept()
        print(f"Connected with {str(address)}")
        user.send("NAME".encode('utf-8'))
        username = user.recv(1024).decode('utf-8')
        usernames.append(username)
        users.append(user)
        print(f"Clients' username: {username}")
        global_msg(f"{username} joined the chatroom.".encode('utf-8'))
        user.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_user, args=(user,))
        thread.start()

def private_msg(user, msg): # Send a message to a specific user.
    user.send(msg)

print("Server started")
receive()