# Socket-Pair

## Installation

First, install `socket_pair` package.

```bash
pip install git+https://github.com/asrafulashiq/socket_pair
```

## Instruction

### Initialization

- Import library:
  
  ```python
  from socket_pair.socket_pair import SockPairs
  ```

- All teams should initialize `sockObj` first. For example, for `RPI`, it should be:

  ```python
  sockObj = SockPairs(name_self='RPI', 
                      name_other=['NU', 'MU', 'Pooja'])
  ```

  And for `MU`:

  ```python
  sockObj = SockPairs(name_self='MU', 
                      name_other=['NU', 'RPI', 'Pooja'])
  ```

  And for `NU`:

  ```python
  sockObj = SockPairs(name_self='NU', 
                      name_other=['MU', 'RPI', 'Pooja'])
  ```

  And for Pooja, 

  ```python
  sockObj = SockPairs(name_self='Pooja', 
                      name_other=['NU', 'RPI', 'MU'])
  ```


### Synchronization

For synchronization between groups, there are two functions: `sync_all` and `sync_with`.

### **`sync_all`**

Each team should call `sync_all` three times:

1. At the beginning of batch, so that everyone starts from the same line
2. When Pooja copies the frames for processing
3. When everyone finishes the batch processing 

Hence, Pooja's code should look like:

```python
sockObj.sync_all()  # batch start

# Pooja copies the current batch in a folder for the group to process
# and then call
sockObj.sync_all()

# ...

# End of batch, sync here 
sockObj.sync_all()

```

Codes for other groups should look like:

```python
# start batch
sockObj.sync_all()

# wait to sync here so that next batch from Pooja is ready
sockObj.sync_all()

# Read the frames after sync_all

# ... 

# End of batch, sync here 
sockObj.sync_all()
```

### **`sync_with`**

`sync_with` is called when two groups want to be in sync with each other. In our setting, this happens in the following cases:

- When `MU` finishes person processing, `MU` should let `NU` know that the person processing is done and they should be in sync. The code block for `MU` should be:
  
  ```python
    # ... 
    # finished person processing
    # and then call:
    sockObj.sync_with('NU')
    # ...
  ```

  And NU's code should look like:
  
  ```python
    # ...
    # finish pre-processing for action detection
    sockObj.sync_with('MU')

    # Read MU's PAX results
    # ...

  ```

- When `RPI` finishes bin processing, `RPI` and `NU` should be in sync. RPI's code:
  
  ```python
    # ...
    # finished bin processing
    sockObj.sync_with('MU')

    # ...
  ```

  And NU's code should look like:
  
  ```python
    # ...
    # finished pre-processing for action detection
    # and then call:
    sockObj.sync_with('RPI')

    # read bin results from RPI

    # ...
  ```
