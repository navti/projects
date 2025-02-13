import struct
import select
import time

GIVE_ID = 0x22222222
GIVE_ID_N = 42
CLOSE_CONN = 0x11111111
TAIL_BLOCK = 0b01
FOOD_BLOCK = 0b10


def ExpectRecv(connection, n):
    data = b""
    start = time.time()
    while len(data) < n and time.time() - start < 0.5:
        if select.select([connection],[],[], 0.5)[0]:
            data += connection.recv(n - len(data))
    return data


def ReceiveHeader(connection):
    return struct.unpack(">ii", ExpectRecv(connection, 8))


def ReceiveObjects(connection, n_objs):
    # Make sure we only listen if there's somthing to listen for
    if n_objs == 0: return None
    raw_data = ExpectRecv(connection, 4*4*n_objs)
    return grouper(struct.unpack(">"+"i"*(n_objs*4), raw_data), 4)


def grouper(iterable, n):
    # *n replicates the iterator so each .next moves "all" the iterators
    return zip(*[iter(iterable)]*n)
