#!/bin/python3

# import needed libraries
import os
import sys
from random import randrange
from time import perf_counter as time
import algorithms as functions

#-----------------------------------------------------------------------------------------------
# check if terminal supports colors
# taken from django: https://github.com/django/django/blob/main/django/core/management/color.py
# moved colorama init from before into the function
# Copyright (c) Django Software Foundation and individual contributors.
# All rights reserved.
def supports_color():

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
#-----------------------------------------------------------------------------------------------


# class for easier color changing
class format:
    # check if terminal supports colors
    if supports_color():
        magenta = "\033[95m"
        blue = "\033[94m"
        cyan = "\033[96m"
        green = "\033[92m"
        yellow = "\033[93m"
        red = "\033[91m"
        normal = "\033[0m"
        bold = "\033[1m"
    # else set colors to empty strings
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

# function to dispay measured time in correct unit
def format_time(t):
    if t >= 1:
        return str(round(t,2)) + " s"
    t *= 10**3
    iterations = 0
    while round(t,2) == 0:
        t *= 10**3
        iterations += 1
    match iterations:
        case 0:
            unit = " ms"
        case 1:
            unit = " µs"
        case 2:
            unit = " ns"
        case _:
            return "None"
    return str(round(t,2)) + unit

# function to display help information
def help(algorithms):
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
        "-> -h, --h, -help, --help or help for this information\n" +
        "-> benchmark for testing efficiency" +
        format.normal +
        sep +
        format.cyan +
        "second argument:\n" +
        "-> none to sort/benchmark default array\n" +
        "-> random to sort/benchmark random array\n" +
        "-> input + min 2 more args to sort/benchmark\n" +
        "   array made from next arguments\n" +
        "-> benchmark as first arg + size" +
        format.normal +
        sep +
        format.green +
        "third argument:\n" +
        "-> number for size of random benchmark array after\n" +
        "   benchmark + size as previous args" +
        format.normal +
        sep +
        format.yellow +
        "-> anything if input as second arg\n" +
        "-> debug to show errors" +
        format.normal +
        sep[:-1]
    )

# function for benchmark option
def benchmark(algorithms,arg,data):
    # init iteration arrays
    for algorithm in algorithms:
        globals()["steps_" + algorithm] = []
        globals()["time_" + algorithm] = []
    # init seperator
    if os.get_terminal_size()[0] < 35:
        sep = "\n" + os.get_terminal_size()[0] * "-" + "\n"
    else:
        sep = "\n" + 35 * "-" + "\n"
    # init array from input
    if len(data) != 0:
        array = data
        iterations = 1
    elif arg.isdigit():
        size = int(arg)
    else:
        size = 128
    if "iterations" not in locals():
        iterations = 3
    # init total time and mw arrays
    time_s = 0
    times_mw = []
    steps_mw = []
    # benchmark 3 arrays for accuracy
    for i in range(iterations):
        # do this for every algorithm
        for algorithm in algorithms:
            # check if array var already set
            # otherwise generate random array
            if "size" in locals():
                array = []
                for j in range(size):
                    array.append(randrange(size))
            # measure time
            start = time()
            # call function for algorithm
            exec(f"functions.bench().{algorithm}(array)")
            end = time()
            # add measured values to array of algorithm
            globals()["steps_" + algorithm].append(functions.steps)
            globals()["time_" + algorithm].append(end - start)
            # reset stepss
            functions.steps = 0
    # check if multible or only one item in array
    if len(array) == 1:
        num = " item"
    else:
        num = " items"
    # print heading
    print(
        sep[1:] +
        format.magenta +
        format.bold +
        "Benchmark" +
        " with " +
        str(len(array)) +
        num +
        format.normal +
        sep[:-1]
    )
    # do this for every algorithm
    for algorithm in algorithms:
        # print name
        print(format.blue + algorithm.split("sort")[0].capitalize() + " Sort:")
        # calcultae mws for time and steps
        mw_s = 0
        mw_t = 0
        for steps in globals()["steps_" + algorithm]:
            mw_s += steps
        for t in globals()["time_" + algorithm]:
            mw_t += t
        mw_s = round(mw_s / iterations)
        mw_t = mw_t / iterations
        times_mw.append(mw_t)
        steps_mw.append(mw_s)
        # format time
        mw_t_display = format_time(mw_t)
        mw_t_per_n = format_time(mw_t / len(array))
        # print information
        print(
            "-> " +
            format.cyan +
            str(round(mw_s / len(array))) +
            format.blue +
            " steps per item" +
            "\n-> " +
            format.green +
            str(mw_s) +
            format.blue +
            " total steps" +
            "\n-> " +
            format.cyan +
            mw_t_per_n +
            format.blue +
            " per item" +
            "\n-> " +
            format.green +
            mw_t_display +
            " total time" +
            format.normal +
            sep[:-1]
        )
        # add time of algorithm to total time
        time_s += mw_t
    # format time
    time_string = format_time(time_s)
    # get smallest and biggest values from array and the corresponding name
    sorted_times = functions.default().bubblesort(times_mw)
    sorted_steps = functions.default().bubblesort(steps_mw)
    fastest = algorithms[times_mw.index(sorted_times[0])]
    smallest = algorithms[steps_mw.index(sorted_steps[0])]
    slowest = algorithms[times_mw.index(sorted_times[-1])]
    biggest = algorithms[steps_mw.index(sorted_steps[-1])]
    # print summary
    print(
        format.yellow +
        "total time: " +
        time_string +
        format.normal +
        sep +
        format.green +
        "Fastest: " +
        fastest.split("sort")[0].capitalize() +
        " Sort\n" +
        "Smallest footprint: " +
        smallest.split("sort")[0].capitalize() +
        " Sort" +
        format.normal +
        sep +
        format.red +
        "Slowest: " +
        slowest.split("sort")[0].capitalize() +
        " Sort\n" +
        "Biggest footprint: " +
        biggest.split("sort")[0].capitalize() +
        " Sort" +
        format.normal +
        sep[:-1]
    )

