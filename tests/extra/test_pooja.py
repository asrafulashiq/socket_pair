from socket_pair.socket_pair import SockPairs
import time

myself = 'Wrapper'
others = ['NU', 'RPI']
# others = ['Wrapper']
other = 'RPI'

sockObj = SockPairs(myself, others)

# start
sockObj.sync_all()

# store frames
sockObj.sync_all()

time.sleep(1)

# batch-end: final sync
sockObj.sync_all()