#!/usr/bin/env python
"""A script to convert calculate points from WC 2014 prediction.
"""

__author__ = 'Ismail Sunni'
__copyright__ = 'Ismail Sunni'
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = 'Ismail Sunni'
__email__ = 'imajimatika@gmail.com'
__status__ = 'Prototype'
__date__ = '12 July 2014'

import csv

real_result = ['Brazil', 'Mexico']
real_result += ['Netherlands', 'Chile']
real_result += ['Colombia', 'Greece']
real_result += ['Costa Rica', 'Uruguay']
real_result += ['France', 'Switzerland']
real_result += ['Argentina', 'Nigeria']
real_result += ['Germany', 'USA']
real_result += ['Belgium', 'Algeria']

real_winner = ''  # will be updated after the final match

def read_csv(path):
	predictions = []
	with open(path, 'rb') as csvfile:
		rows = csv.reader(csvfile, delimiter=',')
		for row in rows:
			predictions.append(row)
	return predictions

def get_group_point(prediction, real):
	point = 0
	if prediction[0] == real[0]:
		point += 1
	if prediction[1] == real[1]:
		point += 1
	if prediction[0] in real:
		point += 1
	if prediction[1] in real:
		point += 1
	if prediction[0] == prediction[1]:
		point -= 1
	return point

def get_total_group_point(predictions, reals):
	points = []
	for i in range(8):
		index = 2 * i
		point = get_group_point(predictions[index:index + 2], reals[index:index + 2])
		points.append(point)
	return points, sum(points)

def main():
	points = []
	csv_path = 'predictions.csv'
	predictions = read_csv(csv_path)
	for prediction in predictions[1:-2]:
		point = []
		point.append(prediction[1])
		
		# groups
		group_points, group_point = get_total_group_point(prediction[4:], real_result)
		# winner
		if prediction[3] == real_winner:
			winner_point = 10
		else:
			winner_point = 0

		point.append(group_points)
		point.append(winner_point)
		point.append(group_point + winner_point)
		points.append(point)

	for point in points:
		print point

	winner_point = points[0]
	for point in points:
		if point[-1] > winner_point[-1]:
			winner_point = point
	print 'Winner is ', winner_point


if __name__ == '__main__':
	main()