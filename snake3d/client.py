import socket
import struct

from network_utils import *

s = socket.socket()
s.connect(("localhost", 4588))

# Initial handshake
s.send(struct.pack(">ii", GIVE_ID, GIVE_ID_N))
d = s.recv(4)
my_id = struct.unpack(">i", d)[0]
print("My id is: {%d}"%my_id)

while True:
    x = input("x> ")
    y = input("y> ")
    z = input("z> ")
    header = struct.pack(">ii", my_id, 3)
    data = struct.pack(">iiii", 0b10, int(x), int(y), int(z))
    s.send(header+data*3)

    n_user_data_objects = struct.unpack(">i", s.recv(4))[0]
    print("There are %d user data objects coming"%n_user_data_objects)
    for i in range(n_user_data_objects):
        user_id, n_objs = ReceiveHeader(s)
        print(user_id, n_objs)
        values = ReceiveObjects(s, n_objs)
        print(grouper(values, 4))
