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

real_winner = 'Germany'

def read_csv(path):
    predictions = []
    with open(path, 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            predictions.append(row)
    return predictions

def write_csv(path, data):
    with open(path, 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(data)

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
    csv_path = 'World Cup 2014 Poling Result - Sheet1.csv'
    predictions = read_csv(csv_path)
    # print predictions[1]
    # return
    for prediction in predictions[1:]:
        point = []
        point.append(prediction[1])
        
        # groups
        group_points, group_point = get_total_group_point(prediction[3:], real_result)
        # winner
        if prediction[2] == real_winner:
            winner_point = 10
        else:
            winner_point = 0

        point.append(group_points)
        point.append(winner_point)
        point.append(group_point + winner_point)
        points.append(point)

    data = []
    header = [
        'Nama',
        'Grup A',
        'Grup B',
        'Grup C',
        'Grup D',
        'Grup E',
        'Grup F',
        'Grup G',
        'Grup H',
        'Juara',
        'Total']

    data.append(header)

    for point in points:
        datum = []
        datum.append(point[0])
        datum.extend(point[1])
        datum.extend(point[2:])
        data.append(datum)
        print point
    result_path = 'result.csv'
    write_csv(result_path, data)

    winner_point = points[0]
    for point in points:
        if point[-1] > winner_point[-1]:
            winner_point = point
    print 'Winner is ', winner_point
    print 'See your result %s' % result_path


if __name__ == '__main__':
    main()