from typing import List, MutableSequence, Optional, Union
import zmq
import socket

try:
    from loguru import logger
except ModuleNotFoundError:
    import logging
    FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('socket-server')


def is_port_open(port: int) -> bool:
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)

    res = False
    if result_of_check == 0:
        print("Port is open")
        res = True
    else:
        print("Port is not open")
        res = False
    a_socket.close()
    return res


def string_to_int(s):
    ord3 = lambda x: '%.3d' % ord(x)
    return int(''.join(map(ord3, s)))


def get_random_port(name: Union[str, List[str]] = '') -> int:
    port = hash(string_to_int(name)) % 100 + 5555
    return port


import psutil
import numpy as np


class FreePort():
    def __init__(self, name, is_server=True) -> None:
        seed = hash(string_to_int(name)) % 2**32
        self.rng = np.random.RandomState(seed)
        self.is_server = is_server

    def getfreeport(self):
        port = self.rng.randint(49152, 65535)
        if not self.is_server:
            return port
        portsinuse = []
        while True:
            conns = psutil.net_connections()
            for conn in conns:
                portsinuse.append(conn.laddr[1])
            if port in portsinuse:
                port = self.rng.randint(49152, 65535)
            else:
                break
        return port

    def __call__(self):
        return self.getfreeport()


class SockPairs(object):
    def __init__(self,
                 name_self: str = 'RPI',
                 name_other: List[str] = ['NU', 'MU', 'Pooja']):
        self.name_self = name_self

        if isinstance(name_other, str):
            name_other = [name_other]

        self.name_other = name_other

        # Create pairs of sockets
        self.sock_pairs = {}
        for name in self.name_other:
            self.sock_pairs[name] = _SocketPair(name, self.name_self)

    def send(self, msg: Union[str, dict], to: Optional[str] = None):
        if isinstance(to, MutableSequence):
            for t in to:
                self.sock_pairs[t].send(msg)
        else:
            self.sock_pairs[to].send(msg)

    def listen(self, frm: Optional[str] = None) -> Union[str, dict]:
        return self.sock_pairs[frm].listen()

    def send_all(self, msg: Union[str, dict]):
        self.send(msg, self.name_other)

    def sync_all(self):
        for name in self.name_other:
            self.sock_pairs[name].sync()
        logger.info('All groups are in sync')

    def sync_with(self, name: str):
        if name not in self.name_other:
            raise ValueError(f'No connection established between {name}')
        self.sock_pairs[name].sync()


class _SocketPair(object):
    def __init__(self,
                 name_other: Optional[str] = 'B',
                 name_self: Optional[str] = 'A',
                 port: Optional[int] = None) -> None:
        names = [name_other, name_self]
        assert len(names) == 2

        self.name_self = name_self
        self.name_other = name_other
        self.names = sorted(list(names))
        self.port = port

        # define who is server and client
        self.server_name = self.names[0]
        self.client_name = self.names[1]
        self.is_server = name_self == self.server_name

        if self.port is None:
            self.port = FreePort(''.join(self.names),
                                 is_server=self.is_server).getfreeport()
            logger.debug(
                f"port between {self.names[0]} & {self.names[1]}: {self.port}")

        if name_self is None:
            name_self = names[0]

        if name_self == self.server_name:
            self.init_server()
        else:
            self.init_client()

    def init_server(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        while True:
            try:
                self.socket.bind("tcp://*:%s" % self.port)
            except zmq.error.ZMQError:
                logger.error(f'Port {self.port} is already in use')
                self.port += 1
            else:
                break

        logger.info(f"Server {self.server_name} started on port {self.port}")

    def init_client(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        while True:
            try:
                self.socket.connect("tcp://localhost:%s" % self.port)
            except zmq.error.ZMQError:
                logger.error(f'Port {self.port} is already in use')
                self.port += 1
            else:
                break

        logger.info(
            f"Client {self.client_name} Connected to server {self.server_name} on port {self.port}"
        )

    def send(self, msg: Union[dict, str]) -> None:
        self.socket.send_pyobj(msg)

    def listen(self) -> Union[str, dict]:
        msg = self.socket.recv_pyobj()
        return msg

    def sync(self):
        sync_msg = f'sync between {self.names[0]} and {self.names[1]}'
        self.send(sync_msg)
        msg = self.listen()
        print(msg)

    def finish(self) -> None:
        self.socket.close()
        self.context.term()
