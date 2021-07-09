"""
Filename:
    main.py

Function:
    Analyzies video files to detect flashing footage and issue an automatic warning if flashing footage is detected

Important notes:
    Code should be formatted by black and checked for bugs by pylintb
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

# Prettified table printing function


def tableOutput(
    time: int,
    num_points: int,
    print_table_title: bool = True,
    title: list = ["Time(seconds)", "Number of points"],
):
    """
    Usage:
        tableOutput(arg1, arg2, arg3, arg4)
        > Time(seconds)       Number of points
          1s                  3 points
          2s                  5 points
          3s                  4 points

    Variables:
        Arg1 - time must be an int
        Arg2 - num_points must be an int
        Arg3 - (Optional) print_table_title is a boolean and is set to true by default
        Arg4 - (Optional) title must be a list and will be handled by a fallback if not provided
    """
    if print_table_title == True:
        # Print title via python's format function
        print("{:<20} {:<30}".format(title[0], title[1]))
    time = str(time) + "s"
    num_points = str(num_points) + " points"
    print("{:<20} {:<30}".format(time, num_points))


# Primary video analyzing function


def analyzeData(videofile: str, headlessMode: bool = False):
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
                # Only print output if not in headless mode
                if not headlessMode:
                    if secondCounter < 1:
                        # Run the table printing function for pretty output
                        tableOutput(secondCounter, points)
                    else:
                        # We want to print the table title only once
                        # so we set "print_table_title" to false
                        # when we run the table printing function again
                        tableOutput(secondCounter, points, False)
            frameCount = 0
            secondCounter += 1
            points = 0

        # Reset the lastColorAverage
        lastColorAverage = avgAvg
        success, image = vidcap.read()

    # Return average number of flashes per second
    return avgAvg


if __name__ == "__main__":
    print("Beginnning analysis...\n")
    analyzeData(source)
    if analyzeData(source, headlessMode=True) > 3:
        print(
            "\n[WARN]: Footage contains flashes and is not suitable for photosensitive individuals"
        )
