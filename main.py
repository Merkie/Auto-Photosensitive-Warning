import cv2
import numpy


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


analyzeData("tests/tests.mp4")
