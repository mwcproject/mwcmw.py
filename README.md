# mwcmw.py

mwc is a privacy-preserving digital currency built openly by developers distributed all over the world. Check [mwc.mw](https://mwc.mw/) to know more!

This module provides Python wrappers for

* [MWC Wallet API V3](https://docs.mwc.mw/wiki/api/wallet-api/)
* [MWC Node API V2](https://docs.mwc.mw/wiki/api/node-api/)

If you need help please check how to reach our [community](https://mwc.mw/community).

## Examples

Using the Node V2 API to access the locally running mwc node.

```python
from mwcmw.node_v2 import NodeV2

import pprint
from pathlib import Path
home = str(Path.home())

pp = pprint.PrettyPrinter(indent=4)
owner_api_url = 'http://localhost:3413/v2/owner'

# change to your mwc owner_api secret file
owner_api_sercet_file = os.path.join(home, '.mwc/main/.api_secret')
owner_api_user = 'mwcmain'
owner_api_password = open(owner_api_sercet_file).read().strip()

foreign_api_url = 'http://localhost:3413/v2/foreign'

# change to your mwc owner_api sercret file
foreign_api_sercet_file = os.path.join(home, '.mwc/main/.foreign_api_secret')
foreign_api_user = 'mwcmain'
foreign_api_password = open(foreign_api_sercet_file).read().strip()

node = NodeV2( foreign_api_url, foreign_api_user, foreign_api_password, owner_api_url, owner_api_user, owner_api_password)
pp.pprint(node.get_status())
pp.pprint(node.get_header(1036985))
pp.pprint(node.get_kernel('096a7303ab9e3a68cf0b3d70d6ec61311efaf0f33f2ac251bff2a4da45908d3f15'))
pp.pprint(node.get_kernel('08f0a2b7e3ddd0ccc60ac147e93f3e8b01ede591d0da08ba93333e3c73fd45c1cf'))
```

Using the Wallet V3 API to access the locally running mwc wallet listener.

```python
from mwcmw.wallet_v3 import WalletV3

import pprint, os

pp = pprint.PrettyPrinter(indent=4)
api_url = 'http://localhost:3420/v3/owner'

# change to your mwc owner_api sercret file
api_sercet_file = '/home/ubuntu/.mwc/main/.owner_api_secret'
api_user = 'mwc'
api_password = open(api_sercet_file).read().strip()
wallet = WalletV3(api_url, api_user, api_password)
wallet.init_secure_api()

# change to you wallet password
wallet_password = '123'

wallet.open_wallet(None, wallet_password)
pp.pprint(wallet.node_height())
pp.pprint(wallet.get_slatepack_address())

# send to gate.io
send_args = {
    'src_acct_name': None,
    'amount': int(2.67020546 * 1000000000),
    'minimum_confirmations': 10,
    'max_outputs': 500,
    'num_change_outputs': 1,
    'selection_strategy_is_use_all': False,
    'target_slate_version': None,
    'payment_proof_recipient_address': 'mwc1n26np6apy07576qx6yz4qayuwxcpjvl87a2mjv3jpk6mnyz8y4vq65ahjm',
    'ttl_blocks': None,
    'send_args': {
        "dest": 'mwc1n26np6apy07576qx6yz4qayuwxcpjvl87a2mjv3jpk6mnyz8y4vq65ahjm',
        "post_tx": True,
        "fluff": True,
        "skip_tor": False
    }
}
print(wallet.init_send_tx(send_args))
```

More examples in examples folder.
