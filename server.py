import socket
from _thread import *
import threading
import json
import server_handler as h

HOST = '127.0.0.1'
PORT = 65432

cards = ["3", "4", "5", "6", "7", "J", "Q", "K", "A", "2"]

print_lock = threading.Lock()

def threaded(c):
  c.send(b"Welcome to President")
  while True:
    data = c.recv(1024)
    response = h.handler(data)
    if not response:
      break
    else:
      c.send(response.encode())
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