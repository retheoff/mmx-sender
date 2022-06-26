#!/usr/bin/env python3

'''
calc_job.py MMX DURATION NBR_ADDR AVG_DELAY_PER_TX
Calculate the amount (MMX) sent per transaction and number of iterations to simulate.

Example:
I have 500 MMX.
I want it to run for 4 hours.
I have 50 addresses.
I want to set each transaction to have a 525 ms average delay.

calc_job.py 500 4 50 525
'''

import sys



def calculate(budget, duration, nbr_addresses, avg_delay, fee=0.004):
	'''
	Return (amount, iterations).
	'''
	N = duration * 3.6e6 / avg_delay
	return budget / N - fee, int(duration * 3.6e6 / (nbr_addresses * avg_delay) + .5)

def main():
	amount, iterations = calculate(*map(float,sys.argv[1:]))
	nbr_addresses = int(sys.argv[3])
	avg_delay = float(sys.argv[4])
	difference = 0.3 # Range difference on ammount and delay
	amin = amount*(1-difference)
	amax = amount*(1+difference)
	dmin = avg_delay*(1-difference)
	dmax = avg_delay*(1+difference)
	print(f'mmx-send-test.py --amount {amin:.6f},{amax:.6f} --count {nbr_addresses} --delay {dmin:.0f},{dmax:.0f} --iterations {iterations}')
	

if __name__ == "__main__":
	main()

