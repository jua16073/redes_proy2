import json

cards = ["3", "4", "5", "6", "7", "J", "Q", "K", "A", "2"]

users = []
rooms = []

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
    print("Salas")
    response = {
      'type': "normal",
      'body': "nani"
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
