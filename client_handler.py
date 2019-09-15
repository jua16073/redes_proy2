import json
from threading import Lock, Event

username = ""
id = -1
room = -1

state = {

}

def handler(jmsg, event):
  msg = json.loads(jmsg)
  if msg['type'] == 'login':
    username = msg['user']
    id = msg['id']
    print("usuario: " + msg['user'] + " id:" + str(msg['id']))
  elif msg['type'] == 'normal':
    print(msg['body'])


def send_handler(event):
  print("Id es: ", id)
  if id == -1:
    resp = input("Ingrese su usuario\n")
    jmsg = {
      'type': "login",
      'body': resp,
    }
    if resp == 'exit':
      return False
    respose = json.dumps(jmsg)
  else:
    if room == -1:
      resp = input("Desea: \n 1) Crear sala \n 2) Unirse a sala \n 3) Ver salas disponibles")
      if resp in [1, 2, 3]:
        jmsg = {
          'type': "room",
          'body': resp,
        }
        if resp == 'exit':
          return False
        respose = json.dumps(jmsg)
  return respose
