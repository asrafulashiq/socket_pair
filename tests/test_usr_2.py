from socket_pair.socket_pair import SockPairs

myself = 'Pooja'
others = ['NU', 'RPI']
# others = ['RPI']
other = 'RPI'

sockObj = SockPairs(myself, others)

sockObj.sync_all()

sockObj.sync_with(other)

print(sockObj.listen(other))
sockObj.send({'msg': 'hello back'}, other)

obj = sockObj.listen(other)
