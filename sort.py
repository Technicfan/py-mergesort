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
def mergesort(array):
    # check if array has multible elements
    if len(array) > 1:
        # mergesort the array recursively
        half = len(array) // 2
        left = mergesort(array[:half])
        right = mergesort(array[half:])
        return merge(left,right)
    else:
        # nothing to do if only one element or less
        return array

# second (more complex) part of the algorithm
def merge(left,right):
    sorted = []
    # repeat this until one array is empty
    while len(left) > 0 and len(right) > 0:
        # add smaller value to result and delete it from input
        if left[0] < right[0]:
            sorted.append(left[0])
            del left[0]
        else:
            sorted.append(right[0])
            del right[0]        
    # return all arrays together
    return sorted + left + right
######################################################
# quick sort algorithm
# taken from "https://stackoverflow.com/questions/18262306/quicksort-with-python"
# and modified for consistency
def quicksort(array):
    less = []
    equal = []
    greater = []
    if len(array) > 1:
        pivot = array[0]
        for item in array:
            if item < pivot:
                less.append(item)
            elif item == pivot:
                equal.append(item)
            else:
                greater.append(item)
        return quicksort(less) + equal + quicksort(greater)
    else:
        return array
######################################################
# bubble sort algorithm
def bubblesort(array):
    # save array to local var to prevent changing input outside of function
    array = array[:]
    for item in array:
        for i in range(len(array)-1):
            # check if next item is smaller
            if array[i] > array[i+1]:
                # swap items
                array[i], array[i+1] = array[i+1], array[i]
    return array
######################################################
# selection sort algorithm
def selectionsort(array):
    # same as above
    array = array[:]
    for index in range(len(array)):
        # set start index to loop var
        min = index
        for i in range(index+1,len(array)):
            # check if the current item is smaller
            if array[i] < array[min]:
                # set min to this
                min = i
        # check if min changed
        if min != index:
            # swap items
            array[min], array[index] = array[index], array[min]
    return array
######################################################
# gnome sort algorithm
def gnomesort(array):
    # same as above
    array = array[:]
    # start at the beginning
    index = 0
    while index < len(array):
        # check if index is 0 or previous item is smaller
        if index == 0 or array[index] >= array[index-1]:
            # move on
            index += 1
        else:
            # swap current and previous item
            array[index], array[index-1] = array[index-1], array[index]
            # go back
            index -= 1
    return array
######################################################


def main(args):
    # init available algorithms
    algorithms = (
        "mergesort",
        "quicksort",
        "bubblesort",
        "selectionsort",
        "gnomesort"
    )
    # check if there are no arguments or the first one is a form of help
    if len(args) == 1 or (len(args) == 2 and args[1] in ("help", "--help", "-h", "-help", "--h")):
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
        for i in range(randrange(2,22)):
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
    sep = "\n" + (len(str(data)) - 1) * "-" + "\n"

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
        case "bubblesort" | "2":
            name = "Bubble Sort"
            sortfunc = bubblesort
        case "selectionsort" | "3":
            name = "Selection Sort"
            sortfunc = selectionsort
        case "gnomesort" | "4":
            name = "Gnome Sort"
            sortfunc = gnomesort

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
