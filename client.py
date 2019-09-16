import socket
import json
import threading
from threading import Lock, Event, Barrier
from _thread import *
#import client_handler as h



# username = ''
# id = -1
# room = -1

class Client:


  def __init__(self, username, HOST = '127.0.0.1', PORT = 65432):
    self.id = None
    self.name = username
    self.room = None
    self.lock = threading.Lock()
    #self.server_listener.start()
    self.server = (HOST, PORT)
    self.connected = True
    self.register()

  def register(self):
    jmsg = {
      'type': 'login',
      'body': self.name,
    }
    msg = json.dumps(jmsg)
    print(msg)
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect(self.server)
    data = self.s.recv(1024)
    print(data.decode())
    self.s.send(msg.encode())
    data = self.s.recv(1024)
    msg = json.loads(data.decode())
    self.id = msg['id']
    print("Listo " + self.name + " id: " + str(self.id))
    self.server_listener = listener(self.s, self)
    self.server_listener.start()
    self.send_msg()
  
  def send_msg(self):
    body = input("Mensaje: ")
    if body == "exit":
      self.logout()
    elif body == "start":
      body = input("Ingrese el nombre del cuarto: ")
      self.create_room(body)
    elif body == "search":
      self.get_room()
    elif body == "join":
<<<<<<< HEAD
      body = input("Ingrese el nombre del cuarto al que desea ingresar: ")
      self.join_room(body, self.name)
    elif body == "empezar":
      self.start_game(self.name)
=======
      body = input("Ingrese el nombre dle cuarto al que desea ingresar: ")
      self.join_room(body,[self.id, self.name])
    elif body == "chat":
      body = input("Mensaje a mandar: ")
      jmsg = {
        'type': 'chat',
        'body': body,
      }
      msg = json.dumps(jmsg)
      self.s.send(msg.encode())
>>>>>>> bc8de9d7df10017bb2a9f599f53ac7a598fe6db8
    else:
      jmsg = {
        'type': 'normal',
        'body': body,
      }
      msg = json.dumps(jmsg)
      self.s.send(msg.encode())
  
  def create_room(self, room):
    jmsg = {
      'type': 'start',
      'body': room
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  def get_room(self):
    jmsg = {
      'type': 'getrooms',
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  def start_game(self, name):
    jmsg = {
      'type': 'startGame',
      'name': name,
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  def join_room(self,room,name):
    jmsg = {
      'type': 'join',
      'body': room,
      'name': name,
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  def reciever(self, jmsg):
    msg = json.loads(jmsg)
    if msg['type'] == "normal":
      print("\nrecibido: ", msg['body'])
    elif msg['type'] == "room":
      print(msg['body'])
    elif msg['type'] == 'joined':
      self.room = msg['room']
      print("Joined to room: ", msg['room'])
    else:
      print(msg)

  def logout(self):
    jmsg = {
      'type': 'logout',
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())
    self.connected = False
    self.server_listener.stop()

class listener(threading.Thread):
  def __init__(self, s, client):
    threading.Thread.__init__(self)
    self.client = client
    self.conn = s
  
  def run(self):
    while True:
      if self.client.connected:
        data = self.conn.recv(1024)
        if data:
          self.client.reciever(data.decode())
      else:
        break
  
  def stop(self):
    self.conn.close()


if __name__ == "__main__":
  user = input("Ingrese su nombre de Usuario ")
  client = Client(user)
  while True:
    if client.connected:
      client.send_msg()
    else:
      break