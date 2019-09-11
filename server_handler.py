import json

def handler(jmsg):
  msg = json.loads(jmsg)
  # LOGIN
  if msg['type'] == "login":
    response = {
      'type': "login",
      'body': True,
    }
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
      'body': "recibido",
    }
  # LOGOUT
  elif msg['type'] == "logout":
    print("Bye")
    return False
  else:
    response = {
      'type': "normal",
      'body': "nani",
    }
  return json.dumps(response)
