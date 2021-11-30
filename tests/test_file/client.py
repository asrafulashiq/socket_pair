from socket_pair.socket_pair import SockPairs
import time

myself = 'NU'
others = ['Wrapper']

sockObj = SockPairs(myself, others)

# start
sockObj.sync_all()

strt = time.time()
obj = sockObj.listen(frm=others[0])

end = time.time()
print(f"Time passed {end-strt}")