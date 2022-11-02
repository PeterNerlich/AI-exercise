#!/usr/bin/env python3

import sys
import pickle
import math
from itertools import permutations

from basics import Concept, Perceptron, memoize, my_reduce
from learner import Learner


c_order = []
bits_required = int()
combinations = []
perceptrons = []
testing_set = set()


@memoize
def get_codings(concept):
	return tuple(my_reduce(lambda s,x,c,i: s+([f"{i:0{bits_required}b}"] if x == concept else []), c_order, []))

def perceptron_file(combination):
	combination = sorted(list(combination))
	return "_".join(combination)+".perceptron"

def load_perceptron(combination):
	try:
		with open(perceptron_file(combination), "rb") as f:
			state = pickle.load(f)
			assert type(state) is Perceptron
			return state
	except FileNotFoundError:
		print(f"Could not load perceptron: {perceptron_file(combination)}")
		exit(1)

def main(order, *files):
	if order == "ALL":
		order = [i.name for i in Concept]
		perms = tuple(permutations(order))
		for i,perm in enumerate(perms):
			perm = ",".join(perm)
			print(f"\n\n### PERMUTATION {i+1} of {len(perms)}:\t{perm}\n\n")
			main(perm, *files)
		return

	global c_order
	global bits_required
	global combinations
	global perceptrons
	global testing_set

	c_order = order.split(",")
	assert len(c_order) > 0
	bits_required = (len(c_order)-1).bit_length()
	unused_positions = (2**bits_required -1) - (len(c_order)-1)
	c_order.extend(["Unknown"] * unused_positions)

	# Find out combinations for every bit
	table = [["", *c_order, ""]]
	for bit in range(bits_required):
		combination = set()
		bits = []
		for i,concept in enumerate(c_order):
			if i & 2**bit:
				combination.add(concept)
				bits.append("1")
			else:
				bits.append("0")
		combinations.append(combination)
		table.append([f"2^{bit}", *bits, perceptron_file(combination)])
	column_sizes = list(map(lambda col: max(map(lambda cell: len(cell), col)), zip(*table)))

	print("Coding table (codes are written vertically, least significant bit starting):")
	for row in table:
		line = []
		for i,col in enumerate(row):
			if i == 0 or i == len(row)-1:
				line.append(f"{col:<{column_sizes[i]}}")
			else:
				line.append(f"{col:^{column_sizes[i]}}")
		print("  ".join(line))
	print()
	answer = "-"
	while answer.lower() not in ("","y","n","yes","no"):
		answer = input("Please ensure the perceptrons are trained and correctly named. Continue? (Y/n) ")
	if answer.lower() in ("n", "no"):
		return

	# Load perceptron for every combination
	perceptrons = list(map(load_perceptron, combinations))

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
		result = "".join(map(lambda x: str(round(x.run(example))), perceptrons))
		total += 1
		if result in get_codings(example._concept.name):
		#if result in get_codings(example._concept) or result in get_codings(example._concept.name):
			passed += 1
		else:
			failed += 1
		print(f"{failed} failed, {passed} passed (out of {total})\t{example._concept}\t{get_codings(example._concept.name)}:\t{result}")

	print("\n------\n")
	print(f"Ran {total} tests, {failed} failed ({percent(failed/total)}) and {passed} classified correctly ({percent(passed/total)}).")


def percent(x):
	return f"{round(x*100, 2)}%"


if __name__ == '__main__':
	main(sys.argv[1], *sys.argv[2:])
