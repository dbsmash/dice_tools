import destruction_simulator as ds

def test_get_quantity():
	print 'testing get_quantity'
	q = ds.get_quantity(4)
	assert(q == 4)

	for i in xrange(1, 100):
		q = ds.get_quantity('d3')
		assert(q >= 1 and q <= 3)

	for i in xrange(1, 100):
		q = ds.get_quantity('2d3')
		assert(q >= 2 and q <= 6)

	for i in xrange(1, 100):
		q = ds.get_quantity('5d6')
		assert(q >= 5 and q <= 30)

def test_roll_dice():
	print 'testing roll_dice'
	for i in xrange(1, 100):
		total = ds.roll_dice(2)
		assert(total >= 2 and total <= 12)

	total = ds.roll_dice(2, 1, 1)
	assert(total == 0)

	total = ds.roll_dice(15, 14, 0)
	assert(total > 0 and total <= 6)

def test_floored_percentage():
	print 'testing floored_percentage'
	fp = ds.floored_percentage(.6578787878, 1)
	assert(fp == '65.7%')

	fp = ds.floored_percentage(.6578787878, 4)
	assert(fp == '65.7878%')

def test_get_total_damage_from_attack():
	print 'testing get_total_damage_from_attack'
	for i in xrange(1,100):
		total = ds.get_total_damage_from_attack(2, 10, False, 0, 0)
		assert(total >= 12 and total <= 22)

	for i in xrange(1,100):
		total = ds.get_total_damage_from_attack(2, 10, True, 0, 0)
		assert(total >= 13 and total <= 28)

test_get_quantity()
test_roll_dice()
test_floored_percentage()
test_get_total_damage_from_attack()