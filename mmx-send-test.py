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
	
	MMXDIR = indexArgs('mmx_dir') if (indexArgs('mmx_dir') != None) else os.environ['HOME'] + "/mmx-node/build"
	MMXCMD = MMXDIR + "/mmx"

	amount = float(indexArgs('amount')) if (indexArgs('amount') != None) else 0
	count = int(indexArgs('count')) if (indexArgs('count') != None) else 0

	delay = float(indexArgs('delay')) if (indexArgs('delay') != None) else 200
	# print("Selected delay: " + str(delay))
	if delay > 0:
		delay = delay / 1000

	loop = int(indexArgs('iterations')) if (indexArgs('iterations') != None) else 1

	with open(outfile) as f:
		data = json.load(f)

	
	print("Sending transactions: " + str(count) + " Iterations: " + str(loop))
	print("Delaying txs: " + str(delay))
	loop_count = 0
	
	while loop_count < loop:
		print("---- Begin tx loop: " + str(loop_count + 1) + "---")
		random.shuffle(data)
		c = 0
		for address in data:
			if(c >= 1):
				time.sleep(delay)
			
			# print(loop_count)
			try:
				
				cmd = [MMXCMD, 'wallet', 'send', '-a', str(amount), '-t', address]
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
			
			c += 1
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
		indexArgs = lambda key: getattr(pargs,key) if hasattr(pargs,key) else None

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
