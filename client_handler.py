import json

username = ""
id = -1

state = {

}

def handler(jmsg):
  msg = json.loads(jmsg)
  if msg['type'] == 'login':
    username = msg['user']
    id = msg['id']
    print("usuario: " + msg['user'] + " id:" + str(msg['id']))
    pass
  elif msg['type'] == 'normal':
    print(msg['body'])


def send_handler(msg):
  print("handler for sending")