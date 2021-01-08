# pyProgressbar
Rainbow progressbar for bash output using python

```python
# region usage example
from time import sleep

def simulateLongTask(progressbar):
    for i in range(total):
        sleep(0.02) # simulate task that takes a while
        progressbar.ShowProgress(i, 'myMessage')

# demo usage
total = 1500
progressbar = Progressbar(total)
# optional parameters that can be set to your liking
progressbar.SetDisplayPattern("wave")
progressbar.animateLeftToRight = True
progressbar.animationSpeed = 5
progressbar.rainbowWaveEnabled = True

simulateLongTask(progressbar)

progressbar.SetDisplayPattern("rectangles")
simulateLongTask(progressbar)

progressbar.SetDisplayPattern("tableflip")
progressbar.rainbowColorChangeSpeed = 1.0
progressbar.animateLeftToRight = False
simulateLongTask(progressbar)

progressbar.SetDisplayPattern("rectangles")
progressbar.rainbowWaveEnabled = False
progressbar.rainbowColorChangeSpeed = 3.0
simulateLongTask(progressbar)

# you can also set your own DisplayPattern
progressbar.AddNewDisplayPattern("myPattern", "CustomDisplayPattern") # segments % len(displayPattern) should be 0 to get a perfect loop
progressbar.SetDisplayPattern("myPattern")
# you could also add and set the displaypattern in one line
# progressbar.AddAndSetNewDisplayPattern("myNewPattern", "CustomDisplayPattern")
progressbar.rainbowWaveEnabled = True
progressbar.rainbowColorChangeSpeed = 1.0
simulateLongTask(progressbar)
# endregion
```
