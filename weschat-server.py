import socket, select
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_sock.bind(("0.0.0.0", 8888))
server_sock.listen(16)
CONNECTIONS = [server_sock]
UNAMES = {}

class Room:
    def __init__(self, name):
        self.name = name
        self.users = []
    def admit(self, user):
        self.users.append(user)
        self.send(user, "You have entered the room "+self.name)
    def expel(self, user):
        try:
            self.send(user, "You have left the room "+self.name)
            self.users.remove(user)
        except:
            pass
    def recv(self, message):
        #print(self.users)
        for user in self.users:
            self.send(user, message)
    def lookupSocket(self, user):
        for connection in CONNECTIONS:
            try:
                if connection.getpeername() == user:
                    return connection
            except:
                pass
        return None
    def send(self, user, message):
        sock = self.lookupSocket(user)
        try:
            sock.send((message+"\n").encode("UTF-8"))
        except AttributeError:
            pass # Not a socket
        except:
            sock.close()
            self.expel(user)
            CONNECTIONS.remove(user)
    def lookupUser(self, user):
        return user in self.users
    def autoExpel(self):
        for user in self.users:
            if self.lookupSocket(user) == None:
                self.users.remove(user)
        if len(self.users) == 0 and self.name != "hall": # Hall never closes
            rooms.remove(self)

def broadcast(sock, message):
    message = bytes(message, "UTF-8")
    for s in CONNECTIONS:
        if s != server_sock:
            try:
                s.send(message)
            except:
                try: # Sometimes it can't be closed...
                    s.close()
                    CONNECTIONS.remove(s)
                except:
                    pass



def name(addr):
    #print(UNAMES)
    if addr in UNAMES.keys():
        return UNAMES[addr]
    else:
        return str(addr)

hall = Room("hall")
rooms = [hall]

def roomLookup(name):
    for room in rooms:
        if room.name == name:
            return room
    return None

def lookupUser(user):
    for room in rooms:
        if user in room.users:
            return room
    return None

## COMMANDS

class Commander:
    def __init__(self):
        self.COMMANDS = {
            "/uname":self.uname,
            "/join":self.join,
            "/help":self.help,
            "/room":self.room
            }

    def uname(self, data, addr, sock):
        uname = data[7:].strip("\r\n")
        UNAMES[addr] = uname

    def join(self, data, addr, sock):
        currentRoom = lookupUser(addr)
        currentRoom.expel(addr)
        rname = data[6:].strip("\r\n")
        room = roomLookup(rname)
        if room == None:
            room = Room(rname)
            rooms.append(room)
        room.admit(addr)

    def help(self, data, addr, sock):
        helpmessage = '''WesChat help menu:
/uname [username]: Change your username
/join [room]: Join a chatroom
/help: Display this help
/room: Display the current room name
'''
        sock.send(helpmessage.encode("UTF-8"))

    def room(self, data, addr, sock):
        room = lookupUser(addr)
        if room is None:
            room = "Error looking up room"
        room = "You are in the room "+room.name+"\n"
        sock.send(room.encode("UTF-8"))

    def command(self, data, addr, sock):
        for command in self.COMMANDS.keys():
            if data.startswith(command):
                self.COMMANDS[command](data, addr, sock)

commander = Commander()
##

WAITING = []
HANDSHAKE = "Ni"

try:
    while True:
        for room in rooms:
            room.autoExpel()
        read_sockets = select.select(CONNECTIONS+WAITING, [], [], 0)[0]
        for sock in read_sockets:
            if sock == server_sock:
                sfd, addr = server_sock.accept()
                #CONNECTIONS.append(sfd)
                WAITING.append(sfd)
                #hall.admit(addr)
                print("Client "+name(addr)+" connected, awaiting handshake")
                #hall.recv("<server> Client "+name(addr)+" connected")
            else:
                try:
                    data = sock.recv(4096)
                    addr = sock.getpeername()
                    if sock in WAITING:
                        if data.decode() == HANDSHAKE:
                            print(name(addr)+" handshaked")
                            WAITING.remove(sock)
                            hall.admit(addr)
                            hall.recv("Client "+name(addr)+" connected")
                            CONNECTIONS.append(sock)
                        else:
                            #print("Received "+data.decode()+" not "+HANDSHAKE)
                            WAITING.remove(sock)
                        continue
                    if data:
                        data = data.decode()
                        if data.startswith("/"):
                            commander.command(data, addr, sock)
                        else:
                            msg = "<"+name(addr)+"> "+data
                            #print(msg)
                            userRoom = lookupUser(addr)
                            userRoom.recv(msg)
                            #print(hall.users)
                            #print(lookupUser(addr))
                            #print(addr in hall.users)
                            #hall.recv(msg)
                except Exception as e:
                    print(e)
                    print("Client "+name(addr)+" disconnected")
                    try: # sometimes closing/removing will fail
                        sock.close()
                        CONNECTIONS.remove(sock)
                        hall.recv("<server> Client "+name(addr)+" disconnected")
                        try:
                            del UNAMES[addr]
                        except KeyError:
                            pass
                        continue
                    except:
                        continue
finally:
    server_sock.close()
