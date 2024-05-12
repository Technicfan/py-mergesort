# sort functions that count steps for benchmark
class bench:
    # init steps
    def __init__(self):
        self.steps = 0

    # first part of the merge sort algorithm
    def mergesort(self,array):
        # check if array has multible elements
        self.steps += 1
        if len(array) > 1:
            # mergesort the array recursively
            half = len(array) // 2
            left = self.mergesort(array[:half])
            right = self.mergesort(array[half:])
            self.steps += 4
            return self.merge(left,right)
        else:
            # nothing to do if only one element or less
            return array
    # second (more complex) part of the algorithm
    def merge(self,left,right):
        sorted = []
        self.steps += 1
        # repeat this until one array is empty
        while len(left) > 0 and len(right) > 0:
            self.steps += 2
            # add smaller value to result and delete it from input
            if left[0] < right[0]:
                sorted.append(left[0])
                del left[0]
            else:
                sorted.append(right[0])
                del right[0]
            self.steps += 3
        self.steps += 2
        # return all arrays together
        return sorted + left + right

    # quick sort algorithm
    def quicksort(self,array):
        # init arrays
        less = []
        equal = []
        greater = []
        self.steps += 4
        # check if multible items in array
        if len(array) > 1:
            # use first element as pivot
            pivot = array[len(array) // 2]
            self.steps += 1
            for item in array:
                # smaller items in less
                if item < pivot:
                    less.append(item)
                    self.steps += 2
                # same items in equal
                elif item == pivot:
                    equal.append(item)
                    self.steps += 3
                # bigger items in greater
                else:
                    greater.append(item)
                    self.steps += 3
            # return all arrays after another
            self.steps += 2
            return self.quicksort(less) + equal + self.quicksort(greater)
        # one or less items -> nothing to do
        else:
            return array

    # bubble sort algorithm
    def bubblesort(self,array):
        # save array to local var to prevent changing input outside of function
        array = array[:]
        for item in array:
            self.steps += 1
            for i in range(len(array)-1):
                # check if next item is smaller
                if array[i] > array[i+1]:
                    # swap items
                    array[i], array[i+1] = array[i+1], array[i]
                    self.steps += 1
                self.steps += 1
        return array

    # selection sort algorithm
    def selectionsort(self,array):
        # same as above
        array = array[:]
        self.steps += 1
        for index in range(len(array)):
            # set start index to loop var
            min = index
            self.steps += 2
            for i in range(index+1,len(array)):
                # check if the current item is smaller
                if array[i] < array[min]:
                    # set min to this
                    min = i
                    self.steps += 1
                self.steps += 1
            # check if min changed
            if min != index:
                # swap items
                array[min], array[index] = array[index], array[min]
                self.steps += 1
            self.steps += 1
        return array

    # gnome sort algorithm
    def gnomesort(self,array):
        # same as above
        array = array[:]
        # start at the beginning
        index = 0
        self.steps += 1
        while index < len(array):
            self.steps += 1
            # check if index is 0 or previous item is smaller
            if index == 0 or array[index] >= array[index-1]:
                # move on
                index += 1
                self.steps += 1
            else:
                # swap current and previous item
                array[index], array[index-1] = array[index-1], array[index]
                # go back
                index -= 1
                self.steps += 1
            self.steps += 2
        self.steps += 1
        return array

    # insertion sort algorithm
    def insertionsort(self,array):
        # same as above
        array = array[:]
        self.steps += 1
        for i in range(len(array)-1):
            # next item and next index
            nexti = i + 1
            next = array[nexti]
            self.steps += 2
            # move values right as long as they're smaller
            while nexti > 0 and next < array[nexti-1]:
                self.steps += 2
                array[nexti] = array[nexti-1]
                nexti -= 1
                self.steps += 1
            # achieve swapping
            array[nexti] = next
            self.steps += 1
        return array

# normal sort functions
class default:
    # first part of the merge sort algorithm
    def mergesort(self,array):
        # check if array has multible elements
        if len(array) > 1:
            # mergesort the array recursively
            half = len(array) // 2
            left = self.mergesort(array[:half])
            right = self.mergesort(array[half:])
            return self.merge(left,right)
        else:
            # nothing to do if only one element or less
            return array

    # second (more complex) part of the algorithm
    def merge(self,left,right):
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

    # quick sort algorithm
    def quicksort(self,array):
        # init arrays
        less = []
        equal = []
        greater = []
        # check if multible items in array
        if len(array) > 1:
            # use first element as pivot
            pivot = array[len(array) // 2]
            for item in array:
                # smaller items in less
                if item < pivot:
                    less.append(item)
                # same items in equal
                elif item == pivot:
                    equal.append(item)
                # bigger items in greater
                else:
                    greater.append(item)
            # return all arrays after another
            return self.quicksort(less) + equal + self.quicksort(greater)
        # one or less items -> nothing to do
        else:
            return array

    # bubble sort algorithm
    def bubblesort(self,array):
        # save array to local var to prevent changing input outside of function
        array = array[:]
        for item in array:
            for i in range(len(array)-1):
                # check if next item is smaller
                if array[i] > array[i+1]:
                    # swap items
                    array[i], array[i+1] = array[i+1], array[i]
        return array

    # selection sort algorithm
    def selectionsort(self,array):
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

    # gnome sort algorithm
    def gnomesort(self,array):
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

    # insertion sort algorithm
    def insertionsort(self,array):
        # same as above
        array = array[:]
        for i in range(len(array)-1):
            # next item and next index
            nexti = i + 1
            next = array[nexti]
            # move values right as long as they're smaller
            while nexti > 0 and next < array[nexti-1]:
                array[nexti] = array[nexti-1]
                nexti -= 1
            # achieve swapping
            array[nexti] = next
        return array