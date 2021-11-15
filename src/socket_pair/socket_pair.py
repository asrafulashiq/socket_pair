from typing import List, MutableSequence, Optional, Union
import zmq

try:
    from loguru import logger
except ModuleNotFoundError:
    import logging
    FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('socket-server')


def string_to_int(s):
    ord3 = lambda x: '%.3d' % ord(x)
    return int(''.join(map(ord3, s)))


def get_random_port(name: Union[str, List[str]] = '') -> int:
    port = hash(string_to_int(name)) % 100 + 5555
    return port


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

        if self.port is None:
            self.port = get_random_port(''.join(self.names))

        # define who is server and client
        self.server_name = self.names[0]
        self.client_name = self.names[1]

        if name_self is None:
            name_self = names[0]

        if name_self == self.server_name:
            self.init_server()
            self.is_server = True
        else:
            self.init_client()
            self.is_server = False

    def init_server(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.bind("tcp://*:%s" % self.port)
        logger.info(f"Server {self.server_name} started on port {self.port}")

    def init_client(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        self.socket.connect("tcp://localhost:%s" % self.port)
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
