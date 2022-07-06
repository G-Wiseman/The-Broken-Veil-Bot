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
        list.append(random.randint(1,6))


    dropped = min(list)
    list.remove(dropped)
    return (dropped, list)

def roll_print_single(num_dice, num_sides):
    message = ""
    sum = 0
    line_count = 0
    for i in range(0, num_dice):
        roll_num = roll(1, num_sides)
        sum += roll_num
        message += f"({roll_num})"
        if line_count == 10:
            message += "\n"
        else:
            line_count += 1
    message += f"\n-----\n {sum}"
    return message
