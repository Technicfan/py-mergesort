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
    else:  # You need to handle the part at the end of the recursion - 
           # when you only have one element in your array, just return the array.
        return array
######################################################


def main(args):
    # init available algorithms
    algorithms = (
        "mergesort",
        "quicksort"
    )
    # check if there are no arguments or the first one is a form of help
    if len(args) == 1 or (len(args) >= 2 and args[1] in ("help", "--help", "-h", "-help", "--h")):
        # sperator because it's often used
        sep = "\n" + 65 * "-" + "\n"
        print(
            sep[1:] +
            "Python script that sorts an array with multible algorithms\n" +
            "Made and published by Technicfan under MIT Licence on GitHub\n" +
            "for learning purposes - (https://github.com/Technicfan/pysort)" +
            sep +
            "Usage:" +
            sep +
            "first argument:"
        )
        # print available algorithms
        for func in algorithms:
            print(f"-> {func} or {algorithms.index(func)}")
        print(
            "   to use this sorting algorithm\n" +
            "-> -h, --h, -help, --help or help for this information" +
            sep +
            "second argument:\n" +
            "-> none to sort default array\n" +
            "-> random to sort random array\n" +
            "-> input + min 2 more args to sort array made from next arguments" +
            sep +
            "next arguments only matter if second arg is input" +
            sep[:-1]
        )
        # exit to prevent running the rest of the script
        exit(0)
            
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
    sep = "\n" + len(str(data)) * "-" + "\n"

    # check if invalid algorithm specified
    if not (args[1] in algorithms or args[1] in (str(i) for i in range(0,len(algorithms)))):
        # show hint for user
        print(
            sep[1:] +
            "No, or invalid sorting algorithm selected!" +
            sep +
            "Available algorithms:"
        )
        # show available algorithms to the user
        for func in algorithms:
            print(f"-> {func} - {algorithms.index(func)}")
        print(sep[1:-1])
        # let the user choose one
        chosen = input("Choose algorithm:\n>> ")
        # check if it's available and add or replace it in args
        if chosen in algorithms:
            args[1] = chosen
        # also index is an option
        elif chosen in (str(i) for i in range(0,len(algorithms))):
            args[1] = algorithms[int(chosen)]
        else:
            print("invalid option!")
            exit(1)
    # now set selected algorithm
    match args[1]:
        case "mergesort" | "0":
            name = "Merge Sort"
            sortfunc = mergesort
        case "quicksort" | "1":
            name = "Quick Sort"
            sortfunc = quicksort

    # sort the data and measure time
    begin = time()
    sorted = sortfunc(data)
    end = time()

    # print everything
    print(
        sep[1:] +
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
        " ms" +
        sep[:-1]
    )

# run main function with cmd arguments
main(argv)
