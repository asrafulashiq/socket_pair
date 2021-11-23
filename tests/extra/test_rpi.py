from socket_pair.socket_pair import SockPairs
import time

myself = 'RPI'
others = ['NU', 'Wrapper']
# others = ['Wrapper']
other = 'NU'

sockObj = SockPairs(myself, others)

# start
sockObj.sync_all()

sockObj.sync_all()
# read frames

time.sleep(1)

# sync with NU after processing bins
sockObj.sync_with('NU')
# NU will read bin results

# NU finishes processing RPI and MU
sockObj.sync_with('NU')

# create feed

# batch-end: final sync
sockObj.sync_all()