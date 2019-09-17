import socket
import json
import threading
from threading import Lock, Event, Barrier
from _thread import *

# username = ''
# id = -1
# room = -1

class Client:
  def __init__(self, username, HOST = '127.0.0.1', PORT = 65432):
    self.id = None
    self.name = username
    self.room = None
    self.lock = threading.Lock()
    self.server = (HOST, PORT)
    self.connected = True
    self.register()
    self.cards = None
    self.card_names = None
    self.current_turn = None
    self.current_card = None

  # Registrar en Server
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
    #self.id = msg['id']
    print("Listo " + self.name)
    #" id: " + str(self.id)
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
      body = input("Ingrese el nombre del cuarto al que desea ingresar: ")
      self.join_room(body, self.name)
    elif body == "empezar":
      jmsg = {
        'type': "startGame",
        'room': self.room
      }
      msg = json.dumps(jmsg)
      self.s.send(msg.encode())
    elif body == "chat":
      body = input("Mensaje a mandar: ")
      jmsg = {
        'type': 'chat',
        'body': body,
      }
      msg = json.dumps(jmsg)
      self.s.send(msg.encode()) 
    elif body == "jugada":
      names = []
      selected = []
      if self.current_turn == self.name:
        while True:
          for card in self.cards:
            print(" ", card[0])
            names.append(card[0])
          card = input("Ingrese el nombre de las cartas o carta (separadas por coma)")
          if card in names:
            for c in self.cards:
              if card == c[0]:
                if int(c[1]) >= int(self.current_card[1]):
                  self.cards.remove(c)
                  jmsg = {
                    'type': 'move',
                    'room': self.room,
                    'selected': c,
                  }
                  msg = json.dumps(jmsg)
                  self.s.send(msg.encode())
                  break
                else:
                  print("Carta no valida, carta en juego es mayor")
          else:
            print("Carta no esta en tu mano")
      else:
        print("No es tu turno")

    else:
      jmsg = {
        'type': 'normal',
        'body': body,
      }
      msg = json.dumps(jmsg)
      self.s.send(msg.encode())
  
  # Create rooms
  def create_room(self, room):
    jmsg = {
      'type': 'start',
      'body': room
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  # Get all available rooms
  def get_room(self):
    jmsg = {
      'type': 'getrooms',
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  # Join_rooms
  def join_room(self, room, name):
    jmsg = {
      'type': 'join',
      'body': room,
      'name': name,
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  # Know how to handle recieved messages
  def reciever(self, jmsg):
    msg = json.loads(jmsg)
    if msg['type'] == "normal":
      print("\nrecibido: ", msg['body'])

    elif msg['type'] == "room":
      print(msg['body'])

    elif msg['type'] == 'joined':
      self.room = msg['room']
      print("Joined to room: ", self.room)

    elif msg['type'] == 'cards':
      print("Cartas Recibidas")
      cards = []
      for card in msg['cards']:
        cards.append(card.split("/"))
      self.cards = cards
      print(self.cards)
      self.current_card = msg['current_card']
      self.current_turn = msg['turn']
      print("El turno es de: ", msg['turn'])

    elif msg['type'] == 'move':
      self.current_card = msg['current_card']
      self.current_turn = msg['turn']
      print("El turno ahora es de: ", self.current_turn)
      print("Carta en la mesa es: ", self.current_card)
    else:
      print(msg)

  # Logout from server
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
        data = self.conn.recv(2048)
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