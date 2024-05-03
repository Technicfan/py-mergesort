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


######################################################
# first part of the merge sort algorithm
def mergesort(data):
    match len(data):
        # error if data empty
        case 0:
            print("No input data")
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
    # return all arrays together
    return merged + left + right
######################################################
# quick sort algorithm
# copied from "https://stackoverflow.com/questions/18262306/quicksort-with-python"
# and renamed function from sort to quicksort
def quicksort(array):
    """Sort the array by using quicksort."""

    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return quicksort(less)+equal+quicksort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to handle the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array
######################################################


def main(args):
    # init available algorithms
    algorithms = [
        "mergesort",
        "quicksort"
    ]
    # check if no or not available algorithm specified
    if len(args) < 2 or ( len(args) >= 2 and not args[1] in algorithms ):
        print("No or not available sorting algorithm selected!\nAvailable algorithms:")
        # show available algorithms to the user
        for func in algorithms:
            print(f"  {func}")
        # let the user choose one
        chosen = input("Choose algorithm:")
        # check if it's available and add or replace it in args
        if chosen in algorithms:
            if len(args) == 1:
                args.append(chosen)
            else:
                args[1] = chosen
        else:
            exit(1)
    # now set selected algorithm
    match args[1]:
        case "mergesort":
            name = "Merge Sort"
            sortfunc = mergesort
        case "quicksort":
            name = "Quick Sort"
            sortfunc = quicksort
            
    # create array to sort
    data = []
    # if random specified create random array
    if len(args) >= 3 and args[2] == "random":
        for i in range(0,randrange(2,22)):
            data.append(randrange(222))
    # if input specified create array from input
    elif len(args) > 3 and args[2] == "input":
        # create integer array
        if checkdigit(args[3:]) == True:
            for item in args[3:]:
                data.append(int(item))
        # or string array
        else:
            for item in args[3:]:
                data.append(item)
    else:
        # default fallback from task
        data = [2, 20, 100, 1, 50, 5, 200, 10]
    
    # dynamicly generate length of the seperator
    sep = "\n"
    for i in range(0,len(str(data))-1):
        sep += "-"
    sep += "\n"

    # sort the data and measure time
    begin = time()
    sorted = sortfunc(data)
    end = time()

    # print everything
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

# run main function with cmd arguments
main(argv)
