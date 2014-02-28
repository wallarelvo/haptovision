
import cv2
import sys
import numpy as np
import blob
import feedback

cv2.namedWindow('Display Window')
COLOR_MIN = np.array([0, 0, 0], np.uint8)
COLOR_MAX = np.array([0, 0, 0], np.uint8)
BLOB_COLOR = (0, 255, 0)
padding = 0
blobSize = 0
bList = list()


def getSoundFeedbackController():

    binary_feedback = feedback.BinaryFeedbackController()
    sound_event = feedback.events.SoundEvent()
    text_event = feedback.events.TextEvent()
    binary_feedback.add_event(sound_event)
    binary_feedback.add_event(text_event)
    return binary_feedback


binary_feedback = getSoundFeedbackController()


def printStats():
	print "Blob Threshold:", blobSize
	print "Range:", padding
	print "HSV:", COLOR_MAX


def changedBlobSize(thresh):
	global blobSize
	blobSize = thresh
	changedRange(padding)


def changedRange(nRange):
	global padding
	padding = nRange
	changed(0)(COLOR_MAX[0])
	changed(1)(COLOR_MAX[1])
	changed(2)(COLOR_MAX[2])


def changed(channel):
	def changedChannel(thresh):
		COLOR_MAX[channel] = thresh
		COLOR_MIN[channel] = thresh - padding if thresh - padding > 0 else 0
		global img, img_hsv, bList
		img_disp = np.copy(img)
		img_thresh = cv2.inRange(img_hsv, COLOR_MIN, COLOR_MAX)
		bList = blob.getBlobs(img_thresh, blobSize)

		for b in bList:
		    cv2.fillConvexPoly(img_disp, b.getConvexHull(), BLOB_COLOR)

		cv2.imshow('Display Window', img_disp)
	return changedChannel


def on_mouse(event, x, y, flags, param):
    binary_feedback.push(bList, x, y)


def main():
	if len(sys.argv) != 2:
	    print "Usage : python display_image.py <image_file>"

	else:
		global img, img_hsv
		img = cv2.imread(sys.argv[1], cv2.CV_LOAD_IMAGE_COLOR)

		if (img == None):
			print "Could not open or find the image"
		else:
			img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			img_thresh = cv2.inRange(img, COLOR_MIN, COLOR_MAX)

			cv2.createTrackbar('Hue:','Display Window', 0, 255, changed(0))
			cv2.createTrackbar(
			    'Saturation:','Display Window', 0, 255, changed(1)
			)
			cv2.createTrackbar(
			    'Value:','Display Window', 0, 255, changed(2)
			)
			cv2.createTrackbar(
			    'Blob', 'Display Window', 0, 50000, changedBlobSize
			)
			cv2.createTrackbar(
			    'Range:', 'Display Window', 0, 255, changedRange
			)

			cv2.imshow('Display Window',img)
			cv2.setMouseCallback('Display Window', on_mouse)

			cv2.waitKey(0)
			cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
