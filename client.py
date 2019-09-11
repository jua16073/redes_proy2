import socket
import json
import threading
from _thread import *
import client_handler as h

HOST = '127.0.0.1'
PORT = 65432
username = ''

def listenThread(c):
  while True:
    data = c.recv(1024)
    h.handler(data)


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
    start_new_thread(listenThread, (s,))
    while True:
      body = input("Mensaje: ")
      if body == "exit":
        jmsg = {
            'type': "logout"
          }
        msg = json.dumps(jmsg)
        s.send(msg.encode())
        break
      else:
        jmsg = {
          'type': 'normal',
          'body': body
        }
        msg = json.dumps(jmsg)
        s.send(msg.encode())
    s.close()


if __name__ == "__main__":
  main()