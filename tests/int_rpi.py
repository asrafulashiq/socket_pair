from socket_pair.socket_pair import SockPairs
import time

myself = 'RPI'
others = ['NU', 'Pooja', 'MU']

sockObj = SockPairs(myself, others)

# start
sockObj.sync_all()

sockObj.sync_all()
# read frames
time.sleep(3)

# sync with NU after processing bins
sockObj.sync_with('NU')
# NU will read bin results

# NU finishes processing RPI and MU
sockObj.sync_with('NU')

# create feed
time.sleep(3)

# batch-end: final sync
sockObj.sync_all()