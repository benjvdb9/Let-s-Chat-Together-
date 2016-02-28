#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 15, 2016

import socket
import sys
import ast
import json

IP = socket.gethostbyname(socket.gethostname())
SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        self.__addr = ''
        self.__client = ''
        self.__clientIPlist = []
        self.__namelist = []
        self.__database = {}
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            self.__client = client
            self.__addr = addr[0]
            self._clientlist()
            try:
                print('Connected by:', addr)
                reqst= self._receive(client)
                sent = reqst
                self._routechoice(reqst[0], reqst[1])
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
            chunks.append(data)
            finished = data == b''
        message = b''.join(chunks).decode()[1:] #La première lettre sert a identifier le type de requète
        code =b''.join(chunks).decode()[:1]
        print('Code:', code)
        return (code, message)

    def _routechoice(self, code, message):
        print('routechoice:', code, message)
        if code == '1':
            print('Chose IPrequest')
            self._IPrequest(message)
        if code == '2':
            self._database(message)
        if code == '3':
            self._username(message)

    def _IPrequest(self, IPreq):
        for elem in self.__database.keys():
            name = elem.split('.')[0]
            hostname = self.__database[elem][0]
            if elem == IPreq or name == IPreq or hostname == IPreq or hostname.split('.')[0] == IPreq:
                IP = self.__database[elem][1]
                msg = 'His IP address is ' + IP 
                self.__client.send(msg.encode())

    def _database(self, password):
        if password == 'echo1234':
            msg = json.dumps(self.__database, indent=2, ensure_ascii= False)
            self.__client.send(msg.encode())

    def _clientlist(self):
        try:
            with open('database.txt', 'r') as file:
                datb = file.read()
                datbase = ast.literal_eval(datb)
                self.__database = datbase
        except:
            datbase= {}

        for elem in self.__database.keys():
            self.__namelist += [elem]
            print('Pose problème:', self.__database[elem][1])
            self.__clientIPlist += [self.__database[elem][1]]
        
        if self.__addr not in self.__clientIPlist:
            self.__clientIPlist += [self.__addr]
            print('ClientIPList:', self.__clientIPlist)
            name = socket.gethostbyaddr(self.__addr)[0]
            print('Client Name:', name)
            self.__namelist += [name]
            self._writedatabase()
                
    def _writedatabase(self):
        maxi = len(self.__clientIPlist)
        dbse = {self.__namelist[i] : [self.__namelist[i], self.__clientIPlist[i]] for i in range(0, maxi)}
        self.__database = dbse
        with open('database.txt', 'w') as file:
            file.write(str(dbse))


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
        self._send(self.__request, self.__choice)
        self._receive()
        self.__s.close()
    
    def _send(self, sentdata, code):
        totalsent = 0
        rqs = code.encode() + sentdata
        try:
            while totalsent < len(rqs):
                sent = self.__s.send(rqs[totalsent:])
                totalsent += sent
        except OSError:
            print("Erreur lors de l'envoi du message.")

    def _receive(self):
        chunks = []
        finished = False
        while not finished:
            data = self.__s.recv(512)
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
            EchoClient(password.encode(), '2').run()
        elif choice == '3':
            username = input('Username ?\n')
            pass
        else:
            print('Unknown command')
