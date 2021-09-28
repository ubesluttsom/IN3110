import cv2
import numpy

image = cv2.imread("rain.jpg")
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

sum_image = image.sum(axis=2)
#breakpoint()
#image = image*numpy.array([[ 0.07, 0.72, 0.21 ]])
#numpy_image = image.mean(axis=2)
image[:,:,0] = numpy_image*0.07/3
image[:,:,1] = numpy_image*0.72/3
image[:,:,2] = numpy_image*0.21/3
#breakpoint()


numpy_image = numpy_image.astype("uint8")
cv2.imwrite("rain_grayscale.jpg", numpy_image)
