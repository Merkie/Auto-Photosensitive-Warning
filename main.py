"""
Filename:
    main.py

Function:
    Analyzies video files to detect flashing footage and issue an automatic warning if flashing footage is detected

Important notes:
    Code should be formatted by black and checked for flashes by pylint
"""

import cv2
import numpy
import sys

# Takes as input (from command line) a video file to scan

if len(sys.argv) < 2:
    print("Example usage: python main.py 'yourfile.mp4'")
    print("You forgot to enter arguments!")
    sys.exit()
else:
    source = sys.argv[1]
    print("You chose the video file", source)

# Primary video analyzing function

def analyzeData(videofile):
    vidcap = cv2.VideoCapture(videofile)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    lastColorAverage = 0
    points = 0
    frameCount = 0
    secondCounter = 0

    success, image = vidcap.read()

    while success:
        frameCount += 1

        # Get the average color
        r, g, b = numpy.average(numpy.average(image, axis=0), axis=0)
        avgAvg = (r + g + b) / 3

        # If the difference between the two frames is greator or less than a certain threshold
        if lastColorAverage - avgAvg > 50 or lastColorAverage - avgAvg < -50:
            points += 1

        # Debug
        if frameCount == fps:
            if points > 0:
                print(f"{points} points in a second {secondCounter}")
            frameCount = 0
            secondCounter += 1
            points = 0

        # Reset the lastColorAverage
        lastColorAverage = avgAvg

        success, image = vidcap.read()

if __name__ == "__main__":
    print("Beginnning analysis...")
    analyzeData(source)
