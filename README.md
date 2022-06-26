MMX Sender
Send test transactions and harvest addresses

https://github.com/retheoff/mmx-sender

The goal of this is to provide a constant stream of transactions, but not necessarily a benchmark or stress test. 

### You'll need to take 3 steps:

1. Calculate your send job 
    (based on your budget and time/duration of the send job)
2. Harvest addresses from the network
    (this is saved in a json file)
3. Do the send job!

4. Optional: Save a list of your addresses to randomize sending from.


---

**Calcuate a send job:**

```calc_job.py MMX DURATION NBR_ADDR AVG_DELAY_PER_TX```

Calculate the amount (MMX) sent per transaction and number of iterations to simulate.

Example:
I have 500 MMX.
I want it to run for 4 hours.
I have 50 addresses on the network harvested.
I want to set each transaction to have a 525 ms average delay.
```
calc_job.py 500 4 50 525
```

OUTPUT (provides the send job command to run):
```
mmx-send-test.py --amount 0.009960,0.018498 --count 50 --delay 368,682 --iterations 549
```



---

**Harvest some addresses**

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
---
**Then you can do transaction tests.**

This will randomize the collected addresses, so you can easily run a few at a time and it will pick from the harvested list at random.

*NOTE:*

Added support for ranged values in amount and delay using a comma delimiter. For example:

```--amount 0.001,0.002 --delay 300,700```

```
usage: mmx-send-test.py [-h] --amount AMOUNT --count COUNT 
  [--delay DELAY] [--mmx-dir MMX_DIR] [--address-file ADDR_FILE] [--iterations ITERATIONS]

optional arguments:
  -h, --help            show this help message and exit
  --amount AMOUNT       
	Amount to send in MMX
	Optionally use a range split by comma:
		--amount 0.001,0.002
  
  --count COUNT         Number of addresses to send
  
  --delay DELAY         
     Delay between sending each
	 transaction in milliseconds 
	 (default 200) 
	 Optionally use a range split by comma:
		--delay 300,700
		
  --mmx-dir MMX_DIR     
  	Directory containing mmx command: 
		default <homedir>/mmx-node/build
		
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


Example using ranges (output by calc_job.py):
mmx-send-test.py --amount 0.009960,0.018498 \
  --count 50 --delay 368,682 --iterations 549

```

---

**Save a list of your own addresses:**

```
get_my_addresses.py
```
All this does is run "mmx wallet show 50".
Then saves your addresses from that output to $HOME/my_mmx_addresses.json

If this is detected by the mmx-send-test.py script it will be used to randomize the source address in transaction sending, using your wallet addresses.
