import socket
import json
import threading
from _thread import *

HOST = '127.0.0.1'
PORT = 65432
username = ''

def listenThread(c):
  while True:
    data = c.recv(1024)
    if data:
      print('Received ', data)
    else:
      continue


def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
    print(data)
    username = input("Ingrese su nombre de usuario: \n")
    jmsg = {
      'type': "login",
      'body': username,
    }
    msg = json.dumps(jmsg)
    s.send(msg.encode())
    data = s.recv(1024)
    jmsg = json.loads(data)
    if jmsg['body'] == True:
      start_new_thread(listenThread, (s,))
      while True:
        body = input("Ingrese su opción")
        jmsg = {
          'type': 'normal',
          'body': body,
        }
        msg = json.dumps(jmsg)
        s.send(msg.encode())
        ans = input('\n continue?')
        if ans == 'n':
          jmsg = {
            'type': "logout"
          }
          msg = json.dumps(jmsg)
          s.send(msg.encode())
          break
        else:
          continue
    s.close()


if __name__ == "__main__":
  main()