import argparse
import random
import time
import json
from math import floor
from collections import defaultdict

random.seed(time.time())

SIDES = 6

damage_map = defaultdict(int)

def floored_percentage(val, digits):
	'''
	Turns an ugly percentage float into a pretty percentage string with the specified number of post-decimal digits

	:param val {float}: the value to convert
	:param val {int}: number of decimal places to convert to
	'''

	val *= 10 ** (digits + 2)
	return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)

def roll_dice(rolls, drop_low_num=0, drop_high_num=0):
	'''
	The actual dice rolling engine.  

	Uses random to roll random numbers and append them to a total.
	Handles dropping high and low values by sorting and splicing.
	:param rolls {int}: number of dice to roll
	:param drop_low_num {int}: the number of lowest dice to ignore
	:param drop_high_num {int}: the number of highest dice to ignore
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

def get_total_damage_from_attack(dice, power, drop_low, drop_high):
	'''
	Calculates total damage from an attack given the provided parameters
	'''

	damage_roll = roll_dice(dice, drop_low, drop_high)
	
	return power + damage_roll

def get_quantity(quantity):
	'''
	Gets a quantity from a json field.  If the value is a integer, it is simply returned.
	If it is a string of the form "d6", then it will return a random number between 1
	and the number specified.
	'''
	if type(quantity) in [str, unicode]:
		if quantity.startswith('d'):
			actual_quantity = random.randrange(1, int(quantity[1:]) + 1)
			return actual_quantity
		else:
			params = quantity.split('d')
			if len(params) == 2:
				actual_quantity = 0
				for i in xrange(1, int(params[0]) + 1):
					actual_quantity += random.randrange(1, int(params[1]) + 1)
				return actual_quantity
	return quantity

def run_iteration(sim_data):
	'''
	Runs a full iteration of the combat sequence
	:return {boolean}
	'''

	attackers = sim_data['attackers']
	targets = sim_data['targets']

	target_count = 0
	target = targets[target_count]
	target['damage_taken']= 0;

	for attacker in attackers:
		for weapon in attacker['attacks']:
			for swing in xrange(1, get_quantity(weapon['quantity']) + 1):
				attack_roll = roll_dice(attacker['hit_dice'], 
										attacker['low_hit_dice_drop'], 
										attacker['high_hit_dice_drop'])

				if weapon['attack'] + attack_roll < target['defense']:
					continue

				damage = get_total_damage_from_attack(weapon['damage_dice'], 
													  weapon['power'], 
													  attacker['low_damage_dice_drop'], 
													  attacker['high_damage_dice_drop'])

				if damage <= target['armor']:
					continue
				target['damage_taken'] += (damage - target['armor'])

				if target['damage_taken'] >= target['wounds']:
					target_count += 1

					if target_count >= len(targets):
						return True
					else:
						target = targets[target_count]
						target['damage_taken']= 0;
	return False

def run_simulation(sim_data):
	success = 0.0
	
	for i in xrange(sim_data['iterations']):
		if run_iteration(sim_data):
			success += 1
		for target in sim_data['targets']:
			damage_map[target['name']] += target['damage_taken']

	print 'You would suceed ' + floored_percentage(success / sim_data['iterations'], 1) +' percent of the time.'
	for target in sim_data['targets']:
		print 'Average damage for ' + target['name'] + ' was: ' + str(damage_map[target['name']]/sim_data['iterations'])

def setup_args():
	'''
	Sets up the argument parser and parses the command line arguments
	'''

	parser = argparse.ArgumentParser(description='Calculate how often you will destroy a model.')

	parser.add_argument('simulation_filename', type=str,
	                   help='filename of the .json file to execute a simulation with')

	arguments = parser.parse_args()
	return arguments

if __name__ == '__main__':
	args = setup_args()
	data = open(args.simulation_filename).read()
	simulaton_data = json.loads(data)
	run_simulation(simulaton_data)