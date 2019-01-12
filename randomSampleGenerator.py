import random
from datetime import datetime
import time

#
# Generate "total" "None" type values
#
class noneGenerator:
    def __init__(self, total):
        self.index = 0
        self.total = total
    def __iter__(self):
        return self
    def __next__(self):
        if self.index < self.total:
            self.index += 1
            return None
        else:
            raise StopIteration

#
# Generate "total" "Boolean" type values, each could be True or False
#
class boolGenerator:
    def __init__(self, total):
        self.index = 0
        self.total = total
        self.min = min
        self.max = max

    def __iter__(self):
        return self
    def __next__(self):
        if self.index < self.total:
            self.index += 1
            return random.randint(0, 1) == 1
        else:
            raise StopIteration

#
# Generate "total" "Integer" type values, each between range of [min, max)
#
class intGenerator:
    def __init__(self, total, min, max, negativeAllow = False):
        self.index = 0
        self.total = total
        self.min = min
        self.max = max
        self.negativeAllow = negativeAllow

    def __iter__(self):
        return self
    def __next__(self):
        if self.index < self.total:
            self.index += 1
            num = random.randrange(self.min, self.max)
            if self.negativeAllow and random.randint(0, 9) % 2 == 0:
                num *= -1
            return num
        else:
            raise StopIteration

#
# Generate "total" "Float" type values, each between range of [min, max), min and max to be int
#
class floatGenerator:
    def __init__(self, total, min, max, negativeAllow = False):
        self.index = 0
        self.total = total
        self.min = int(min)
        self.max = int(max)
        self.negativeAllow = negativeAllow

    def __iter__(self):
        return self
    def __next__(self):
        if self.index < self.total:
            self.index += 1
            num = random.random() * random.randrange(self.min, self.max)
            if self.negativeAllow and random.randint(0, 9) % 2 == 0:
                num *= -1
            return num
        else:
            raise StopIteration

#
# Generate "total" "String" type values, length of each element is in range of [minLength, maxLength)
# charset can be chosen among alphabet, number, punctuation and customized charset, and the combination of them
#
class stringGenerator:
    def __init__(self, total, minLength, maxLength, alphabetAllow = True, numberAllow = True, punctuationAllow = False, otherChars = []):
        numberTable = [chr(ascii) for ascii in range(48, 58)] # [0-9]
        alphabetTable = [chr(ascii) for ascii in range(65, 91)] # [A-Z]
        alphabetTable.extend([chr(ascii) for ascii in range(97, 123)]) # [a-z]
        punctuationTable = [' ','!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','<','=','>','?','@','[','\\',']','^','_','`','{','|','}','~']

        self.index = 0
        self.total = total
        self.minLength = int(minLength)
        self.maxLength = int(maxLength)

        self.charSet = otherChars
        if alphabetAllow:
            self.charSet.extend(alphabetTable)
        if numberAllow:
            self.charSet.extend(numberTable)
        if punctuationAllow:
            self.charSet.extend(punctuationTable)

    def __iter__(self):
        return self
    def __next__(self):
        if self.index < self.total:
            self.index += 1
            stringLength = random.randrange(self.minLength, self.maxLength)
            return ''.join(random.choices(self.charSet, k = stringLength))
        else:
            raise StopIteration

#
# Generate "total" "Datetime" type values, each element is in range of [minDatetime, maxDatetime)
# e.g. datetimeGenerator(5, datetime.strptime('2018-01-01 00:00:01', "%Y-%m-%d %H:%M:%S"), datetime.strptime('2018-12-31 23:59:59', "%Y-%m-%d %H:%M:%S"))
#
class datetimeGenerator:
    FORMAT = "%Y-%m-%d %H:%M:%S"
    def __init__(self, total, minDatetime, maxDatetime):
        self.index = 0
        self.total = total
        self.minInSecond = int(time.mktime(minDatetime.timetuple()))
        self.maxInSecond = int(time.mktime(maxDatetime.timetuple()))

    def __iter__(self):
        return self
    def __next__(self):
        if self.index < self.total:
            self.index += 1
            secondsSinceEpoch = random.randrange(self.minInSecond, self.maxInSecond)
            return datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secondsSinceEpoch)),"%Y-%m-%d %H:%M:%S")
        else:
            raise StopIteration

#
# Generate a one-dimension"Array" each iteration, repeat it for "total" times
# each element is of determined data type generated from random value generator
# if the number of generators is less then array size, they are used in rotation
# for example:
# arrGen = arrayGenerator(5, 8, [intGenerator(0, 0, 10), stringGenerator(0, 3, 8), boolGenerator(0)])
# for item in arrGen:
#     print(item)
#
class arrayGenerator:
    def __init__(self, total, arrayLength, generators):
        self.index = 0
        self.total = total
        self.arrayLength = arrayLength
        for gen in generators:
            gen.total = total * arrayLength
        self.generators = generators

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < self.total:
            self.index += 1
            arr = []
            for c in range(self.arrayLength):
                gen = self.generators[c % len(self.generators)]
                arr.append(gen.__next__())
            return arr
        else:
            raise StopIteration

if __name__ == '__main__':
    arrGen = arrayGenerator(500000000, 7, [intGenerator(0, 1, 10000000000000000000), intGenerator(0, 1, 10000000000),
                                   stringGenerator(0, 3, 20), stringGenerator(0, 3, 20),
                                   intGenerator(0, 1, 10000000000),
                                   stringGenerator(0, 3, 20), stringGenerator(0, 3, 20)])
    for item in arrGen:
        print(item)