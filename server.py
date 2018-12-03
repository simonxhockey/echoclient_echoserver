import socket
import select
import sys


def usage():
    print("syntax : echoserver <port> [-b]")
    print("sample : echoserver 1234 -b")

def main():
    # option is for broadcasting
    # if option is false, the message is not going to be broadcasted
    option = False

    # if the broadcast option is turn-on
    if len(sys.argv) == 3 and sys.argv[2] == "-b":
        option = True
    # syntax error
    elif len(sys.argv) != 2:
        usage()
        sys.exit(1)

    host = "localhost"
    port = sys.argv[1]

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, int(port)))
    server_socket.listen(10)
    # we don't need input
    connection_list = [server_socket]

    while connection_list:
        try:
            # rlist => read_socket: wait until ready for reading
            # wlist => write_socket: wait until ready for writing
            # xlist => error_socket: wait for an exceptional condition
            # unlock blocking state per 10seconds
            read_socket, write_socket, error_socket = select.select(connection_list, [], [], 10)

            for ob in read_socket:
                # new request
                if ob == server_socket:
                    (client_socket, address) = server_socket.accept()
                    connection_list.append(client_socket)
                    print("New client %s is connected." % address[0])

                # any data from client
                else:
                    data = ob.recv(1024)
                    if data:
                        print("I got the message [%s] from client." % data)
                        if option == False:
                            ob.send(data)
                        # send message to all connected clients
                        else:
                            for clients in connection_list:
                                if clients != server_socket:
                                    clients.send(data)

                    # if client broke the connection
                    else:
                        connection_list.remove(ob)
                        print("A connection with client %s is disconnected." % address[0])
                        ob.close()

        except KeyboardInterrupt:
            server_socket.close()
            sys.exit()

if __name__ == "__main__":
    main()

