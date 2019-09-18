import socket
import json
import threading
from threading import Lock, Event, Barrier
from _thread import *
from colorama import init
from colorama import Fore, Back, Style

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
    self.current_turn = None
    self.current_card = None
    self.current_quantity = 0

  # Registrar en Server
  def register(self):
    jmsg = {
      'type': 'login',
      'body': self.name,
    }
    msg = json.dumps(jmsg)
    #print(Back.MAGENTA + Fore.CYAN + msg + Style.RESET_ALL)
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect(self.server)
    data = self.s.recv(1024)
    print(Back.MAGENTA + Fore.CYAN + data.decode() + Style.RESET_ALL)
    self.s.send(msg.encode())
    data = self.s.recv(1024)
    msg = json.loads(data.decode())
    self.server_listener = listener(self.s, self)
    self.server_listener.start()
    self.send_msg()
  
  def help():
    print("Comandos")
    print("start: Crear sala")
    print("join: Unirse a sala")
    print("search: Mostrar salas")
    print("game: Empezar el juego")
    print("move: Realizar jugada")
    print("exit: Salir del juego")
  
  def send_msg(self):
    body = input("Comando: ")
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

    elif body == "game":
      jmsg = {
        'type': "startGame",
        'from': self.name,
        'room': self.room,
      }
      msg = json.dumps(jmsg)
      self.s.send(msg.encode())

    elif body == "chat":
      if self.room != None:
        body = input("Mensaje a mandar: ")
        jmsg = {
          'type': 'chat',
          'from': self.name,
          'room': self.room,
          'body': body,
        }
        msg = json.dumps(jmsg)
        self.s.send(msg.encode()) 
      else:
        print("No estas en una sala todavia")

    elif body == "move":
      names = []
      selected = []
      if self.current_turn == self.name:
        cycle = True
        while cycle:
          for card in self.cards:
            print(Back.RED+Fore.WHITE," ", card[0] , Style.RESET_ALL)
            names.append(card[0])
          card = input("Ingrese el nombre de las cartas o carta (separadas por coma): \n")
          multiple = card.split(", ")
          if len(multiple) == 1:
            if card in names:
              for c in self.cards:
                if card == c[0]:
                  if int(c[1]) >= int(self.current_card) and 1 >= self.current_quantity:
                    self.cards.remove(c)
                    jmsg = {
                      'type': 'move',
                      'from': self.name,
                      'room': self.room,
                      'selected': c,
                      'card_quantity': 1
                    }
                    msg = json.dumps(jmsg)
                    self.s.send(msg.encode())
                    if len(self.cards) == 0:
                      jmsg = {
                        'type': 'finished',
                        'from': self.name,
                        'room': self.room,
                      }
                      msg = json.dumps(jmsg)
                      self.s.send(msg.encode())
                    cycle = False
                  else:
                    print("Carta no valida, carta en juego es mayor")
            elif card == "pass":
              jmsg = {
                'type': 'move',
                'from': self.name,
                'room': self.room,
                'selected': 'pass',
              }
              msg = json.dumps(jmsg)
              self.s.send(msg.encode())
              cycle = False
            else:
              print(Back.RED + Fore.BLACK + "Carta no esta en tu mano"+ Style.RESET_ALL)
          else:
            check = True
            for c_name in multiple:
              if c_name in names:
                pass
              else:
                check = False
                print(Back.RED + Fore.BLACK + c_name, " no esta en tu mano" + Style.RESET_ALL)
            if len(multiple) >= self.current_quantity:
              values = []
              selected_cards = []
              for c in self.cards:
                for c_name in multiple:
                  if c[0] == c_name:
                    values.append(c[1])
                    selected_cards.append(c)
              if len(set(values)) == 1:
                if int(values[0]) >= int(self.current_card):
                  print("Valor: ", values[0])
                  for sc in selected_cards:
                    self.cards.remove(sc)
                  jmsg = {
                      'type': 'move',
                      'from': self.name,
                      'room': self.room,
                      'selected': selected_cards[0],
                      'card_quantity': len(multiple)
                    }
                  msg = json.dumps(jmsg)
                  self.s.send(msg.encode())
                  if len(self.cards) == 0:
                      jmsg = {
                        'type': 'finished',
                        'from': self.name,
                        'room': self.room,
                      }
                      msg = json.dumps(jmsg)
                      self.s.send(msg.encode())
                  cycle = False
                else:
                  print(Back.RED + Fore.BLACK + "El valor de La(s) carta(s) en juego es mayor"+ Style.RESET_ALL)
            else:
              print(Back.RED + Fore.BLACK + "Tines que jugar un numero mayor o igual a las cartas en juego"+ Style.RESET_ALL)
      else:
        print(Back.RED + Fore.BLACK + "No es tu turno" + Style.RESET_ALL)

    else:
      jmsg = {
        'type': 'normal',
        'from': self.name,
        'body': body,
      }
      msg = json.dumps(jmsg)
      self.s.send(msg.encode())
  
  # Create rooms
  def create_room(self, room):
    jmsg = {
      'type': 'start',
      'from': self.name,
      'body': room
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  # Get all available rooms
  def get_room(self):
    jmsg = {
      'from': self.name,
      'type': 'getrooms',
    }
    msg = json.dumps(jmsg)
    self.s.send(msg.encode())

  # Join_rooms
  def join_room(self, room, name):
    jmsg = {
      'type': 'join',
      'from': self.name,
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
      #print(self.cards)
      self.current_card = msg['current_card']
      self.current_turn = msg['turn']
      print(Back.BLUE+ Fore.WHITE+"El turno es de: ", msg['turn'], Style.RESET_ALL)

    elif msg['type'] == "finished":
      print(Fore.BLUE + Back.YELLOW +"Termino, ahora a esperar al resto")
      print("Puesto: ", msg['puesto'], Style.RESET_ALL)

    elif msg['type'] == 'move':
      self.current_card = msg['current_card']
      self.current_turn = msg['turn']
      self.current_quantity = msg['card_quantity']
      print(Back.BLUE+Fore.WHITE+"El turno ahora es de: ", self.current_turn , Style.RESET_ALL)
      print(Back.BLUE + Fore.WHITE+"Carta en la mesa es: ", self.current_card , Style.RESET_ALL)
      print(Back.BLUE + Fore.WHITE+"Cantidad de la carta en mesa: ", self.current_quantity , Style.RESET_ALL)

    elif msg['type'] == 'chat':
      print(Back.CYAN+Fore.BLACK+msg['from'],":" + Back.LIGHTMAGENTA_EX + Fore.WHITE,msg["body"] + Style.RESET_ALL)

    else:
      print(msg)

  # Logout from server
  def logout(self):
    jmsg = {
      'from': self.name,
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
  init()
  user = input(Back.GREEN + Fore.BLACK+"Ingrese su nombre de Usuario" + Style.RESET_ALL + " ")
  client = Client(user)
  while True:
    if client.connected:
      client.send_msg()
    else:
      break