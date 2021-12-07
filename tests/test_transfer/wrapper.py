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
    sockObj.sync_all()
    start = time.time()

    # get N images from stream
    img_list = [np.random.rand(1200, 1200) for _ in range(N)]

    # save stream to a folder as jog images
    os.makedirs('images', exist_ok=True)
    for img_idx, img in enumerate(img_list):
        cv2.imwrite(f'images/{i}_{img_idx}.jpg', img)

    sockObj.sync_all()

    sockObj.sync_all()

    time_passed = time.time() - start
    times.append(time_passed)
    print(f'{i}/{max_iter} - {time_passed}')

print(f'Average time: {np.mean(times)}')