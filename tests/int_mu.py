from socket_pair.socket_pair import SockPairs
import time

myself = 'MU'
others = ['RPI', 'Pooja', 'NU']

sockObj = SockPairs(myself, others)

# start
sockObj.sync_all()

# read frames
sockObj.sync_all()

# process frames
time.sleep(3)

# sync with RPI after pre-processing
sockObj.sync_with('NU')

# NU will read pax results

# batch-end: final sync
sockObj.sync_all()