#!/usr/bin/env python3

from enum import Enum
import math
import numpy as np


def memoize(f):
	cache = {}
	def foo(x):
		if x not in cache:
			cache[x] = f(x)
		return cache[x]
	return foo

def my_reduce(fn, coll, init=[]):
	for i,el in enumerate(coll):
		init = fn(init, el, coll, i)
	return init


class Concept(Enum):
	"""docstring for Concept"""
	Unknown = 0
	Stop = 1
	GiveWay = 2
	PriorityToTheRight = 3
	PriorityRoad = 4
	TurnLeft = 5
	TurnRight = 6


class FeatureVector(tuple):
	"""docstring for FeatureVector"""
	def __new__(self, arg):
		return tuple.__new__(FeatureVector, arg)

class ClassifiedFeatureVector(FeatureVector):
	def __new__(self, arg, concept=Concept.Unknown):
		fv = FeatureVector.__new__(ClassifiedFeatureVector, arg)
		fv._concept = concept
		return fv

	@property
	def concept(self):
		return self._concept

class Perceptron(object):
	"""docstring for Perceptron"""
	def __init__(self, dim, concept_mapping, bias=1):
		if type(dim) == list:
			self._dim = len(dim)
			self._weights = dim +[bias]
		else:
			self._dim = dim
			self._weights = [1/dim] *dim +[bias]
		self.concept_mapping = concept_mapping

	@property
	def dim(self):
		return self._dim

	@property
	def weights(self):
		return self._weights

	@property
	def bias(self):
		return self._weights[self._dim]

	def raw(self, feature_vector):
		return np.dot(self._weights, list(feature_vector) +[1])

	def run(self, feature_vector):
		return self.raw(feature_vector)

	def train(self, training_set, learning_rate=0.0001):
		diffs = []
		for classified_feature_vector in training_set:
			correct_answer = classified_feature_vector._concept
			vector = list(classified_feature_vector) +[1]

			desired_output = self.get_mapped_value(correct_answer)
			actual_output = self.raw(classified_feature_vector)
			diff = desired_output - actual_output

			for i in range(self._dim):
				self._weights[i] += learning_rate * (vector[i] if diff > 0 else -vector[i])
				#self._weights[i] += learning_rate * diff*vector[i]

			diffs.append(abs(diff))
			#print(f"[Training]  diff was {diff} ({desired_output}: {actual_output})")

		mean_error, max_error, min_error = (np.mean(diffs), max(diffs), min(diffs))
		return (mean_error, max_error, min_error)

	def assess_error(self, testing_set):
		diffs = []
		for classified_feature_vector in testing_set:
			correct_answer = classified_feature_vector._concept

			desired_output = self.get_mapped_value(correct_answer)
			actual_output = self.raw(classified_feature_vector)
			diff = desired_output - actual_output

			diffs.append(abs(diff))

		mean_error, max_error, min_error = (sum(diffs)/len(diffs), max(diffs), min(diffs))
		return (mean_error, max_error, min_error)

	def get_mapped_value(self, concept):
		if type(self.concept_mapping) in (list, tuple):
			return 1 if concept in self.concept_mapping or concept.name in self.concept_mapping else 0
		elif type(self.concept_mapping) == dict:
			return self.concept_mapping.get(concept) or 0
		elif type(self.concept_mapping) == type(lambda: 0):
			return self.concept_mapping(concept)
		else:
			raise ValueError("Perceptron was not initialized with concept_mapping as a supported type. (sorry we didn't check right away)")


class MulticlassPerceptron(Perceptron):
	"""docstring for Perceptron"""
	def __init__(self, dim, Concept_enum, bias=1):
		self.Concept_enum = Concept_enum
		concept_mapping = dict([(x.name, x.value) for x in Concept_enum])
		super(MulticlassPerceptron, self).__init__(dim, concept_mapping, bias=bias)

	def run(self, feature_vector):
		try:
			return self.Concept_enum(round(self.raw(feature_vector)))
		except ValueError:
			return self.Concept_enum.Unknown
