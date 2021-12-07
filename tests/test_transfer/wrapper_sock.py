import os
from socket_pair.socket_pair import SockPairs
import time
import numpy as np
import cv2

myself = 'Wrapper'
others = ['RPI']

sockObj = SockPairs(myself, others, is_main=True)

max_iter = 50
N = 40

times = []
sockObj.sync_all()

for i in range(max_iter):
    start = time.time()

    sockObj.sync_all()
    # get N images from stream
    img_list = [np.random.rand(1200, 1200) for _ in range(N)]

    # send img_list to other
    sockObj.send(img_list, to='RPI')

    sockObj.sync_all()

    time_passed = time.time() - start
    times.append(time_passed)
    print(f'{i}/{max_iter} - {time_passed}')

print(f'Average time: {np.mean(times)}')