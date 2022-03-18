#!/usr/bin/env python
import random

def roll(num_dice, num_sides):
    roll = 0
    for dice in range(0, num_dice):
        roll += random.randint(1, num_sides)
    return roll

def four_six_drop():
    list = []
    for i in range(0,4):
        list.append(roll(1,6))

    list.sort()
    dropped = list.pop(0)
    return (dropped, list)


def rollstats():
    random.seed()
    string = "Stats are\n-----------\n"
    for loop in range(0,6):
        dropped, three_six = four_six_drop()
        stat = sum(three_six)
        string += ("**" + str(stat) + "** ")
        string += (str(three_six) + " {" + str(dropped) + "}\n")
    return string
