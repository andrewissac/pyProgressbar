import sys
import colorsys as c
from collections import deque

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

def hlsToBash(h,l,s):
    r,g,b = tuple(int(x * 255) for x in c.hls_to_rgb(h, l, s))
    return rgbToBash(r,g,b)

class Progressbar():
    def __init__(
        self, totalCount, segments = 60, bold = False, rainbowWaveEnabled = True, 
        animateLeftToRight = True, animationSpeed = 5, rainbowColorChangeSpeed = 2.0, 
        rainbowColorIncrement = 25, luminosity = 0.65, saturation = 1.0):
        self.totalCount = totalCount
        # segments % len(displayPattern) should be 0 to get a perfect loop
        self.segments = segments
        self.bold = bold
        self.rainbowWaveEnabled = rainbowWaveEnabled
        self.__rainbowColorIncrement = rainbowColorIncrement
        self.animationSpeed = 5 # every 5 steps -> cyclic rotate displaypattern, may vary on each case!
        self.animateLeftToRight = animateLeftToRight
        self.rainbowColorChangeSpeed = rainbowColorChangeSpeed
        self.luminosity = luminosity
        self.saturation = saturation
        self.patterns = { 
            "wave" : ',.~*^`^*~.', 
            "tableflip" : '(ノಠ 益ಠ)ノ彡┻━┻........', 
            "rectangles" : '▮'
        }
        self.displayPattern = self.__generateCharsDeque(self.patterns["wave"])

    def AddNewDisplayPattern(self, patternName: str, patternString: str):
        self.patterns[patternName] = patternString
    
    def SetDisplayPattern(self, dispPattern: str):
        if (dispPattern not in self.patterns.keys()):
            self.AddNewDisplayPattern(dispPattern, dispPattern)
        self.displayPattern = self.__generateCharsDeque(self.patterns[dispPattern])
    
    def AddAndSetNewDisplayPattern(self, patternName: str, patternString: str):
        self.AddNewDisplayPattern(patternName, patternString)
        self.SetDisplayPattern(patternName)

    def ShowProgress(self, count: int = 0, message: str= ''):
        if(count % self.animationSpeed == 0): # simple mechanism to only rotate chars every n loop steps (may vary in your case)
            if(self.animateLeftToRight):
                self.displayPattern.rotate(-1) # cyclic rotation of displayPattern
            else:
                self.displayPattern.rotate(1) # cyclic rotation of displayPattern
        filledProgressbarSegments = int(round(self.segments * count / float(self.totalCount)))

        # using HLS colorspace
        h = 0.0 
        if (count / float(self.totalCount)) * self.rainbowColorChangeSpeed < 1.0:
            h = (count / float(self.totalCount)) * self.rainbowColorChangeSpeed
        else:
            h = (count / float(self.totalCount)) * self.rainbowColorChangeSpeed - 1.0 # make it repeat (remember hue interval: 0..1)
        l = self.luminosity # should be between 0 and 1
        s = self.saturation # should be between 0 and 1

        percentage = round(100.0 * count / float(self.totalCount-2), 1)
        bar = hlsToBash(h,l,s)
        if self.bold:
            bar += bcolors.BOLD
        if self.rainbowWaveEnabled:
            h_increment = (self.__rainbowColorIncrement / float(self.totalCount)) * self.rainbowColorChangeSpeed
            for i in range(filledProgressbarSegments):
                bar += self.displayPattern[i] + hlsToBash(h,l,s)
                h += h_increment
        else:
            for i in range(filledProgressbarSegments):
                bar += self.displayPattern[i]
        bar += bcolors.ENDC
        bar += '-' * (self.segments - filledProgressbarSegments)

        if(count >= self.totalCount-1):
            sys.stdout.write('\n')
            sys.stdout.flush()
            return
        sys.stdout.write('[{0}] {1}% ...{2}\r'.format(bar, percentage, message))
        sys.stdout.flush()

    def __generateCharsDeque(self, patternString: str):
        chars = [char for char in patternString]
        dispPattern = deque(self.__repeatList(chars, self.segments))
        return dispPattern

    def __repeatList(self, l, n):
        '''
        Repeats a given list l until length n is reached.
        e.g. [1,2,3] -> repeatList([1,2,3], 7) -> returns [1,2,3,1,2,3,1]
        '''
        l.extend(l * n)
        l = l[:n]
        return l
