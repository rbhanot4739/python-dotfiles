import socket
import select

import sys

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # This is to prevent the socket going into TIME_WAIT status and OSError "Address already in use"
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 50000)
    server.bind(server_address)
    print('**** Server started on {}: {} ****'.format(*server_address))
    server.listen(5)

except socket.error as e:
    print('Error occurred while creating the socket {}'.format(e))

inputs = [server]
outputs = []

# TODO - Figure a way to handle peer to peer connections

try:
    while inputs:
        readable, writable, error = select.select(inputs, outputs, [])

        for sock in readable:
            if sock is server:
                client, _ = sock.accept()
                total_clients = [i.getpeername() for i in inputs if i is not sock]
                inputs.append(client)
                msg = 'Other users in the chatroom {}'.format(total_clients)
                print(msg)
                client.sendall(bytes(msg, 'utf-8'))
            else:
                data = sock.recv(1024).decode()
                if data:
                    print(data)
                    if sock not in outputs:
                        outputs.append(sock)
                else:
                    print('Client disconnected')
                    sock.close()
                    inputs.remove(sock)


except KeyboardInterrupt:
    server.close()
    sys.exit('ctrl-c issues!!')
