import argparse
import random
import time

from math import floor

random.seed(time.time())

SIDES = 6

def floored_percentage(val, digits):
	'''
	Turns an ugly percentage float into a pretty percentage string with the specified number of post-decimal digits
	'''

	val *= 10 ** (digits + 2)
	return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)

def roll_dice(rolls, drop_low_num=0, drop_high_num=0):
	'''
	The actual dice rolling engine.  
	Uses random to roll random numbers and append them to a total.
	Handles dropping high and low values by sorting and splicing.
	'''

	results = []
	for roll in xrange(rolls):
		results.append(random.randrange(1, SIDES + 1))
	results.sort()

	if drop_low_num:
		for drop in xrange(drop_low_num):
			results = results[1:]

	if drop_high_num:
		for drop in xrange(drop_high_num):
			results = results[:-1]

	return sum(results)

def run_simulation(args):
	'''
	Manages the simulation by tracking number of successes versus number of simulations
	'''

	success = 0.0
	for i in xrange(args.iterations):
		result = roll_dice(args.dice, args.low, args.high)
		if args.attack + result >= args.defense:
			success = success + 1
	print 'You would suceed ' + floored_percentage(success / args.iterations, 1) +' percent of the time.'

def setup_args():
	'''
	Sets up the argument parser and parses the command line arguments
	'''

	parser = argparse.ArgumentParser(description='Calculate some dice rolls.')

	parser.add_argument('iterations', type=int,
	                   help='an integer to specify how many simulations to run')

	parser.add_argument('attack', type=int,
	                   help='an integer to specify what the simulation attack value is')

	parser.add_argument('defense', type=int,
	                   help='an integer to specify what the simulation defense is')

	parser.add_argument('dice', type=int,
	                   help='an integer to specify how many total dice to roll')

	parser.add_argument('--low', dest='low', action='store',
		default=0, type=int,
		help='an integer to specify how many of the lowest dice to drop')

	parser.add_argument('--high', dest='high', action='store',
		default=0, type=int,
		help='an integer to specify how many of the highest dice to drop')

	return parser.parse_args()

if __name__ == '__main__':
	args = setup_args()
	run_simulation(args)
