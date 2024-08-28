import random

from collections import namedtuple
from itertools import permutations
from typing import Set , Tuple
from fractions import Fraction

PRIZE = 0
PLAYER_CHOICE = 1
FINAL_CHOICE = 2
Prob_Event = namedtuple("Prov_Event" ,
                        ["prob" , "prize_door" , "player_choice" , "final_choice" , "result"])

# Fun program to show Monte Hall problem
# Author: Douglas Rosenberg
# This progrm is to help people understand the Monte Hall problem
# I did not see any explainations where the entire probablity space is presented as tuples
# Assigns a winning leaf as 1/9
# Assigns a non-winning leaf as 1/18
# This allows that Monte will reveal each of the non-winning doors 1/2 of the time
# This program models this as a non-equal Probitlity Space where Monte will reveal each Losing door
# an equal number of times on the 3rd stap.
# This make each losing choice as 1/18.
# I did this to make it easier for people to grasp why switching makes sense


def assignProbSwitch (event: list[tuple]) -> Set[Prob_Event] :
    prob_events: Set[Prob_Event] = set()
    for outcome in event :

        if outcome[PRIZE] == outcome[PLAYER_CHOICE] :
            prob_event = Prob_Event("1/9" , outcome[PRIZE] , outcome[PLAYER_CHOICE] , outcome[FINAL_CHOICE] , 'W')

        else :
            prob_event = Prob_Event("1/18" , outcome[PRIZE] , outcome[PLAYER_CHOICE] , outcome[FINAL_CHOICE] , 'L')
        prob_events.add(prob_event)
    return prob_events


def stay_monty_hall_choose () :
    win_pick = random.randint(1 , 3)
    # you pick car
    your_pick = random.randint(1 , 3)
    return win_pick == your_pick


def switch_monty_hall_choose () :
    win_pick = random.randint(1 , 3)
    # you pick car
    your_pick = random.randint(1 , 3)
    # host reveals where i is not
    for i in [1 , 2 , 3] :
        if win_pick == i and your_pick != i :
            # host you switch to winning door
            your_pick = win_pick
        elif win_pick == i and your_pick == i :
            # host reveals another door other than i
            # you pick away from winning door an lose
            your_pick = -1
    return win_pick == your_pick


def sum_prob (prob_events: set[Prob_Event]) :
    sum_win = 0
    for event in prob_events :
        if event.result == 'W' :
            sum_win += eval(event.prob)
    return sum_win


def ask_number_times () :
    while True :
        number_times = input("How many times do you want to run simulation?  (default is 100,000)")
        try :
            if not number_times :
                number_times = 100_000
            else :
                number_times = int(number_times)
            return number_times
        except :
            print("Invalid selection try again")


def simulate_monte_carlo () :
    run_number = ask_number_times()
    stay_won = 0
    switch_won = 0
    print(f'Running simulation {run_number:,}')
    for i in range(run_number) :
        stay_won += stay_monty_hall_choose()
        switch_won += switch_monty_hall_choose()
    prob_switched = switch_won / run_number
    print(f'Strategy where you stay with Original Door: You won {stay_won / run_number:.3%}')
    print(f'Strategy where you Switch doors: You won {switch_won / run_number:.3%}')
    print(f'Switch differs from theoretical 2/3 (5 decimals) {prob_switched - 2 / 3:.5f}')


def print_sample_space_tuples (sample_space: Set[Prob_Event]) -> None :
    for outcome in sample_space :
        t = tuple(outcome)
        print(t)


def print_sample_Space (sample_space: Set[Prob_Event]) -> None :
    print_sample_space_tuples(sample_space)
    for outcome in sample_space :
        print(outcome)


def compute_sample_space (display=False) :
    import itertools
    x = [1 , 2 , 3]
    # 1. Winning car door
    # 2. Choice by player
    # 3. Choice by Monte to show door ( we will assume it is always lowest door, not the player and not winner
    # 4. Final choice by player

    sample_space = [p for p in itertools.product(x , repeat=3)]

    new_sample_space = set()
    for point in sample_space :
        if point[PLAYER_CHOICE] == point[FINAL_CHOICE] :
            continue

        new_sample_space.add(point)
    win_event = set()
    new_sample_space = sorted(new_sample_space)
    print('new sample space len =' , len(sample_space))
    for point in new_sample_space :
        if point[FINAL_CHOICE] != point[PRIZE] :
            continue

        if point[PRIZE] == point[PLAYER_CHOICE] :
            continue

        win_event.add(point)
    win_event = sorted(win_event)
    if display :
        print(f'win event = ' , set(win_event))
        print('size win event =' , len(win_event))
    prob_events = assignProbSwitch(new_sample_space)
    if display :
        print_sample_Space(prob_events)
    frac_win = Fraction(sum_prob(prob_events))
    frac_win = frac_win.limit_denominator(9)
    print('Probability of winning = ' , frac_win)


def main () :
    print("Welcome to Monte Hall Game Fun")
    menu_str = """
     1 For theoretical Result
     2 For Monte Carlo simulation
     3 Display Event Space Tuples with Probabilities
     """
    print(menu_str)
    request = input('Enter selection: ')
    match request :
        case "1" :
            compute_sample_space()
        case "2" :
            simulate_monte_carlo()
        case "3" :
            compute_sample_space(display=True)
        case _ :
            print("Invalid request")


if __name__ == "__main__" :
    main()
