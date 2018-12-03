import socket
import select
import sys


def usage():
  print("syntax : echoclient <host> <port>")
  print("sample : echoclient 127.0.0.1 1234")

def main():
  # syntax error
  if len(sys.argv) != 3:
    usage()
    sys.exit(1)

  host = sys.argv[1]
  port = sys.argv[2]

  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    client_socket.connect((host, int(port)))
  except Exception as e:
    print("I couldn't make a connection to server %s:%s" % (host, port))
    sys.exit(1)
  print("A connection to server %s:%s is built successfully" % (host, port))

  while True:
    try:
      # sys.stdin is stream for input
      connection_list = [sys.stdin, client_socket]
      # rlist => read_socket: wait until ready for reading
      # wlist => write_socket: wait until ready for writing
      # xlist => error_socket: wait for an exceptional condition
      # unlock blocking state per 10seconds
      read_socket, write_socket, error_socket = select.select(connection_list, [], [], 10)

      for ob in read_socket:
        if ob == client_socket:
          data = ob.recv(1024)
          if data:
            print("A message from server: " + data)
                  
          else:
            print("A connection with server %s:%s is disconnected." %(host, port))
            client_socket.close()
            sys.exit(1)
            
        else:
          message = raw_input()
          client_socket.send(message)

    except KeyboardInterrupt:
      client_socket.close()
      sys.exit(1)

if __name__ == "__main__":
  main()