def main(args):
    # init available algorithms
    algorithms = (
        "mergesort",
        "quicksort",
        "bubblesort",
        "selectionsort",
        "gnomesort",
        "insertionsort"
    )
    # check if there are no arguments or the first one is a form of help
    if len(args) == 1 or (len(args) == 2 and \
       args[1] in ("help", "--help", "-h", "-help", "--h")):
        help(algorithms)
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
    # and check if it fits in current terminal
    if os.get_terminal_size()[0] < len(str(data)) - 1:
        sep = "\n" + os.get_terminal_size()[0] * "-" + "\n"
        smallterm = True
    else:
        sep = "\n" + (len(str(data)) - 1) * "-" + "\n"
        smallterm = False

    # check if invalid option specified
    if not (args[1] in algorithms + ("benchmark",) or \
       args[1] in (str(i) for i in range(len(algorithms)))):
        # make shure that seperator is longer than text displayed
        msg = "No or invalid option specified!"
        if len(msg) > len(sep) and not smallterm:
            sep = "\n" + (len(msg) + 1) * "-" + "\n"
        # show hint for user
        print(
            sep[1:] +
            format.yellow +
            msg +
            format.normal +
            sep +
            format.blue +
            "Available options:\n" +
            "-> benchmark"
        )
        # show available algorithms to the user
        for func in algorithms:
            print(f"-> {func} - {algorithms.index(func)}")
        print(format.normal + sep[1:-1])
        # let the user choose one
        chosen = input(f"{format.cyan}Choose algorithm:\n{format.green}>>{format.normal} ")
        # check if it's available and replace it in args
        if chosen in algorithms + ("benchmark",):
            args[1] = chosen
        else:
            # also index is an option
            try:
                args[1] = algorithms[int(chosen)]
            except:
                exit(1)

    # call benchmark if specified
    if len(args) >= 2 and args[1] == "benchmark":
        # if size given, use it
        if len(args) > 3 and args[2] == "size":
            benchmark(algorithms,args[3],[])
        # else use data array
        else:
            benchmark(algorithms,"",data)
        # exit to prevent further execution
        return

    # now set selected algorithm
    try:
        algorithm = algorithms[int(args[1])]
    except:
        algorithm = args[1]
    # get name of function
    sortfunc = getattr(functions.default(), algorithm)

    # sort the data and measure time
    begin = time()
    sorted = sortfunc(data)
    end = time()

    # check if multible or only one item in array
    if len(data) == 1:
        num = " item"
    else:
        num = " items"
    # make sure once again that seperator is longer than text
    headline = algorithm.split("sort")[0].capitalize() + \
               " Sort Algorithm with " + str(len(data)) + num
    if len(headline) + 2 > len(sep) and not smallterm:
            sep = "\n" + (len(headline) + 1) * "-" + "\n"

    # format time
    time_display = format_time(end - begin)
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
        time_display +
        format.normal +
        sep[:-1]
    )

# protection
if __name__ == "__main__":
    # option to see errors
    if "debug" in sys.argv:
        main(sys.argv)
    else:
        try:
            # run main function with cmd arguments
            main(sys.argv)
        except:
            # show error in red
            print(format.red + "An error ocurred" + format.normal)
