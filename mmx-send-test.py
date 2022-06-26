#!/usr/bin/env python3
import sys,os,time
import json
import subprocess
import argparse
import platform
import textwrap
import random

def quickPopen(cmd):
	cmd = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	out, err = cmd.communicate()
	return out, err

def run(pargs):
	indexArgs = lambda key: getattr(pargs,key) if hasattr(pargs,key) else None
	outfile = os.environ['HOME'] + '/harvested-mmx-addresses.json'
	outfile = indexArgs('addr_file') if (indexArgs('addr_file') != None) else outfile
	addrsfile = os.environ['HOME'] + '/my_mmx_addresses.json'
	if os.path.isfile(addrsfile):
		myaddrs = json.load(open(addrsfile, 'r'))
		print('Found addrs')
	else:
		myaddrs = None
	
	MMXDIR = indexArgs('mmx_dir') if (indexArgs('mmx_dir') != None) else os.environ['HOME'] + "/mmx-node/build"
	MMXCMD = MMXDIR + "/mmx"

	def get_value_selector(arg, default_value, dtype=float):
		index_arg = indexArgs(arg)
		if index_arg is None:
			return lambda: dtype(default_value)
		elif ',' in index_arg:
			value_range = index_arg.split(',')
			if len(value_range) != 2:
				print(f'Range format is invalid.  Received: {index_arg}')
			else:
				vmin, vmax = map(dtype, value_range)
				vrange = vmax - vmin
				return lambda: vmin + vrange * random.random()
				# This is random linear interpolation between vmin and vmax.
		return lambda: dtype(index_arg)
	
	getAmount = get_value_selector('amount', 0)
	getDelay = get_value_selector('delay', 200, dtype=int)
	
	#amount = float(indexArgs('amount')) if (indexArgs('amount') != None) else 0
	count = int(indexArgs('count')) if (indexArgs('count') != None) else 0

	#delay = float(indexArgs('delay')) if (indexArgs('delay') != None) else 200
	# print("Selected delay: " + str(delay))
	#if delay > 0:
	#	delay = delay / 1000

	loop = int(indexArgs('iterations')) if (indexArgs('iterations') != None) else 1

	with open(outfile) as f:
		data = json.load(f)

	
	#print("Sending transactions: " + str(count) + " Iterations: " + str(loop))
	#print("Delaying txs: " + str(delay))
	loop_count = 0
	
	while loop_count < loop:
		print("---- Begin tx loop: " + str(loop_count + 1) + "---")
		random.shuffle(data)
		for c,address in enumerate(data):
			delay = getDelay()
			if(c >= 1 or loop_count >= 1):
				time.sleep(getDelay() * 0.001)
				# Multiply by 0.001 to convert milliseconds to seconds
				# because user inputs milliseconds and time.sleep() expects seconds
			else:
				delay = 0
			
			# print(loop_count)
			print(f"[{loop_count:05d}|{loop:05d}] ({c+1}) Sending transaction with delay: {delay:.0f} ms")
			
			try:
				cmd = [MMXCMD, 'wallet', 'send', '-a', f'{getAmount():.8f}', '-t', address]
				if myaddrs is not None and len(myaddrs) > 0:
					cmd += ['-s', random.choice(myaddrs)]
				print("{0}".format(' '.join(cmd)))
				proc = subprocess.Popen(cmd,
					stdout=subprocess.PIPE,stderr=subprocess.PIPE)

				result, err = proc.communicate()
				if(not err):
					# print("Result ........")
					print(result.decode('utf-8'))
				else:
					raise Exception("  ***Error***  \n{0}".format(err.decode('utf-8')) )


			except subprocess.CalledProcessError as e:
				print("Process Error running mmx: ")
				print(' '.join(proc.args))
				print(e.output.decode())
				# continue
			except Exception as e:
				print("Error running mmx: ")
				print(' '.join(proc.args))
				print(e)
				# continue
			
			if c >= count:
				break
			

		loop_count += 1


	return 0




def main():
	doc = textwrap.dedent("""\


		Example with address file and mmx location:
		python3 mmx-send-test.py \\\r
			--mmx-dir /home/greg/src/mmx-node/build \\\r
			--address-file /home/greg/Documents/mmx-addresses.json \\\r
			--amount 0.0123 --count 10 --delay 250 --iterations 2

		Example with defaults:
		python3 mmx-send-test.py --amount 0.0123 --count 10

		The above defaults to:
		--mmx-dir <homedir>/mmx-node/build
		--address-file <homedir>/harvested-mmx-addresses.json
		--delay 200
		--iterations 1
			

		""")

	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,epilog=doc)

	parser.add_argument('--amount', required=True, dest="amount",
		help='Amount to send in MMX')
	parser.add_argument('--count', required=True, dest="count",
		help='Number of addresses to send')

	parser.add_argument('--delay', required=False, dest="delay",
		help='Delay between sending each transaction in milliseconds (default 200)')

	parser.add_argument('--mmx-dir', required=False, dest="mmx_dir",
		help='Directory containing mmx command: default <homedir>/mmx-node/build')

	parser.add_argument('--address-file', required=False, dest="addr_file",
		help='Full file path to json address file. Default is <homedir>/harvested-mmx-addresses.json')

	parser.add_argument('--iterations', required=False, dest="iterations",
		help='Repeat sending count X times (default: 1)')

	try:
		pargs = parser.parse_args()
		#indexArgs = lambda key: getattr(pargs,key) if hasattr(pargs,key) else None

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
