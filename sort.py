#!/bin/python3

# import libraries for cmd arguments,
# generating random numbers,
# measuring the time
# and running in parallel
from sys import argv
from random import randrange
from time import time
import multiprocessing as mp
from math import log
import algorithms as functions

#-----------------------------------------------------------------------------------------------
# libraries for supports_color function
import sys
import os

# check if terminal supports colors
# taken from django: https://github.com/django/django/blob/main/django/core/management/color.py
# modified to run in parallel and added colorama init from before
# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
def supports_color(q):

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

    q.put(  
        is_a_tty and (
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
    )
#-----------------------------------------------------------------------------------------------


# class for easier color changing
class format:
    q = mp.Queue()
    if __name__ == "__main__":
        # run django function in parallel
        t = mp.Process(target=supports_color, args=(q,))
        t.start()
        t.join()
    # check output
    if not q.empty() and q.get():
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

def benchmark(algorithms,arg):
    funcs = {
        "mergesort": functions.mergesort_b,
        "quicksort": functions.quicksort_b,
        "bubblesort": functions.quicksort_b,
        "selectionsort": functions.selectionsort_b,
        "gnomesort": functions.gnomesort_b
    }
    for algorithm in algorithms:
        globals()["steps_" + algorithm] = ()
    if arg.isdigit():
        size = int(arg)
    else:
        size = 128
    for i in range(3):
        for algorithm in algorithms:
            array = []
            for j in range(size):
                array.append(randrange(5*10**3))
            funcs.get(algorithm)(array)
            globals()["steps_" + algorithm] += round(functions.steps / len(array)),
            functions.steps = 0
    for algorithm in algorithms:
        print(algorithm.split("sort")[0].capitalize() + " Sort:")
        mw = 0
        for steps in globals()["steps_" + algorithm]:
            mw += steps
        print(str(round(mw/10)) + " steps per item")

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
        # print information
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
        # print rest of help
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
    elif len(args) >= 2 and args[1] == "benchmark":
        if len(args) > 2:
            benchmark(algorithms,args[2])
        else:
            benchmark(algorithms,"")
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
            sortfunc = functions.mergesort
        case "quicksort" | "1":
            name = "Quick Sort"
            sortfunc = functions.quicksort
        case "bubblesort" | "2":
            name = "Bubble Sort"
            sortfunc = functions.bubblesort
        case "selectionsort" | "3":
            name = "Selection Sort"
            sortfunc = functions.selectionsort
        case "gnomesort" | "4":
            name = "Gnome Sort"
            sortfunc = functions.gnomesort

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
        str(time_round) + 
        " ms" +
        format.normal +
        sep[:-1]
    )

#try:
    # run main function with cmd arguments
main(argv)
#except:
    # show error in red
#    print(format.red + "An error ocurred" + format.normal)
