from socket_pair.socket_pair import SockPairs
import time

myself = 'Pooja'
others = ['NU', 'RPI', 'MU']

sockObj = SockPairs(myself, others)

# start
sockObj.sync_all()

# store frames
time.sleep(1)
sockObj.sync_all()

time.sleep(1)

# batch-end: final sync
sockObj.sync_all()