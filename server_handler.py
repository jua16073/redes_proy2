import json
from Salas import Salas
import President
import View
import controller
import player
import Deck
import pickle

games = []
# controllers = controller.Controller(game)
# view = View.View(game)
# sala = {
#       'nombre': msg['room'],
#       'users': temp_users,
#       'turn': 0,
#       'current_card': 0
#     }

cards = ["3", "4", "5", "6", "7", "J", "Q", "K", "A", "2"]

complete = []
users = []
rooms = []

salas = Salas(4)

def handler(jmsg, c):
  msg = json.loads(jmsg)
  # LOGIN
  if msg['type'] == "login":
    users.append([c,msg['body'], None])
    complete.append((c, msg['body']))
    response = {
      'type': "login",
      'user': msg['body'],
      'body': True,
    }
      # 'id': users.index(msg['body']),
    print("Bienvenido: " + msg['body'])

  # Creacion de cuartos
  elif msg['type'] == "start":
    print("Se esta creando la sala " + msg['body'])
    salas.create_room(msg['body'])
    response = {
      'type': "room",
      'body': "Created"
    }

  elif msg['type']=='startGame':
    cards = Deck.generar_cartas()
    user_cards = [[], [], [], [], []]
    temp_users = []
    for user in users:
        if user[2] == msg['room']:
          temp_users.append(user)
    sala = {
      'name': msg['room'],
      'users': temp_users,
      'turn': 0,
      'current_card': [0,0,0]
    }
    rooms.append(sala)
    while len(cards):
      for user in temp_users:
        if len(cards) > 0:
          temp_card = cards.pop()
          user_cards[temp_users.index(user)].append(temp_card.name + "/"+ str(temp_card.num) + "/" + temp_card.suit)
    response = {
      'type' : 'cards',
      'to': temp_users,
      'body': "nani",
      'cards': user_cards,
      'turn': temp_users[sala['turn']][1],
      'current_card': sala['current_card']
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
    for user in users:
      if user[0] == c:
        user[2] = msg['body']
    response = {
      'type': "joined",
      'body':"Joined",
      'room': msg['body']
    }

  # generic chat 
  elif msg['type'] == 'chat':
    tos = []
    for x in complete:
      tos.append(x)
    response = {
      'type': 'chat',
      'to': tos,
      'body': msg['body']
    }

  elif msg['type'] == "move":
    for s in rooms:
      if s['name'] == msg['room']:
        print("Si son iguales")
        s['turn'] = (s['turn'] + 1) % len(s['users'])
        s['current_card'] = msg['selected']
        response = {
          'to': s['users'],
          'type': "move",
          'current_card': s['current_card'],
          'turn': s['users'][s['turn']][1]
        }
    print(rooms)

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
