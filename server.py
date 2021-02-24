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

channels = []

def global_msg(msg, index): # A simple broadcast message for all clients.
    channel = channels[index]
    for i in users:
        u_index = users.index(i)
        if (channels[u_index] == channel):    # Check if user is in the same channel.
            try:
                i.send(msg)
            except:
                print("An error occurred.")
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
                index = users.index(user)
                global_msg(msg, index)

        except: # If the user disconnects, terminate the connection.
            index = users.index(user)
            users.remove(user)
            user.close()
            username = usernames[index]
            global_msg(f'{username} left the chat'.encode('utf-8'), index)
            usernames.remove(username)
            break

def receive():  # Receive new connections/users
    while True:

        user, address = server.accept()
        print(f"Connected with {str(address)}")
        user.send("NAME".encode('utf-8'))
        username = user.recv(1024).decode('utf-8')

        channel = user.recv(1024).decode('utf-8')
        channels.append(channel)
        usernames.append(username)
        users.append(user)
        print(f"Clients' username: {username}\nchannel: {channel}")

        global_msg(f"{username} joined the {channel} chatchannel.".encode('utf-8'), users.index(user))
        user.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_user, args=(user,))
        thread.start()

def private_msg(user, msg): # Send a message to a specific user.
    try:
        user.send(msg)
    except:
        print("An error occurred.")

print("Server started")
receive()