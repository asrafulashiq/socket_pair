# Socket-Pair

## Installation

First, install `pyzmq` package.

```bash
pip install pyzmq
```

Copy `socket_pair.py` in the working directory.

## Instruction

### Initialization

All groups should initialize `sockObj` first. For example, for `RPI`, is shoulds be:

```python
sockObj = SockPairs(name_self='RPI', 
                    name_other=['NU', 'MU', 'Pooja'])
```

And for `MU`:

```python
sockObj = SockPairs(name_self='MU', 
                    name_other=['NU', 'RPI', 'Pooja'])
```

After initializing the python object, all groups will call:

```python
sockObj.sync_all()
```

This ensures that everyone is one the same line and the communication is working properly.


### Synchronization

For synchronization between groups, there are two functions: `sync_all` and `sync_with`.

