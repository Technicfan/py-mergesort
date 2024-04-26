#!/bin/python3

from time import time

array = [ 2, 20, 100, 1, 50, 5, 200, 10 ]

def mergesort(data):
    if len(data) == 1:
        return data
    half = len(data) // 2
    left = mergesort(data[:half])
    right = mergesort(data[half:])
    return merge(left,right)

def merge(left,right):
    sorted = []
    while len(left) > 0 and len(right) > 0:
        if left[0] < right[0]:
            sorted.append(left[0])
            del left[0]
        else:
            sorted.append(right[0])
            del right[0]

    sorted += left
    sorted += right

    return sorted

print(
"""Merge Sort
-------------
array:
""" + 
str(array) + 
"""
-------------
sorted array:"""
)

begin = time()
print(mergesort(array))
end = time()

print(
"""-------------
sorting took """ + 
str(round((end-begin)*10**3,2)) + 
" ms"
)
    