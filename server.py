#!/bin/python3
import socket
import threading


class Client:
    def __init__(self, client, addr, nick):
        self.client = client
        self.address = addr
        self.nickname = nick


# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.client.send(message)


# Sending private message to client with special nickname
def private(nickname, message):
    for client in clients:
        if nickname == client.nickname:
            client.client.send(message.encode('utf8'))


# Handling Messages From Clients
def handle(client):
    global nickname
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            msg_arr = str(message).split(" ")
            print(msg_arr)
            nick = msg_arr[1]
            if nick in nicknames:
                print(msg_arr[0])
                msg_arr[0] = msg_arr[0][2:]
                print(msg_arr[0])
                print(msg_arr[-1])
                msg_arr[-1] = msg_arr[-1][:-1]
                print(msg_arr[-1])
                msg_arr.remove(nick)
                print(msg_arr)
                msg = ' '.join(msg_arr)
                print(msg)
                private(nick, "private from " + str(msg))
            else:
                broadcast(message)
        except:
            # Removing And Closing Clients
            for cl in clients:
                if cl.client == client:
                    nickname = cl.nickname
                    clients.remove(cl)
            client.close()

            broadcast('{} left!'.format(nickname).encode('utf8'))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf8'))
        nickname = client.recv(1024).decode('utf8')
        nicknames.append(nickname)
        client = Client(client, address, nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf8'))
        client.client.send('Connected to server!'.encode('utf8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client.client,))
        thread.start()


print("Server if listening...")
receive()
