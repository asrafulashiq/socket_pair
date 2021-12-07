from socket_pair.socket_pair import SockPairs
import time

myself = 'Wrapper'
others = ['NU', 'RPI', 'MU']

sockObj = SockPairs(myself, others, is_main=True)

batch = 0

while True:
    print(f"BATCH {batch}")

    # batch start
    sockObj.sync_all()

    # store frames
    time.sleep(1)

    # is end-of-frames?
    if batch == 3:
        sockObj.send_all('STOP')
        break
    else:
        sockObj.send_all('CONT')

    # frames ready
    sockObj.sync_all()

    time.sleep(1)

    # batch-end
    sockObj.sync_all()

    batch += 1