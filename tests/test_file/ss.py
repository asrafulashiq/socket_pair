from socket_pair.socket_pair import SockPairs
import time
import numpy as np

myself = 'Wrapper'
others = ['NU']

arr = np.random.rand(120, 1280, 1040, 3)

sockObj = SockPairs(myself, others, is_main=True)

# start
sockObj.sync_all()

sockObj.send(arr, to=others[0])