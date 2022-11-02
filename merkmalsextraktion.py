#!/usr/bin/env python3

import sys
import pickle
import random
import math
import numpy as np
from PIL import Image, ImageStat, ImageOps

from basics import Concept, FeatureVector, ClassifiedFeatureVector

class ImageAnalysis(object):
	"""docstring for ImageAnalysis"""
	def __init__(self, file):
		self.img = Image.open(file)
		self.img.convert("RGB")

		self._prepare()
		self.stat = ImageStat.Stat(self.img)

	@property
	def pixel_count(self):
		return self.img.width * self.img.height
	
	def _prepare(self):
		inv = ImageOps.invert(self.img)
		bbox = inv.getbbox()
		self.img = self.img.crop(bbox)
		self.img.save("debugimg.bmp")


	def histogram(self):
		return tuple(map(lambda x: sum(x)/self.pixel_count, np.array_split(self.img.histogram(), 768/16)))

	def mean_red(self):
		return self.stat.mean[0]

	def mean_green(self):
		return self.stat.mean[1]

	def mean_blue(self):
		return self.stat.mean[2]

	def perceived_brightness(self):
		r,g,b = self.stat.mean
		return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
		


def evaluateImage(image):
	ia = ImageAnalysis(image)
	return FeatureVector([
		ia.mean_red()/255,
		ia.mean_green()/255,
		ia.mean_blue()/255,
		ia.perceived_brightness()/255,
		*ia.histogram(),
		])


def main(destination, classification, *files):
	if destination == "-":
		destination = "/dev/null"
	examples = set()

	# Ensure whether classification exists
	concept = Concept[classification]

	for file in files:
		fv = evaluateImage(file)
		print(f"{classification}:\t{fv}")
		#f.write(f"{classification}:\t{fv}\n")
		examples.add(ClassifiedFeatureVector(fv, concept=concept))

	assert len(examples) > 10
	testing = set(random.sample(list(examples), int(0.4*len(examples))))

	with open(destination, "wb") as f:
		pickle.dump(dict(training=examples.difference(testing), testing=testing), f)


if __name__ == '__main__':
	main(sys.argv[-1], sys.argv[-2], *sys.argv[1:-2])
