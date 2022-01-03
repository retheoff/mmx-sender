#!/usr/bin/env python3
import sys,os,time
import json
import subprocess
import argparse
import platform
import textwrap




def run(pargs):
	indexArgs = lambda key: getattr(pargs,key) if hasattr(pargs,key) else None
	STARTBLOCK = int(indexArgs('start_block')) if (indexArgs('start_block') != None) else 1
	COUNT = int(indexArgs('addr_count')) if (indexArgs('addr_count') != None) else 25
	MAXBLOCKS = int(indexArgs('block_count')) if (indexArgs('block_count') != None) else 50

	MMXDIR = indexArgs('mmx_dir') if (indexArgs('mmx_dir') != None) else os.environ['HOME'] + "/mmx-node/build"
	MMXCMD = MMXDIR + "/mmx"

	addrs = set()
	block = STARTBLOCK
	c = 1
	while len(addrs) < COUNT:
		print('Block: ' + str(block)  + ' block count: ' + str(c) + ' addresses found: ' + str(len(addrs)) )
		result = subprocess.run([MMXCMD, 'node', 'get', 'block', str(block)], capture_output=True, text=True).stdout
		if result is not None:
			j = json.loads(result)
			if j is None:
				continue
			# print(str(block))
			if j['tx_base'] is not None:
				for x in j['tx_base']['outputs']:
					print(x['address'])
					addrs.add(x['address'])
		block += 1
		c += 1
		if c > MAXBLOCKS:
			break


	outfile = os.environ['HOME'] + '/harvested-mmx-addresses.json'
	outfile = indexArgs('addr_file') if (indexArgs('addr_file') != None) else outfile
	

	output = list(addrs)
	json.dump(output, open(outfile, 'w'))

	return 0



def main():
	doc = textwrap.dedent("""\


		Example with output file and mmx location:
		python3 mmx-harvest-addresses.py \\\r
			--mmx-dir /home/greg/src/mmx-node/build \\\r
			--address-file /home/greg/Documents/mmx-addresses.json \\\r
			--start-block 13000 \\\r
			--block-count 100 --address-count 50

		Example with defaults:
		python3 mmx-harvest-addresses.py \\\r
			--start-block 13000 \\\r
			--block-count 100 --address-count 50

		The above defaults to:
		--mmx-dir <homedir>/mmx-node/build
		--address-file <homedir>/harvested-mmx-addresses.json
			

		""")

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,epilog=doc)
	# parser._action_groups.pop()
	# parser.add_argument('--help', required=False, dest="help",
	# 	help='Show this help')
	parser.add_argument('--start-block', required=True, dest="start_block",
		help='Start at block height')
	parser.add_argument('--block-count', required=True, dest="block_count",
		help='Max blocks to loop for harvesting addresses')
	parser.add_argument('--address-count', required=True, dest="addr_count",
		help='Harvest number of addresses')

	parser.add_argument('--mmx-dir', required=False, dest="mmx_dir",
		help='Directory containing mmx command: default <homedir>/mmx-node/build')

	parser.add_argument('--address-file', required=False, dest="addr_file",
		help='Full file path to json address file. Default is <homedir>/harvested-mmx-addresses.json')

	try:
		pargs = parser.parse_args()
		indexArgs = lambda key: getattr(pargs,key) if hasattr(pargs,key) else None
		start_block = indexArgs('start_block')

		print(start_block)

		return run(pargs)

		
	except Exception as e:
		print(e)
		return 1

	return 0


if __name__ == "__main__":
	v = main()
	if(v >= 0):
		#print "Received exit code: " + str(v)
		sys.exit(v)
	else:
		#print "Not Received exit code: " + str(v)
		sys.exit()