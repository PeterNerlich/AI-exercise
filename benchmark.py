#!/usr/bin/env python3

import sys
import pickle

from basics import Perceptron
from learner import Learner


def main(state, *files):
	if state.startswith("-"):
		#state = MulticlassPerceptron(int(saved_state[1:]))
		state = Perceptron(int(state[1:]))
	else:
		with open(state, "rb") as f:
			state = pickle.load(f)

	learner = Learner(None, perceptron=state)
	testing_set = set()

	for file in files:
		with open(file, "rb") as f:
			addition = pickle.load(f)
			assert type(addition) is dict
			assert type(addition["training"]) is set
			assert type(addition["testing"]) is set
			#training_set.update(addition["training"])
			testing_set.update(addition["testing"])

	total = 0
	passed = 0
	failed = 0

	for example in list(testing_set):
		result = learner.classify(example)
		total += 1
		if round(result) == learner._perceptron.get_mapped_value(example._concept):
			passed += 1
		else:
			failed += 1
		print(f"{failed} failed, {passed} passed (out of {total})\t{example._concept}:\t{result}")

	print("\n------\n")
	print(f"Ran {total} tests, {failed} failed ({percent(failed/total)}) and {passed} classified correctly ({percent(passed/total)}).")


def percent(x):
	return f"{round(x*100, 2)}%"


if __name__ == '__main__':
	main(sys.argv[1], *sys.argv[2:])
