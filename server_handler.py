import json
from Salas import Salas
import President
import View
import controller
import player
import Deck
import pickle

# controllers = controller.Controller(game)
# view = View.View(game)
# sala = {
#       'nombre': msg['room'],
#       'users': temp_users,
#       'turn': 0,
#       'current_card': 0
#     }

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
      'active_players': temp_users.copy(),
      'round_players': temp_users.copy(),
      'turn': 0,
      'card_value': 0,
      'card_quantity': 1
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
      'current_card': sala['card_value'],
      'card_quantity': sala['card_quantity']
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
        if msg['selected'] == 'pass':
          for user in s['round_players']:
            if user[1] == msg['from']:
              s['round_players'].remove(user)
              s['turn'] = s['turn'] % len(s['round_players'])
              if len(s['round_players']) <= 1 :
                actual = s['round_players'][0]
                s['round_players'] = s['active_players'].copy()
                s['card_value'] = 0
                s['card_quantity'] = 0
                s['turn'] = s['active_players'].index(actual)
          response = {
            'to': s['users'],
            'type': "move",
            'current_card': s['card_value'],
            'card_quantity': s['card_quantity'],
            'turn': s['round_players'][s['turn']][1],
          }
        else:
          print("Movimiento")
          s['turn'] = (s['turn'] + 1) % len(s['round_players'])
          s['card_value'] = msg['selected'][1]
          response = {
            'to': s['users'],
            'type': "move",
            'current_card': s['card_value'],
            'card_quantity': s['card_quantity'],
            'turn': s['round_players'][s['turn']][1]
          }

  # FINISHED
  elif msg['type'] == "finished":
    print(msg['from']," termino")
    #for s in rooms:
     # if s['name'] == msg['room']:
    
    response = {
      'type': "finished",
      'body': "Termino"
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
