import socket
import sys
import threading
import pdb


class Chat():
    def __init__(self, host=socket.gethostname(), port= 5000):
        s= socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.bind((host, port))
        self.__s= s
        print('Écoute sur {}: {}'.format(host, port))

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/list': self._list
        }
        self.__running = True
        self.__address = None
        self.__clientlist= []
        self.__tokenslist= []
        self.__portlist= []
        threading.Thread(target= self._recieve).start()
        while self.__running:
            line= sys.stdin.readline().rstrip() + ' ' #exm, str: /join Mioz 6000
            command = line[:line.index(' ')] # str: /join
            param = line[line.index(' ')+1:].rstrip() # str: host et port
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    print("Erreur lors de l'exécution de la commande.")
            else:
                print('Commande inconnue:', command)

    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()

    def _quit(self):
        self.__address = None

    def _join(self, param):
        tokens = param.split(' ')
        client= socket.gethostbyaddr(tokens[0])[0]
        clientport= int(tokens[1])
        if len(tokens) == 2:
            try:
                self.__address= (client, clientport)
                if client not in self.__clientlist:
                    print('\n' + tokens[0], 'added to contact list\n')
                    self.__clientlist[:] = [client]
                    self.__tokenslist[:] = [tokens[0]]
                    self.__portlist[:]  = [clientport]
                    self.__index= len(self.__clientlist)
                print("Connecté à {}: {}".format(*self.__address))
            except OSError:
                print("Erreur lors de l'envoi du message.")
            except:
                print('Erreur, join')

    def _send(self, param):
        if self.__address is not None:
            try:
                message= param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent= self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
            except OSError:
                print('Erreur lors de la réception du message')
        else:
            print('Personne a qui envoyer le message')
            

    def _recieve(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(512)
                print(data.decode())
            except socket.timeout:
                pass
            except OSError:
                return
            
    def _list(self):
        i= 0
        print('\nLIST\n---')
        while i < self.__index:
            print('    ' + self.__clientlist[i], '['+ str(self.__tokenslist[i])+ '] (port:', str(self.__portlist[i]) + ')')
            i +=1
        print('---')
            
    def Address(self):
        return self.__address

if __name__ == '__main__':
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run() #Sert a changer l'info du récepteur
    else:
        Chat().run()
