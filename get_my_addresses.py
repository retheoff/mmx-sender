#!/usr/bin/env python3
import os
import subprocess
import json

import pprint


def main():
	cmd = ['/home/greg/src/mmx-node/build/mmx', 'wallet', 'show', '50']
	out = subprocess.check_output(cmd).decode("utf-8")
	data = out.split('\n')
	addrs = [s.split(': ')[1] for s in data[2:] if s != '']
	json.dump(addrs, open(f'{os.environ["HOME"]}/my_mmx_addresses.json', 'w'))


if __name__ == "__main__":
	main()

