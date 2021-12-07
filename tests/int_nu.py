from socket_pair.socket_pair import SockPairs
import time

myself = 'NU'
others = ['RPI', 'Wrapper', 'MU']

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

    # sync with RPI after pre-processing
    sockObj.sync_with('RPI')

    # NU will read bin results

    # NU will sync with MU and read MU results
    sockObj.sync_with('MU')

    # NU finishes processing RPI and MU
    # sync with RPI to send results
    sockObj.sync_with('RPI')

    # batch-end
    sockObj.sync_all()

    batch += 1