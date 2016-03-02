import socket
import sys
import threading
import ast
import time
from ProjComR import EchoClient

class Chat():
    def __init__(self, host=socket.gethostname(), port= 5000):
        s= socket.socket(type=socket.SOCK_DGRAM)
        s.settimeout(0.5)
        if host == '*':
            host=socket.gethostname()
        s.bind((host, port))
        self.__host = host
        self.__linelen= 0
        self.__s= s
        print('Listening on {}: {}'.format(host, port))
        with open('database.txt', 'r') as file:
            datbase= file.read()
            file.close()
        self.__database= ast.literal_eval(datbase)

    def run(self):
        handlers = {
            '/exit': self._exit,
            '/quit': self._quit,
            '/join': self._join,
            '/send': self._send,
            '/list': self._list,
            '/r': self._refresh,
            '/db': self._dtbase,
            '/IP': self._reqsIP,
            '/user': self._user,
            '/check': self._onl,
            '/end': self._endsv,
            '/help': self._help
        }
        self.__running = True
        self.__address = None
        self.__clientlist= []
        self.__tokenslist= []
        self.__portlist= []
        self.__index = 0
        threading.Thread(target= self._recieve).start()
        threading.Thread(target= self._refreshdatabase).start()
        while self.__running:
            line1= sys.stdin.readline()
            line= line1.rstrip() + ' ' #exm, str: /join Mioz 6000
            command = line[:line.index(' ')] # str: /join
            param = line[line.index(' ')+1:].rstrip() # str: host et port
            if command in handlers:
                try:
                    handlers[command]() if param == '' else handlers[command](param)
                except:
                    if not command == '/end':
                        print("An error occured during the execution of the command.")
            else:
                print('Unknown Command:', command)

    def _exit(self):
        self.__running = False
        self.__address = None
        self.__s.close()
        EchoClient(b'', '5').run()
        time.sleep(1)
        EchoClient(b'', '').leave()

    def _quit(self):
        self.__address = None

    def _join(self, param):
        tokens = param.split(' ')
        try:
            r = int(tokens[0].split('.')[0])
        except:
            print(tokens[0], 'is not an IP address')
            return
        client= socket.gethostbyaddr(tokens[0])[0]
        clientport= int(tokens[1])
        if len(tokens) == 2:
            try:
                self.__address= (client, clientport)
                if client not in self.__clientlist:
                    print('\n' + client, 'added to contact list\n')
                    self.__clientlist[:] = [client + ' AKA ' + self.__database[client][0]]
                    self.__tokenslist[:] = [tokens[0]]
                    self.__portlist[:]  = [clientport]
                    self.__index= len(self.__clientlist)
                print("Connected to {}: {}".format(*self.__address))
            except OSError:
                print("Error, could not send message.")

    def _send(self, param):
        if self.__address is not None:
            try:
                sentfrom = self.__database[self.__host][0]
                sentto= self.__database[self.__address[0]][0]
                message= b'from ' + sentfrom.encode() + b': ' + param.encode()
                totalsent = 0
                while totalsent < len(message):
                    sent= self.__s.sendto(message[totalsent:], self.__address)
                    totalsent += sent
                #print(''.join(lenlist))
                print('to {}: {}'.format(sentto, param))
            except OSError:
                print('Error when receiving message')
        else:
            print('Nobody to send a message to')
            

    def _recieve(self):
        while self.__running:
            try:
                data, address = self.__s.recvfrom(512)
                print(data.decode())
                sys.stdout.flush()
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

    def _refresh(self):
        pass

    def _refreshdatabase(self):
        while self.__running:
            time.sleep(10)
            with open('database.txt', 'r') as file:
                self.__database= ast.literal_eval(file.read())
                file.close()

    def _dtbase(self):
        password = input('Password?\n')
        EchoClient(password.encode(), '2').run()

    def _reqsIP(self):
        name = input("Who's IP address would you like?\n")
        EchoClient(name.encode(), '1').run()

    def _user(self):
        username = input('Username?\n')
        EchoClient(username.encode(), '3').run()

    def _onl(self):
        EchoClient(b'', '4').run()

    def _endsv(self):
        password = input('Password?\n')
        if password == 'echo1234':
            self.__running = False
            self.__address = None
            EchoClient(b'', '6').run()
            time.sleep(1)
            EchoClient(b'', '').leave(True)
            self.__s.close()
        else:
            print('Wrong password')

    def _help(self):
        print('''Command  : Description                           : Parameters

/join    : Join someone to chat with ()          : IP address, port
/send    : Send a message to whomever you joined : message
/quit    : Leave the person you've joined earlier: (None)
/r       : Manually refresh messages             : (None)
/list    : A little reminder of who you joined   : (None)
           recently
/IP      : Request someone's IP address          : (None)
/db      : Check out the database                : (None)
           (reseved for admins)
/user    : Change your username                  : (None)
/check   : Check who's online                    : (None)
/exit    : Leave the server and stop the chat    : (None)
/end     : Close the server itself               : (None)
           (reserved for admins)''')
                
if __name__ == '__main__':
    print('Connecting to server')
    EchoClient(b'Connected to server', '7').run()
    if len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run() #Sert a changer l'info du récepteur
    else:
        Chat().run()
