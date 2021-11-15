def get_random_port(name: str = '') -> int:
    port = hash(name) % 100 + 5555
    return port
