import socket
from _thread import *
import threading
import json

HOST = '127.0.0.1'
PORT = 65432

'''
state= {
  id = #
  user_id = #
  user = str
  turn = #
  last_movement = str
  left = []
}
'''

cards = ["3", "4", "5", "6", "7", "J", "Q", "K", "A", "2"]

print_lock = threading.Lock()

def threaded(c):
  c.send(b"Welcome to President")
  data = c.recv(1024)
  jmsg = json.loads(data.decode())
  if jmsg['type'] == "login":
    print("Bienvenido " + jmsg['body'])
    jmsg = {
      'type': "login",
      'body': True,
    }
    msg = json.dumps(jmsg)
    c.send(msg.encode())
    while True:
      data = c.recv(1024)
      msg = json.loads(data.decode())
      if msg['type'] == "normal":
        print("Recieved: ", msg['body'])
        c.send(msg['body'].encode())
      elif msg['type'] == "logout":
        print('bye')
        break
      else:
        continue
  else:
    print("Error")
  print_lock.release()
  c.close()

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    s.listen()
    while True:
      conn, addr = s.accept()
      print_lock.acquire()
      print("Connected by ", addr)
      start_new_thread(threaded, (conn,))
    s.close()


if __name__ == "__main__":
  main()