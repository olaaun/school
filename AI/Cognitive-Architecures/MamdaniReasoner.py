def triangle(position, x0, x2, clip):
	value = 0.0
	x1 = (x0+x2)/2
	if x0 <= position <= x1:
		value = (position - x0) / (x1 - x0)
	elif x1 <= position <= x2:
		value = (x2 - position) / (x1 - x0)
	return min(value, clip)

def grade(position, x0, x1, clip):
	if position>=x1: value = 1.0
	elif position <= x0: value = 0.0
	else: value = (position - x0) / (x1 - x0)
	return min(value, clip)

def reverse_grade(position, x0, x1, clip):
	if position <= x0: value = 1.0
	elif position >= x1: value = 0.0
	else: value = (x1-position) / (x1-x0)
	return min(value,clip)

def fuzzy_and(a, b):
	return min(a,b)

def fuzzy_or(a, b):
	return max(a,b)

def fuzzy_not(a):
	return 1 - a

#Intervals of where the sets are determined for the different linguistic variables
fuzzy_distance = {'VerySmall': (1,2.5), 'Small':(1.5, 4.5), 'Perfect': (3.5, 6.5),
				'Big': (5.5, 8.5), 'VeryBig': (7.5, 9)}
fuzzy_delta = {'ShrinkingFast': (-4,-2.5), 'Shrinking': (-3.5, -0.5), 'Stable': (-1.5, 1.5), 'Growing': (0.5, 3.5), 'GrowingFast': (2.5, 4)}
fuzzy_action = {'BrakeHard': (-8,-5), 'SlowDown': (-7,-1), 'None': (-3,3), 'SpeedUp': (1,7), 'FloorIt': (5,8)}

def mamdani_rasoner(distance, delta):
	#These are the clip values, meaning what values the actions will have. 
	#Like in exercise a, if distance is 0.6 and delta is 0.4, then action none has value 0.4
	#Has to be hardcoded, sadly
	clip_values ={
	'None': fuzzy_and(triangle(distance, fuzzy_distance['Small'][0], fuzzy_distance['Small'][1], 1),
		triangle(delta, fuzzy_delta['Growing'][0], fuzzy_delta['Growing'][1], 1)),
	'SlowDown': fuzzy_and(triangle(distance, fuzzy_distance['Small'][0], fuzzy_distance['Small'][1], 1),
		triangle(delta, fuzzy_delta['Stable'][0], fuzzy_delta['Stable'][1], 1)),
	'SpeedUp': fuzzy_and(triangle(distance, fuzzy_distance['Perfect'][0], fuzzy_distance['Perfect'][1], 1),
		triangle(delta, fuzzy_delta['Growing'][0], fuzzy_delta['Growing'][1], 1)),
	'FloorIt': fuzzy_and(triangle(distance, fuzzy_distance['VeryBig'][0], fuzzy_distance['VeryBig'][1], 1),
		fuzzy_or(fuzzy_not(triangle(delta, fuzzy_delta['Growing'][0], fuzzy_delta['Growing'][1], 1)),
		fuzzy_not(grade(delta, fuzzy_delta['GrowingFast'][0], fuzzy_delta['GrowingFast'][1], 1)))),
	'BrakeHard': reverse_grade(distance, fuzzy_distance['VerySmall'][0], fuzzy_distance['VerySmall'][1], 1)
	}
	numerator = 0
	denominator = 0
	#Dictionary, where key is index 
	#and value is a tuple including action type (i.e. BrakeHard) and value
	index_value_dict = {}
	#This for loop iterates through every x, and finds the correct mu(x) 
	for i in range(-10,11):
		maximum = ('BrakeHard', grade(i,fuzzy_action['BrakeHard'][0], fuzzy_action['BrakeHard'][1], clip_values['BrakeHard']))
		index_value_dict[i] = maximum
		for key in fuzzy_action:
			if key == 'BrakeHard' or key == 'FloorIt':
				continue
			value = triangle(i, fuzzy_action[key][0], fuzzy_action[key][1], clip_values[key])
			if value> maximum[1]:
				maximum = (key, value)
				index_value_dict[i] = maximum
		value = grade(i, fuzzy_action['FloorIt'][0], fuzzy_action['FloorIt'][1], clip_values['FloorIt'])
		if value > maximum[1]:
			maximum = ('FloorIt', value)
			index_value_dict[i] = maximum
		numerator += i*maximum[1]
		denominator += maximum[1]
	if denominator == 0:
		print("Error, all values clipped to zero")
		return
	center_of_gravity = numerator/denominator
	print(center_of_gravity)
	print("Action to be done: " +str(index_value_dict[round(center_of_gravity)][0]))


mamdani_rasoner(7,-2)
