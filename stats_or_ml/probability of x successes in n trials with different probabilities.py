#https://stats.stackexchange.com/questions/9510/probability-distribution-for-different-probabilities

import numpy as np 
number_successes = 9
number_trials = 16

def calc_n_combinations(n_trials, n_successes):
    import math 
    return math.factorial(n_trials) / (math.factorial(n_successes) * math.factorial(n_trials - n_successes))

calc_n_combinations(number_trials, number_successes)

from itertools import combinations
print(list(combinations([1,2,3,], 2)))

number_successes = 9
persons = [0.9, 0.8, 0.7, 0.8, 0.4, 0.5, 0.75, 0.84, 0.43, 0.52, 0.59, 0.28, 0.37, 0.68, 0.24, 0.55]

def my_prob(number_successes, probs):
    answer = 0.0
    combination_list = list(combinations(range(0,len(probs)), number_successes))
    chance_of_sequence = 1
    for com in combination_list:
        for p_i in range(0,len(probs)):
            if p_i in com:
                chance_of_sequence = chance_of_sequence * probs[p_i]
            else:
                chance_of_sequence = chance_of_sequence * (1 - probs[p_i])
        answer += chance_of_sequence
        chance_of_sequence = 1
    # print(answer)
    return answer

from matplotlib import pyplot as plt

def run_my_prob(persons):
    all_ans = []
    for n in range(0, len(persons)):
        all_ans.append(my_prob(n, persons))
    plt.bar(range(0,len(all_ans)),all_ans)
    plt.show()
    # print(f'Sum of all answers: {np.array(all_ans).sum()}')

## Test one 
# How many people are going to survive if they have the following survival probs
persons_low = [0.1, 0.2, 0.13, 0.15, 0.3, 0.2, 0.167, 0.23, 0.05, 0.25, 0.12, 0.05, 0.03, 0.2, 0.2, 0.11]
run_my_prob(persons_low)

# Same question with High Levels
persons_high = [0.901, 0.85, 0.78, 0.8, 0.9, 0.97, 0.89, 0.97, 0.975, 0.92, 0.8, 0.88, 0.86, 0.944, 0.998, 0.83]
run_my_prob(persons_high)


