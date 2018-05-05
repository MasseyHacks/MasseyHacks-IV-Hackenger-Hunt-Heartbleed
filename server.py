import socket
import pickle
import uuid
import traceback
import multiprocessing

with open('data.meme') as file:
    dump = file.read()

def bleed(text, size):
    return text[:min(max(size, 0), len(text))] + dump[:max(size - len(text), 0)]

def comm(conn, addr):

    try:
        message = pickle.loads(conn.recv(10240))

        print('Incoming message from %s: %s' % (str(addr), str(message)))

        o = bleed(message[0], int(message[1]))

        print(len(o))

        #conn.sendall(bytes(o, 'utf-8'))
        conn.send(pickle.dumps(bleed(message[0], int(message[1]))))
    except:
        conn.sendall(pickle.dumps(str(uuid.uuid4())))
        traceback.print_exc()

    conn.close()

if __name__ == '__main__':
    # do stuff

    connections = {}

    HOST = '192.168.4.1'
    PORT = 1511

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(999999)

    print('Server running on [%s:%i]' % (HOST, PORT))

    while True:

        try:

            conn, addr = server.accept()

            print('Incoming connection from [%s]' % str(addr))

            connections[addr] = multiprocessing.Process(target=comm, args=(conn, addr)).run()

        except:
            pass
