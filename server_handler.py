import json
from Salas import Salas

cards = ["3", "4", "5", "6", "7", "J", "Q", "K", "A", "2"]

users = []
complete = []

salas = Salas(4)

def handler(jmsg, c):
  msg = json.loads(jmsg)
  # LOGIN
  if msg['type'] == "login":
    users.append(msg['body'])
    complete.append((c, msg['body']))
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
    salas.create_room(msg['body'])
    response = {
      'type': "room",
      'body': "Created"
    }

  # Send existing rooms
  elif msg['type']=="getrooms":
    print(salas.all_salas())
    response = {
      'type': 'room',
      'body': salas.all_salas()
    }

  # Make user join room
  elif msg['type']=="join":
    salas.unir_sala(msg['name'], msg['body'])
    response = {
      'type': "joined",
      'body':"Joined",
      'room': msg['body']
    }
  
  elif msg['type'] == 'chat':
    tos = []
    for x in complete:
      tos.append(x)
    response = {
      'type': 'chat',
      'to': tos,
      'body': msg['body']
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
    for u in complete:
      if u[0] == c:
        complete.remove(u)
    print("Bye")
    return False
  # Default
  else:
    response = {
      'type': "normal",
      'body': "nani",
    }
  return (response)
