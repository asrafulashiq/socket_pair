from socket_pair.socket_pair import SockPairs
import time

myself = 'NU'
others = ['RPI', 'Wrapper']
other = 'RPI'

sockObj = SockPairs(myself, others)

# start
sockObj.sync_all()

sockObj.sync_all()
# read frames

# process frames
time.sleep(1)

# sync with RPI after pre-processing
sockObj.sync_with('RPI')

# NU will read bin results

# NU will sync with MU and read MU results
# sockObj.sync_with('MU')

# NU finishes processing RPI and MU
# sync with RPI to send results
sockObj.sync_with('RPI')

# batch-end: final sync
sockObj.sync_all()