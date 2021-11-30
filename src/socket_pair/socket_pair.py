from typing import List, MutableSequence, Optional, Union
import zmq
import pickle
import psutil
import numpy as np

try:
    from loguru import logger
except ModuleNotFoundError:
    import logging
    FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('socket-server')

TMP_FILE = '/tmp/tmp_clasp_ports.pkl'


class FreePort():
    def __init__(self) -> None:
        self.rng = np.random.RandomState(0)

    def getfreeports(self, num_ports=10):
        port = self.rng.randint(49152, 65535)
        portsinuse = []
        ports = []
        while True:
            conns = psutil.net_connections()
            for conn in conns:
                portsinuse.append(conn.laddr[1])
            if port in portsinuse or port in ports:
                port = self.rng.randint(49152, 65535)
            else:
                ports.append(port)
            if len(ports) == num_ports:
                break
        return ports


class SockPairs(object):
    def __init__(self,
                 name_self: str = 'RPI',
                 name_other: List[str] = ['NU', 'MU', 'Wrapper'],
                 is_main=False,
                 verbose=False):
        self.name_self = name_self
        self.verbose = verbose
        self.is_main = is_main

        if isinstance(name_other, str):
            name_other = [name_other]
        name_other = list(sorted(name_other))
        self.name_other = name_other

        all_names = [name_self] + name_other
        if is_main:
            ports = self.create_port_pair(all_names)
        else:
            ports = self.read_ports()

        # Create pairs of sockets
        self.sock_pairs = {}
        for name in self.name_other:
            _port = ports[tuple(sorted((name, self.name_self)))]
            self.sock_pairs[name] = _SocketPair(name,
                                                self.name_self,
                                                port=_port,
                                                verbose=self.verbose)

    def create_port_pair(self, names: List[str]) -> int:
        import itertools as it
        names = tuple(sorted(names))
        ports = {}
        pairs = list(it.combinations(names, 2))

        all_ports = FreePort().getfreeports(num_ports=len(pairs))
        for i, pair in enumerate(pairs):
            ports[pair] = all_ports[i]

        pickle.dump(ports, open(TMP_FILE, 'wb'))
        return ports

    def read_ports(self) -> dict:
        with open(TMP_FILE, 'rb') as f:
            ports = pickle.load(f)
        return ports

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
        if self.verbose:
            logger.info('All groups are in sync')

    def sync_with(self, name: str):
        if name not in self.name_other:
            raise ValueError(f'No connection established between {name}')
        self.sock_pairs[name].sync()


class _SocketPair(object):
    def __init__(self,
                 name_other: Optional[str] = 'B',
                 name_self: Optional[str] = 'A',
                 port: Optional[int] = None,
                 verbose=True) -> None:
        names = [name_other, name_self]
        assert len(names) == 2

        self.name_self = name_self
        self.name_other = name_other
        self.names = sorted(list(names))
        self.port = port
        self.verbose = verbose

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
        if self.verbose:
            logger.debug(msg)

    def finish(self) -> None:
        self.socket.close()
        self.context.term()
