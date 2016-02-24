#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 15, 2016

import socket
import sys

IP = socket.gethostbyname(socket.gethostname())
SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        self.__clientlist= []
        self.__IPlist= []
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                reqst= self._receive(client)
                sent = reqst.decode()
                print('Sent:', sent)
                #database = self._clientlist()
                #print('DataBase):', database)
                #cIP = database[sent].encode()
                #print('CorresIP:', cIP, 'Type:', type(cIP))
                #msg= 'Hello'
                #client.send(msg.encode())
                print('cIP sent!')
                client.send(reqst)
                client.close()
                sys.exit()
            except OSError:
                print('Erreur lors de la réception du message.')
    
    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            client.settimeout(3)
            try:
                data = client.recv(32)
            except:
                data= b''
                print('Timeout')
                pass
            print(data)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)

    def _clientlist(self):
        if SERVERADDRESS[0] not in self.__clientlist:
            self.__clientlist[:]= [SERVERADDRESS[0]]
            print('ClientList:', self.__clientlist[:])
            self.__IPlist[:] = [IP]
            print('IPList:', self.__IPlist[:])
            database= {self.__clientlist[i]: self.__IPlist[i] for i in range(0, len(self.__clientlist))}
            return database


class EchoClient():
    def __init__(self, IPrequest):
        self.__request = IPrequest
        print('IPrequest:', IPrequest)
        self.__s = socket.socket()
    
    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
            self._send(self.__request)
            self._receive()
        except OSError:
            print('Serveur introuvable, connexion impossible.')
        self.__s.close()
    
    def _send(self, sentdata):
        totalsent = 0
        rqs = sentdata
        try:
            while totalsent < len(rqs):
                print('Send Loop')
                sent = self.__s.send(rqs[totalsent:])
                totalsent += sent
        except OSError:
            print("Erreur lors de l'envoi du message.")

    def _receive(self):
        chunks = []
        finished = False
        print('Start')
        while not finished:
            print('Loop')
            data = self.__s.recv(512)
            print('Data:', data.decode())
            chunks.append(data)
            finished = data == b''
        print(b''.join(chunks).decode())

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        EchoServer().run()
    #elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        #EchoClient(sys.argv[2].encode()).run()
    elif len(sys.argv) == 2 and sys.argv[1] == 'client':
        choice = input('Choose!\n\t1. request someone\'s IP\n\t2. Check out the database\n\t3. Change your username\n\t4. Block contact')
        print(choice)
        print(choice == '1')
        if choice == '1':
            name = input('Dude\'s name please')
            EchoClient(name.encode()).run()
        elif choice == '2':
            password = input('Password?')
            if password == 'echo1234':
                pass
        elif choice == '3':
            username = input('Username ?')
            pass
        elif choice == '4':
            block = input('Contact to block ?')
            pass
        else:
            print('Unknown command')
        
