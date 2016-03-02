import socket
import sys
import ast
import json
import time

IP = socket.gethostbyname(socket.gethostname())
SERVERADDRESS = (socket.gethostname(), 6000)

class EchoServer():
    def __init__(self):
        self.__s = socket.socket()
        self.__s.bind(SERVERADDRESS)
        self.__addr = ''
        self.__client = ''
        self.__name = ''
        self.__clientIPlist = []
        self.__namelist = []
        self.__userlist = []
        self.__database = {}
        
    def run(self):
        self.__s.listen()
        while True:
            self.__client, addr = self.__s.accept()
            print('Connected by:', addr)
            self.__addr = addr[0]
            self._clientlist()
            try:
                reqst= self._receive(self.__client)
                sent = reqst
                self._routechoice(reqst[0], reqst[1])
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
        return (code, message)

    def _routechoice(self, code, message):
        print('routechoice:', code, message)
        if code == '1':
            print('Chose IPrequest')
            self._IPrequest(message)
        if code == '2':
            print('Chose database')
            self._database(message)
        if code == '3':
            print('Chose username')
            self._username(message)
        if code == '4':
            self._checkonline()
        if code == '5':
            print('Client leaving server')
            self._leave()
        if code == '6':
            print('Closing server')
            self._quit()

    def _IPrequest(self, IPreq):
        found = False
        for elem in self.__database.keys():  #exemples: elem = Mioznitnirn.lan
            hostname = elem.split('.')[0]              #hostname= Mioznitnirn
            username = self.__database[elem][0]        #username= Benjamin
            if elem == IPreq or hostname == IPreq or username == IPreq:
                IP = self.__database[elem][1]
                msg = 'His IP address is ' + IP + ' ({})\n'.format(elem)
                self.__client.send(msg.encode())
                found = True
        if not found:
            msg = 'It seems {} cannot be found in the database'.format(IPreq)
            self.__client.send(msg.encode())

    def _database(self, password):
        if password == 'echo1234':
            msg = json.dumps(self.__database, indent=2, ensure_ascii= False)
            self.__client.send(msg.encode())
        else:
            msg = 'Wrong password'
            self.__client.send(msg.encode())

    def _username(self, username):
        i = 0
        for elm in self.__namelist:
            if elm == socket.gethostbyaddr(self.__addr)[0]:
                msg = username + ' replaced ' + self.__userlist[i]
                print(msg)
                self.__userlist[i] = username
                i+=1
            else:
                i += 1
        self._writedatabase()
        try:
            self.__client.send(msg.encode())
        except:
            self.__client.send(b'An error occured')

    def _checkonline(self):
        onlinelist= []
        for elm in self.__database:
            options = self.__database[elm]
            if options[2] == '1':
                onlinelist += [options[0] + ' (' + elm+ ')']
        msg = '\n\t' + '\n\t'.join(onlinelist)
        print(msg)
        self.__client.send(msg.encode())

    def _leave(self):
        self.__database[self.__name][2] = '0'
            
    def _quit(self):
        self.__client.close()
        self.__database[self.__name][2] = '0'
        sys.exit()

    def _clientlist(self):
        try:
            with open('database.txt', 'r') as file:
                datb = file.read()
                datbase = ast.literal_eval(datb)
                self.__database = datbase
        except:
            datbase= {}
            self.__database = datbase

        self.__userlist = []
        self.__namelist = []
        self.__clientIPlist = []
        self.__authacces = []
        for elem in self.__database.keys():
            self.__namelist += [elem]
            self.__userlist += [self.__database[elem][0]]
            self.__clientIPlist += [self.__database[elem][1]]
            self.__authacces += [self.__database[elem][2]]

        self.__name = socket.gethostbyaddr(self.__addr)[0]
        self.__database[self.__name][2] = '1'
            
        if self.__addr not in self.__clientIPlist:
            self.__clientIPlist += [self.__addr]
            print('New client!', self.__name, self.__addr)
            self.__userlist += [self.__name]
            self.__namelist += [self.__name]
            self.__authacces += '1'
            self._writedatabase()
                
    def _writedatabase(self):
        maxi = len(self.__clientIPlist)
        dbse = {self.__namelist[i] : [self.__userlist[i], self.__clientIPlist[i], self.__authacces[i]] for i in range(0, maxi)}
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

    def leave(self, Closing= False):
        if Closing:
            print('Closing server')
        else:
            print('Leaving server')
        self.__s.close()
        sys.exit()
    
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
        time.sleep(3)
        while not finished:
            self.__s.settimeout(2)
            try:
                data = self.__s.recv(32)
            except:
                data = b''
            chunks.append(data)
            finished = data == b''
        print(b''.join(chunks).decode())

if __name__ == '__main__':
    while True:
        if len(sys.argv) == 2 and sys.argv[1] == 'server':
            EchoServer().run()
        elif len(sys.argv) == 2 and sys.argv[1] == 'client':
            choice = input('Commands:\n\t1. request someone\'s IP\n\t2. Check out the database\n\t3. Change your username\n\t4. Check out the people connected to the server\n\t5. Leave\n\t6. Close the server\n')
            if choice == '1':
                name = input("Who's IP address would you like?\n")
                EchoClient(name.encode(), '1').run()
            elif choice == '2':
                password = input('Password?\n')
                EchoClient(password.encode(), '2').run()
            elif choice == '3':
                username = input('Username ?\n')
                EchoClient(username.encode(), '3').run()
            elif choice == '4':
                EchoClient(b'', '4').run()
            elif choice == '5':
                EchoClient(b'', '5').run()
                time.sleep(1)
                EchoClient(b'', '').leave()
            elif choice == '6':
                password = input('Password?\n')
                if password == 'echo1234':
                    EchoClient(b'', '6').run()
                    time.sleep(1)
                    EchoClient(b'', '').leave(True)
            else:
                print('Unknown command')
        else:
            sys.exit()
