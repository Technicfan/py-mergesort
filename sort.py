#!/bin/python3

# import libraries for cmd arguments,
# generating random numbers
# and measuring the time
from sys import argv
from random import randrange
from time import time

# function to check if input list is made up of digits
def checkdigit(list):
    for item in list:
        if not item.isdigit():
            return False
    return True
        
    return array

######################################################
# first part of the merge sort algorithm
def mergesort(data):
    match len(data):
        # error if data empty
        case 0:
            return "No input data"
            exit(1)
        # nothing to do if only one element
        case 1:
            return data
        # otherwise mergesort the array recursively
        case _:
            half = len(data) // 2
            left = mergesort(data[:half])
            right = mergesort(data[half:])
            return merge(left,right)

# second (more complex) part of the algorithm
def merge(left,right):
    merged = []
    # repeat this until one array is empty
    while len(left) > 0 and len(right) > 0:
        # add smaller value to result and delete it from input
        if left[0] < right[0]:
            merged.append(left[0])
            del left[0]
        else:
            merged.append(right[0])
            del right[0]
    # add items left in the arrays to result
    merged += left + right

    return merged
######################################################


def output(data,name,sortfunc):
    # dynamicly generate length of the seperator
    sep = "\n"
    for i in range(0,len(str(data)) - 1):
        sep += "-"
    sep += "\n"

    # sort the data and measure time
    begin = time()
    sorted = sortfunc(data)
    end = time()

    print(
    name + " Algorithm" +
    sep +
    "array:\n" +
    # format array
    ", ".join(str(i) for i in data) + 
    sep +
    "sorted array:\n" +
    # format sorted array
    ", ".join(str(i) for i in sorted) +
    sep +
    "sorting took " +
    # calulate time and round it
    str(round((end-begin)*10**3,2)) + 
    " ms"
    )

def main(args):
    # check selected sorting arlgorithm
    if len(args) >= 2 and args[1] == "mergesort":
        algorithm = "Merge Sort"
        func = mergesort
    else:
        print("No sorting algorithm selected")
        exit(0)

    # init the array that is going to be sorted
    array = []
    # if random specified create random array
    if len(args) >= 3 and args[2] == "random":
        for i in range(0,randrange(2,20)):
            array.append(randrange(200))
    # if input specified create array from input
    elif len(args) > 3 and args[2] == "input":
        # create integer array
        if checkdigit(args[3:]) == True:
            for item in args[3:]:
                array.append(int(item))
        # or string array
        else:
            for item in args[3:]:
                array.append(item)
    else:
        # default fallback from task
        array = [2, 20, 100, 1, 50, 5, 200, 10]
    
    output(array,algorithm,func)

# run main function with cmd arguments
main(argv)
    