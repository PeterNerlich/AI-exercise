#!/usr/bin/env python3

import sys
import math
import random
import pickle

from basics import Concept, Perceptron, MulticlassPerceptron


class WindowQueue(object):
	def __init__(self, size=10):
		self._list = []
		self._size = size

	def put(self, obj):
		self._list.append(obj)
		if len(self._list) > self._size:
			self._list = self._list[-self._size:]

	def __len__(self):
		return self._list.__len__()

	def __iter__(self):
		return self._list.__iter__()


class Learner(object):
	"""docstring for Learner"""
	def __init__(self, dim, perceptron=None):
		if perceptron:
			self._perceptron = perceptron
		else:
			self._perceptron = MulticlassPerceptron(Concept, dim)

	@property
	def dim(self):
		return self.perceptron.dim

	def learn(self, training, testing, learning_rate=0.001, abort_mean_error=.16, abort_max_error=.75, abort_iterations=800):
		mean_error, max_error, min_error = (math.inf, math.inf, -math.inf)
		last_error = None
		#next_to_last_error = None
		last_errors = WindowQueue(50)
		iterations = 0
		training = list(training)

		last_errors.put(math.inf)

		def show_diff(diff):
			pad = " " if diff >= 0 else ""
			return f"{pad}{round(diff, 4)}"

		while True:
			iterations += 1
			#next_to_last_error = last_error
			#last_error = mean_error

			random.shuffle(training)
			mean_error, max_error, min_error = self._perceptron.train(training, learning_rate=learning_rate)
			#mean_error, max_error, min_error = self._perceptron.train(training, Concept.TurnRight, learning_rate=learning_rate)
			mean_error, max_error, min_error = self._perceptron.assess_error(testing)
			windowed_mean = sum(last_errors)/len(last_errors)
			print(f"({iterations})\terror:\tmean: {mean_error}\t[{windowed_mean}]\tmin: {min_error}\tmax: {max_error}")
			#print(f"({iterations})\terror:\tmean: {mean_error}\t({show_diff(mean_error-last_error)})\tmin: {min_error}\tmax: {max_error}")
			last_errors.put(mean_error)

			if iterations >= 10:
				#if mean_error <= abort_mean_error:
				#	print(f"Mean error sufficiently low, stopping training!")
				#	break
				#if max_error <= abort_max_error:
				#	print(f"Max error sufficiently low, stopping training!")
				#	break
				#if next_to_last_error is not None and next_to_last_error - mean_error <= abort_change_rate:
				#	print(f"Last improvement in mean error sufficiently low, stopping training! ({last_error - mean_error})")
				#	break
				if iterations % 50 == 0:
					if (last_error is not None
							and abs(last_error-windowed_mean) < 0.0001):
						print(f"No mean error improvement in the last 10 iterations! Aborting training.")
						break
					else:
						last_error = windowed_mean
				if iterations > abort_iterations:
					print(f"TOO MANY ITERATIONS! Aborting training.")
					break

	def classify(self, example):
		#return Concept(self._perceptron.run(example))
		#return Concept(round(self._perceptron.run(example)))
		return self._perceptron.run(example)


def main(saved_state, target_state, task, *files):
	if saved_state == "-":
		saved_state = "/dev/null"
	if target_state == "-":
		target_state = "/dev/null"

	if saved_state.startswith("-"):
		#state = MulticlassPerceptron(int(saved_state[1:]), Concept)
		if task.startswith("learn:"):
			target_concepts = task.split(":")[1:]
			target_concepts = ":".join(target_concepts)
			target_concepts = tuple(target_concepts.split(","))
		state = Perceptron(int(saved_state[1:]), target_concepts)
	else:
		with open(saved_state, "rb") as f:
			state = pickle.load(f)
			assert type(state) is Perceptron

	learner = Learner(None, perceptron=state)
	training_set = set()
	testing_set = set()

	for file in files:
		with open(file, "rb") as f:
			addition = pickle.load(f)
			assert type(addition) is dict
			assert type(addition["training"]) is set
			assert type(addition["testing"]) is set
			training_set.update(addition["training"])
			testing_set.update(addition["testing"])

	if task == "classify":
		for example in testing_set:
			print(f"{example._concept}:\t{learner.classify(example)}")
	elif task == "learn" or task.startswith("learn:"):
		try:
			learner.learn(training_set, testing_set)
		except KeyboardInterrupt:
			print("\nTraining aborted by user.")
			answer = ""
			while answer.lower() not in ("y","n","yes","no"):
				answer = input("Save trained perceptron? (Y/N) ")
			if answer.lower() in ("n", "no"):
				return
	else:
		raise Exception("Valid tasks:\tlearn, classify")


	with open(target_state, "wb") as f:
		pickle.dump(learner._perceptron, f)
		print(f"Perceptron with concept_mapping {learner._perceptron.concept_mapping} saved to {target_state}")


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[-1], sys.argv[2], *sys.argv[3:-1])
