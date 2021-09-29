from cv2 import imwrite

def save_image(inputfile, image, suffix="_grayscale"):
  # Convert datatype in numpy array to integers (not floats).
  image = image.astype("uint8")

  # Extract file-extention to tuple: (<base filename>, ".", <file-extention>)
  outputfile = inputfile.rpartition(".")

  # Save image to file with the specified suffix.
  imwrite(outputfile[0] + suffix + "." + outputfile[2], image)
