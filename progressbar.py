# based on https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
# The MIT License (MIT)
# Copyright (c) 2016 Vladimir Ignatev
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import colorsys as c

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def rgbToBash(r,g,b):
    return '\033[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'

def progress(count, total, cycleCharsDeque, progressbarSegments = 60, boldChars = False, message='', colorChangeSpeedParam = 1.0): 
    # progressbarSegments % len(waveCharsDeque) should be 0 to ensure a perfect loop
    progressbarSegments = progressbarSegments # number of bar segments
    filledProgressbarSegments = int(round(progressbarSegments * count / float(total))) # number of bar segments that are filled
    h = 0.0

    if (count / float(total)) * colorChangeSpeedParam < 1.0:
        h = (count / float(total)) * colorChangeSpeedParam
    else:
        h = (count / float(total)) * colorChangeSpeedParam - 1.0 # make it repeat (remember h interval 0..1)
    l = 0.6
    s = 1.0
    r,g,b = tuple(int(x * 255) for x in c.hls_to_rgb(h, l,s ))

    percentage = round(100.0 * count / float(total), 1)
    bar = rgbToBash(r,g,b)
    if boldChars:
        bar += bcolors.BOLD
    for i in range(filledProgressbarSegments):
        bar += cycleCharsDeque[i]
    bar += '-' * (progressbarSegments - filledProgressbarSegments)
    bar += bcolors.ENDC

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percentage, '%', message))
    sys.stdout.flush()

def repeatList(l, n):
    '''
    Repeats a given list l until length n is reached.
    e.g. [1,2,3] -> repeatList([1,2,3], 7) -> returns [1,2,3,1,2,3,1]
    '''
    l.extend(l * n)
    l = l[:n]
    return l

# region usage example
# from time import sleep
# from collections import deque
# total = 1500 # could be any number depending on your problem
# wave = ',.~*^`^*~.'
# tableflip = '(ノಠ 益ಠ)ノ彡┻━┻........'
# chars = [char for char in wave]

# progressbarSegments = 60 # 
# cycleCharsDeque = deque(repeatList(chars, progressbarSegments)) # deque needed for cyclic rotation of chars

# for i in range(total):
#     sleep(0.02) # simulate task that takes a while

#     progress(count=i, total=total, cycleCharsDeque=cycleCharsDeque, boldChars=False, progressbarSegments=progressbarSegments, message='LUUUL', colorChangeSpeedParam=4.0)
#     if(i % 5 == 0): # simple mechanism to only rotate chars every 5 loop steps (may vary in your case)
#         cycleCharsDeque.rotate(-1) # cyclic rotation of charsList
# endregion 
