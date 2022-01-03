MMX Sender
Send test transactions and harvest addresses

https://github.com/retheoff/mmx-sender

First harvest some addresses.
Testnet only have so many addresses and blocks to search.  I pick 50 addresses for now and search through 5000 blocks.

```
usage: mmx-harvest-addresses.py [-h] --start-block START_BLOCK --block-count BLOCK_COUNT --address-count ADDR_COUNT [--mmx-dir MMX_DIR] [--address-file ADDR_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --start-block START_BLOCK
                        Start at block height
  --block-count BLOCK_COUNT
                        Max blocks to loop for harvesting addresses
  --address-count ADDR_COUNT
                        Harvest number of addresses
  --mmx-dir MMX_DIR     Directory containing mmx command: default <homedir>/mmx-node/build
  --address-file ADDR_FILE
                        Full file path to json address file. Default is <homedir>/harvested-mmx-addresses.json

Example with output file and mmx location:
python3 mmx-harvest-addresses.py \
	--mmx-dir /home/greg/src/mmx-node/build \
	--address-file /home/greg/Documents/mmx-addresses.json \
	--start-block 13000 \
	--block-count 100 --address-count 50

Example with defaults:
python3 mmx-harvest-addresses.py \
	--start-block 13000 \
	--block-count 100 --address-count 50

The above defaults to:
--mmx-dir <homedir>/mmx-node/build
--address-file <homedir>/harvested-mmx-addresses.json

```

Then you can do transaction tests.
This will randomize the collected addresses, so you can easily run a few at a time and it will pick from the harvested list at random.

```
usage: mmx-send-test.py [-h] --amount AMOUNT --count COUNT 
  [--delay DELAY] [--mmx-dir MMX_DIR] [--address-file ADDR_FILE] [--iterations ITERATIONS]

optional arguments:
  -h, --help            show this help message and exit
  --amount AMOUNT       Amount to send in MMX
  --count COUNT         Number of addresses to send
  --delay DELAY         Delay between sending each transaction in milliseconds (default 200)
  --mmx-dir MMX_DIR     Directory containing mmx command: default <homedir>/mmx-node/build
  --address-file ADDR_FILE
                        Full file path to json address file. 
						Default is <homedir>/harvested-mmx-addresses.json
  --iterations ITERATIONS
                        Repeat sending count X times (default: 1)

Example with address file and mmx location:
python3 mmx-send-test.py \
	--mmx-dir /home/greg/src/mmx-node/build \
	--address-file /home/greg/Documents/mmx-addresses.json \
	--amount 0.0123 --count 10 --delay 250 --iterations 2

Example with defaults:
python3 mmx-send-test.py --amount 0.0123 --count 10

The above defaults to:
--mmx-dir <homedir>/mmx-node/build
--address-file <homedir>/harvested-mmx-addresses.json
--delay 200
--iterations 1
```