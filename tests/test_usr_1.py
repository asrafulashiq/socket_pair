from socket_pair.socket_pair import SockPairs

myself = 'RPI'
others = ['NU', 'Pooja']
# others = ['Pooja']
other = 'Pooja'

sockObj = SockPairs(myself, others)

sockObj.sync_all()

sockObj.sync_with(other)

sockObj.send({'msg': 'hello'}, other)
print(sockObj.listen(other))

import seaborn as sns
dat = sns.load_dataset('iris')

sockObj.send(dat, other)

# bin_dataframe = {}

# # # ------------------------------------ RPI ----------------------------------- #

# sockObj = SockPairs('RPI', ['NU', 'MU'])

# # Bin detection and Tracking
# ...

# sockObj.send({'Bin_Processed': True}, 'NU')

# # bin_dataframe is a pandas dataframe with
# # with bin information
# sockObj.send(bin_dataframe, 'NU')

# # ------------------------------------ NU ------------------------------------ #
# sockObj = SockPairs('NU', ['RPI', 'MU'])

# # NU Preprocessing

# msg = sockObj.listen('RPI')
# if msg['Bin_Processed']:
#     # NU uses the bin id
#     bin_dataframe = sockObj.listen('RPI')