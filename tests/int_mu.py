from socket_pair.socket_pair import SockPairs
import time

myself = 'MU'
others = ['RPI', 'Wrapper', 'NU']

sockObj = SockPairs(myself, others)

batch = 0

while True:
    print(f"BATCH {batch}")

    # start
    sockObj.sync_all()

    if sockObj.listen('Wrapper') == 'STOP':
        print('No more frames')
        break

    # read frames
    sockObj.sync_all()

    # process frames
    time.sleep(3)

    # sync with NU after pre-processing
    sockObj.sync_with('NU')

    # NU will read pax results

    # batch-end: final sync
    sockObj.sync_all()

    batch += 1