
<div align="center">

# **Bittensor Map Reduce** <!-- omit in toc -->
[![Discord Chat](https://img.shields.io/discord/308323056592486420.svg)](https://discord.com/channels/799672011265015819/1163969538191269918)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

---

### The Incentivized Internet <!-- omit in toc -->

[Discord](https://discord.gg/bittensor) • [Network](https://taostats.io/) • [Research](https://bittensor.com/whitepaper)

</div>

# User Guide

```bash
git clone https://github.com/dream-well/map-reduce-subnet
cd map-reduce-subnet
python -m pip install -e .
```




```python
import torch
import time
from mapreduce.peer import Peer
import bittensor as bt
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--validator.uid', type = int, default=-1, help='Validator UID')
parser.add_argument('--rank', type = int, default=1, help='Rank of the peer')
parser.add_argument('--count', type = int, default=1, help='Number of peers')

bt.subtensor.add_args(parser)
bt.logging.add_args(parser)
bt.wallet.add_args(parser)

config = bt.config(
    parser=parser
)

wallet = bt.wallet(config=config)

# maximum transfer size
bandwidth = 100 * 1024 * 1024

def train(rank, peer_count, bandwidth, wallet, validator_uid, network ):
    bt.logging.info(f"🔷 Starting peer with rank {rank}")
    # Initialize Peer instance
    peer = Peer(rank, peer_count, bandwidth, wallet, validator_uid, network)

    # Initialize process group with the fetched configuration
    peer.init_process_group()

    weights = None

    if rank == 1: # if it is the first peer
        weights = torch.rand((tensor_size, 1), dtype=torch.float32)
        # First peer broadcasts the weights
        peer.broadcast(weights)
    else:
        # Other peers receive the weights
        weights = peer.broadcast(weights)
    
    # Should destroy process group after broadcasting
    peer.destroy_process_group()

    # Number of epochs
    epoch = 2

    # Your training loop here
    bt.logging.info(f"Peer {rank} is training...")   
    
    for i in range(epoch):

        bt.logging.success(f"🟢 Epoch: {i}")
        
        # Replace this with actual training code
        time.sleep(5)
        
        # After calculating gradients
        gradients = torch.ones((tensor_size, 1), dtype=torch.float32)
        
        if rank == 1:
            gradients = torch.ones((tensor_size, 1), dtype=torch.float32) * 3
        
        # Initialize process group
        peer.init_process_group()
        
        # All-reducing the gradients (average of gradients)
        gradients = peer.all_reduce(gradients)
        
        # Destroy process group
        peer.destroy_process_group()
    
    bt.logging.success(f"Peer {rank} has finished training.")

if __name__ == '__main__':
    train(config.rank, config.peer_count, bandwidth, wallet, config.validator.uid, config.subtensor.network)

```

User also can test the map-reduce subnet by running test.py
```bash
python3 test/test.py --subtensor.network local --wallet.name <wallet name> --wallet.hotkey <hotkey name> --validator.uid <validator uid>
```


## License
This repository is licensed under the MIT License.
```text
# The MIT License (MIT)
# Copyright © 2023 ChainDude

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
```

