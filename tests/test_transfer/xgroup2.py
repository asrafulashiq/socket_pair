from socket_pair.socket_pair import SockPairs
import time
import cv2
import numpy as np

myself = 'RPI'
others = ['Wrapper']

sockObj = SockPairs(myself, others)

max_iter = 50
N = 40
sockObj.sync_all()

times = []
for i in range(max_iter):
    start = time.time()

    sockObj.sync_all()

    sockObj.sync_all()
    imgs = np.load('imgs.npy')

    sockObj.sync_all()

    time_passed = time.time() - start
    print(f'{i}/{max_iter} {time_passed}')
    times.append(time_passed)

print(f'Average time: {np.mean(times)}')