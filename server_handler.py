import json
from Salas import Salas

cards = ["3", "4", "5", "6", "7", "J", "Q", "K", "A", "2"]

users = []
rooms = []

salas = Salas(4)

def handler(jmsg):
  msg = json.loads(jmsg)
  # LOGIN
  if msg['type'] == "login":
    users.append(msg['body'])
    response = {
      'type': "login",
      'user': msg['body'],
      'id': users.index(msg['body']),
      'body': True,
    }
    print("Bienvenido: " + msg['body'])
  # Creacion de cuartos
  elif msg['type'] == "start":
    print("Se esta creando la sala " + msg['body'])
    response = {
      'type': "normal",
      'body': "nani"
    }
    salas.create_room(msg['body'])
    
  
  elif msg['type']=="getrooms":
    print(salas.all_salas())
    response = {
      'body ': salas.all_salas()
    }
  elif msg['type']=="join":
    salas.unir_sala(msg['name'], msg['body'])
    response = {
      'body ':"hola"
    }
  # NORMAL
  elif msg['type'] == "normal":
    print(msg['body'])
    response = {
      'type': "normal",
      'body': msg['body'],
    }
  # LOGOUT
  elif msg['type'] == "logout":
    print("Bye")
    return False
  # Default
  else:
    response = {
      'type': "normal",
      'body': "nani",
    }
  return (json.dumps(response))
