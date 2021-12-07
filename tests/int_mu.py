from socket_pair.socket_pair import SockPairs
import time

myself = 'MU'
others = ['RPI', 'Wrapper', 'NU']

sockObj = SockPairs(myself, others)

batch = 0

while True:
    print(f"BATCH {batch}")

    # batch start
    sockObj.sync_all()

    if sockObj.listen('Wrapper') == 'STOP':
        print('No more frames')
        break

    # read frames after sync_all
    sockObj.sync_all()

    # process frames
    time.sleep(3)

    # sync with NU after pre-processing
    sockObj.sync_with('NU')

    # NU will read pax results

    # batch-end
    sockObj.sync_all()

    batch += 1