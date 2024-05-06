#!/bin/python3

# import libraries for cmd arguments,
# generating random numbers
# and measuring the time
from sys import argv
from random import randrange
from time import time
# libraries for supports_color function
import sys
import os

# check if terminal supports colors
# taken from django: https://github.com/django/django/blob/main/django/core/management/color.py
# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
try:
    import colorama

    # Avoid initializing colorama in non-Windows platforms.
    colorama.just_fix_windows_console()
except (
    AttributeError,  # colorama <= 0.4.6.
    ImportError,  # colorama is not installed.
    # If just_fix_windows_console() accesses sys.stdout with
    # WSGIRestrictedStdout.
    OSError,
):
    HAS_COLORAMA = False
else:
    HAS_COLORAMA = True

def supports_color():
    """
    Return True if the running system's terminal supports color,
    and False otherwise.
    """

    def vt_codes_enabled_in_windows_registry():
        """
        Check the Windows Registry to see if VT code handling has been enabled
        by default, see https://superuser.com/a/1300251/447564.
        """
        try:
            # winreg is only available on Windows.
            import winreg
        except ImportError:
            return False
        else:
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console")
                reg_key_value, _ = winreg.QueryValueEx(reg_key, "VirtualTerminalLevel")
            except FileNotFoundError:
                return False
            else:
                return reg_key_value == 1

    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    return is_a_tty and (
        sys.platform != "win32"
        or (HAS_COLORAMA and getattr(colorama, "fixed_windows_console", False))
        or "ANSICON" in os.environ
        or
        # Windows Terminal supports VT codes.
        "WT_SESSION" in os.environ
        or
        # Microsoft Visual Studio Code's built-in terminal supports colors.
        os.environ.get("TERM_PROGRAM") == "vscode"
        or vt_codes_enabled_in_windows_registry()
    )

# class for easier color changing
class format:
    # use django function
    if supports_color():
        magenta = "\033[95m"
        blue = "\033[94m"
        cyan = "\033[96m"
        green = "\033[92m"
        yellow = "\033[93m"
        red = "\033[91m"
        normal = "\033[0m"
        bold = "\033[1m"
    else:
        magenta = ""
        blue = ""
        cyan = ""
        green = ""
        yellow = ""
        red = ""
        normal = ""
        bold = ""

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
        sep = "\n" + 66 * "-" + "\n"
        print(
            sep[1:] +
            format.yellow +
            "Python script that sorts an array with multible algorithms\n" +
            "Made and published by " + 
            format.bold +
            "Technicfan " +
            format.normal +
            format.yellow +
            "under " +
            format.bold +
            "MIT Licence " +
            format.normal +
            format.yellow +
            "on GitHub\n" +
            "for learning purposes - (https://github.com/Technicfan/pysort)" +
            format.normal +
            sep +
            format.magenta +
            format.bold +
            "Usage:" +
            format.normal +
            sep +
            format.blue +
            "first argument:"
        )
        # print available algorithms
        for func in algorithms:
            print(f"-> {func} or {algorithms.index(func)}")
        print(
            "   to use this sorting algorithm\n" +
            "-> -h, --h, -help, --help or help for this information" +
            format.normal +
            sep +
            format.cyan +
            "second argument:\n" +
            "-> none to sort default array\n" +
            "-> random to sort random array\n" +
            "-> input + min 2 more args to sort array made from next arguments" +
            format.normal +
            sep +
            format.green +
            "next arguments only matter if second arg is input" +
            format.normal +
            sep[:-1]
        )
        # exit to prevent running the rest of the script
        return
            
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
    if not (args[1] in algorithms or args[1] in (str(i) for i in range(len(algorithms)))):
        # make shure that seperator is longer than text displayed
        msg = "No or invalid sorting algorithm selected!"
        if len(msg) > len(sep):
            sep = "\n" + (len(msg) + 1) * "-" + "\n"
        # show hint for user
        print(
            sep[1:] +
            format.yellow +
            msg +
            format.normal +
            sep +
            format.blue +
            "Available algorithms:"
        )
        # show available algorithms to the user
        for func in algorithms:
            print(f"-> {func} - {algorithms.index(func)}")
        print(format.normal + sep[1:-1])
        # let the user choose one
        chosen = input(f"{format.cyan}Choose algorithm:\n{format.green}>>{format.normal} ")
        # check if it's available and add or replace it in args
        if chosen in algorithms:
            args[1] = chosen
        else:
            # also index is an option
            try:
                args[1] = algorithms[int(chosen)]
            except:
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

    # make sure once again that seperator is longer than text
    headline = name + " Algorithm"
    if len(headline) + 2 > len(sep):
            sep = "\n" + (len(headline) + 1) * "-" + "\n"

    # make shure that time is not 0
    time_ms = (end - begin) * 10**3
    for i in range(2,4):
        time_round = round(time_ms, i)
        if time_round > 0:
            break

    # print everything
    print(
        sep[1:] +
        format.magenta +
        format.bold +
        headline +
        format.normal +
        sep +
        format.blue +
        "array:\n" +
        # format array
        ", ".join(str(i) for i in data) +
        format.normal +
        sep +
        format.cyan +
        "sorted array:\n" +
        # format sorted array
        ", ".join(str(i) for i in sorted) +
        format.normal +
        sep +
        format.green +
        "sorting took " +
        # calulate time and round it
        str(time_round) + 
        " ms" +
        format.normal +
        sep[:-1]
    )

try:
    # run main function with cmd arguments
    main(argv)
except:
    # show error in red
    print(format.red + "An error ocurred" + format.normal)
