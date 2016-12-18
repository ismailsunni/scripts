# coding=utf-8
"""Script to draw AFF Cup 2016 Final Match Score Guess winner
"""

import random
with open("final_aff_2016.txt") as f:
    answers = f.read()
answers = answers.split('\n')
wrong_answers = []
winner = None
correct_score = '2-0'
for answer in answers:
    name = ''
    score = answer.split(' ')[-1]
    name = answer[:len(answer) - len(score) - 1]
    score_thai = int(score.split('-')[0])
    score_ina = int(score.split('-')[1])

    if not winner:
        if score == correct_score:
            winner = name, score_thai, score_ina
    else:
        wrong_answers.append([name, score_thai, score_ina])

if winner:
    print 'The Winner is %s who is the fastest guesser for %s score' % (winner[0], correct_score)

# Use all participant's name and their answer for the seed for the sake of fairness
seed = 0
for wrong_answer in wrong_answers:
    seed += len(wrong_answer[0]) + score_thai + score_ina

lucky_winner = random.Random(seed).choice(wrong_answers)
print 'The lucky winner is %s' % lucky_winner[0]

# If you found a bug, just assume it's winner's luck. 
# I have done my best, at 6 am in the morning :D

