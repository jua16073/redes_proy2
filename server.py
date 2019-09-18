import socket
from _thread import *
import threading
import json
import server_handler as h

HOST = '127.0.0.1'
#HOST = '192.168.43.182'
PORT = 65432

cards = ["3", "4", "5", "6", "7", "J", "Q", "K", "A", "2"]
def threaded(c):
  c.send(b"Welcome to President")
  while True:
    data = c.recv(1024)
    print(data)
    response = h.handler(data.decode(), c)
    if not response:
      break
    else:
      if response['type'] == 'chat':
        for t in response['to']:
          response.pop('to', None)
          t[0].send(json.dumps(response).encode())
      elif response['type'] == 'cards':
        temp = response.copy()
        for t in response['to']:
          temp.pop('to', None)
          temp['cards'] = response['cards'][response['to'].index(t)]
          t[0].send(json.dumps(temp).encode())
      elif response['type'] == 'move':
        temp = response.copy()
        for t in response['to']:
          temp.pop('to', None)
          t[0].send(json.dumps(temp).encode())
      else:  
        c.send(json.dumps(response).encode())
    # try:
    #   data = c.recv(1024)
    #   print(data)
    #   response = h.handler(data.decode(), c)
    #   if not response:
    #     break
    #   else:
    #     if response['type'] == 'chat':
    #       for t in response['to']:
    #         response.pop('to', None)
    #         t[0].send(json.dumps(response).encode())
    #     else:  
    #       c.send(json.dumps(response).encode())
    # except:
    #   print("clavo")
    #   msg = json.dumps({
    #     'type': "logout"
    #   })
    #   h.handler(msg, c)
    #   break
  c.close()

def main():
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(10)
    print("Socket Listening")
    while True:
      conn, addr = s.accept()
      print("Connected by ", addr)
      start_new_thread(threaded, (conn,))
    s.close()


if __name__ == "__main__":
  main()