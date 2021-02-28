import cv2
import numpy

def analyzeData(videofile):
	
	points = 0

	vidcap = cv2.VideoCapture(videofile)
	success, image = vidcap.read()
	lastColorAverage = 0
	while success:
		#Write the image
		cv2.imwrite("Step_One.jpg", image)

		#Get the average color
		avg_color_per_row = numpy.average(image, axis=0)
		avg_color = numpy.average(avg_color_per_row, axis=0)
		x, y, z = avg_color
		avgAvg = (x+y+z)/3

		if lastColorAverage-avgAvg > 50 or lastColorAverage-avgAvg < -50:
			points += 1

		print(lastColorAverage-avgAvg)

		lastColorAverage = avgAvg

		success, image = vidcap.read()
	
	if(points > 10):
			print(f"Video is seizure inducing. Total of {str(points)} seizure points.")
	else:
		print(f"video is not harmful with {str(points)} points.")

analyzeData("minecraft.mp4")


