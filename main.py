"""
Filename:
    main.py

Function:
    Analyzies video files to detect flashing footage
    and issue an automatic warning if flashing
    footage is detected

Important notes:
    Code should be formatted by black and checked for bugs by pylintb
"""

import sys
import numpy
from cv2 import cv2

# Takes as input (from command line) a video file to scan

if len(sys.argv) < 2:
    print("Example usage: python main.py 'yourfile.mp4'")
    print("You forgot to enter arguments!")
    sys.exit()
else:
    source = sys.argv[1]
    print("You chose the video file", source)

# Prettified table printing function


def table_output(
    time: int,
    num_points: int,
    print_table_title: bool = True,
    title: list = None,
):
    """
    Usage:
        table_output(arg1, arg2, arg3, arg4)
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
    # For safety purposes, we have to specify title as Nonetype
    # so that it doesn't get changed by default upon every call of
    # the function
    if title is None:
        title = ["Time(seconds)", "Number of points"]
    if print_table_title is True:
        # Print title via python's format function
        print("{:<20} {:<30}".format(title[0], title[1]))
    time = str(time) + "s"
    num_points = str(num_points) + " points"
    print("{:<20} {:<30}".format(time, num_points))


# Primary video analyzing function


def analyze_data(videofile: str, headless_mode: bool = False):
    """
    Usage:
        analyzedata(arg1, arg2)
        E.g. analyzedata("somefile.mp4", False)
    Variables:
        Arg1 - (required) relative/absolute path to video file
        Arg2 - (option) whether to run "silently" and not print
               output to the command line
    """
    vidcap = cv2.VideoCapture(videofile)
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    last_color_average = 0
    points = 0
    frame_count = 0
    second_counter = 0

    success, image = vidcap.read()
    while success:
        frame_count += 1

        # Get the average color
        r, g, b = numpy.average(numpy.average(image, axis=0), axis=0)
        current_color_average = (r + g + b) / 3

        # If the difference between the two frames is greator or less than a certain threshold
        if (
            last_color_average - current_color_average > 50
            or last_color_average - current_color_average < -50
        ):
            points += 1

        # Debug
        if frame_count == fps:
            if points > 0:
                # Only print output if not in headless mode
                if not headless_mode:
                    if second_counter < 1:
                        # Run the table printing function for pretty output
                        table_output(second_counter, points)
                    else:
                        # We want to print the table title only once
                        # so we set "print_table_title" to false
                        # when we run the table printing function again
                        table_output(second_counter, points, False)
            frame_count = 0
            second_counter += 1
            points = 0

        # Reset the last_color_average
        last_color_average = current_color_average
        success, image = vidcap.read()

    # Return average number of flashes per second
    return current_color_average


if __name__ == "__main__":
    print("Beginnning analysis...\n")
    analyze_data(source)
    if analyze_data(source, headless_mode=True) > 3:
        print(
            "\n[WARN]: Footage contains flashes and is not suitable for photosensitive individuals"
        )
