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
        self.__addr = ''
        self.__clientlist = []
        self.__namelist = []
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            self.__addr = addr[0]
            print('addr:', self.__addr)
            self._clientlist()
            try:
                print('Connected by:', addr)
                reqst= self._receive(client)
                sent = reqst
                print('Sent:', sent)
                #database = self._clientlist()
                #print('DataBase):', database)
                #cIP = database[sent].encode()
                #print('CorresIP:', cIP, 'Type:', type(cIP))
                #msg= 'Hello'
                #client.send(msg.encode())
                print('cIP sent!')
                client.send(reqst.encode())
                client.close()
                sys.exit()
            except OSError:
                print('Erreur lors de la récepti[on du message.')
    
    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            client.settimeout(2)
            try:
                data = client.recv(32)
            except:
                data= b''
                print('Timeout')
                pass
            print(data)
            chunks.append(data)
            finished = data == b''
        bpp = b''.join(chunks).decode()[4:] #Les 4 premières lettres servent a identifier le type de requète
        code =b''.join(chunks).decode()[:4]
        print('Code:', code)
        return bpp
 
    def _clientlist(self):
        try:
            with open('database.txt', 'r') as file:
                datbase = file.read()
                print('datbase:', datbase)
        except:
            datbase= []
        if self.__addr not in datbase:
            self.__clientlist += [self.__addr]
            print('ClientList:', self.__clientlist)
            name = socket.gethostbyaddr(self.__addr)
            print('Name:', name)
            self.__namelist += [name]
            maxi = len(self.__clientlist)
            dbse = {self.__clientlist[i] : [self.__clientlist[i], self.__namelist[i]] for i in range(0, maxi)}
            with open('database.txt', 'w') as file:
                file.write(str(dbse))
            #return database


class EchoClient():
    def __init__(self, IPrequest, choice):
        self.__request = IPrequest
        self.__s = socket.socket()
        self.__choice = choice
    
    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
        except OSError:
            print('Serveur introuvable, connexion impossible.')
        self._routechoice(self.__request, self.__choice)
        self._receive()
        self.__s.close()

    def _routechoice(self, var, choice):
        if choice == '1':
            self._send('send', var)
        elif choice == '2':
            self._datbase('dtbs', var)
        elif choice == '3':
            self._username('user', var)
        elif choice == '4':
            self._block('blck', var)
        else:
            print('error')
    
    def _send(self, code, sentdata):
        totalsent = 0
        rqs = code.encode() + sentdata
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
        choice = input('Choose!\n\t1. request someone\'s IP\n\t2. Check out the database\n\t3. Change your username\n\t4. Block contact\n')
        if choice == '1':
            name = input('Dude\'s name please\n')
            EchoClient(name.encode(), '1').run()
        elif choice == '2':
            password = input('Password?\n')
            if password == 'echo1234':
                pass
        elif choice == '3':
            username = input('Username ?\n')
            pass
        elif choice == '4':
            block = input('Contact to block ?\n')
            pass
        else:
            print('Unknown command')
