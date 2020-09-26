# BirdEyeView
Dependency
- OpenCv 4.4.0

Environnment
- Python 3.8.5
- Windows 10 2004

# Executing
Run GetParameters.py. Find two lines that are parrallel in real life, but aren't in the camera frame. These lines will delimit the final frame and warping, thus make sure to find lines that are close to the sides, the closer the better. Start with the first line, start from the top left and hold you mouse until you have reached the bottom of that line. Repeat this step, but on the top right. Check Image Below.
![GetParameters.py](https://raw.githubusercontent.com/AquarelMc/BirdEyeView/master/Capture63.PNG)
Program will then exit after printing out 5 parameters calculated from the two given lines. Copy these numbers to BirdEyeView.py and run. Upon running, the camera's perspective will(hopefully) be changed to a bird eye view.
![BirdEyeView.py](https://raw.githubusercontent.com/AquarelMc/BirdEyeView/master/Capture64.PNG)

# Algorithms
To find the final vertical scaling factor, the following has been used:
![VerticalScaleSolving](https://raw.githubusercontent.com/AquarelMc/BirdEyeView/master/Capture65.PNG)

To find the camera angle, nonlinear curve fitting has been used:
![Excel Sheet](https://raw.githubusercontent.com/AquarelMc/BirdEyeView/master/Capture66.PNG)
[Excel Sheet](https://github.com/AquarelMc/BirdEyeView/blob/master/Relation%20Between%20Camera%20Angle%20And%20Perspective.xlsx?raw=true)
