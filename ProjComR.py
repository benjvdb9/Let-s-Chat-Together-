#!/usr/bin/env python3
# echo.py
# author: Sébastien Combéfis
# version: February 15, 2016

import socket
import sys

SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        
    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                reqst= self._receive(client) 
                print(reqst.decode())
                client.send(reqst)
                client.close()
            except OSError:
                print('Erreur lors de la réception du message.')
    
    def _receive(self, client):
        chunks = []
        finished = False
        while not finished:
            data = client.recv(1024)
            chunks.append(data)
            finished = data == b''
        return b''.join(chunks)


class EchoClient():
    def __init__(self, IPrequest):
        self.__request = IPrequest
        self.__s = socket.socket()
    
    def run(self):
        try:
            self.__s.connect(SERVERADDRESS)
            print(self._send())
            self.__s.close()
        except OSError:
            print('Serveur introuvable, connexion impossible.')
    
    def _send(self):
        totalsent = 0
        rqs = self.__request
        try:
            while totalsent < len(rqs):
                sent = self.__s.send(rqs[totalsent:])
                totalsent += sent
            return reqst.decode()
        except OSError:
            print("Erreur lors de l'envoi du message.")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        EchoServer().run()
    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        EchoClient(sys.argv[2].encode()).run()
