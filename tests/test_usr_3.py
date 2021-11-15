from socket_pair.socket_pair import SockPairs

myself = 'NU'
others = ['Pooja', 'RPI']
# others = ['RPI']
other = 'RPI'

sockObj = SockPairs(myself, others)

sockObj.sync_all()

print(sockObj.listen(other))
sockObj.send({'msg': 'hello back'}, other)

obj = sockObj.listen(other)
