#!/bin/sh

function learn {
	./learner.py -52 "learn:${1//_/,}" *.vectors "$1.perceptron"
}

function generate {
	echo "$1" >> ./results.txt

	echo "" | \
	./combined.py "$1" *.vectors | \
	tail -n 1 >> ./results.txt
}


learn PriorityToTheRight_Stop_TurnLeft_Unknown
learn GiveWay_PriorityToTheRight_TurnRight_Unknown
learn PriorityRoad_TurnLeft_TurnRight_Unknown
generate Unknown,Stop,GiveWay,PriorityToTheRight,PriorityRoad,TurnLeft,TurnRight

learn GiveWay_PriorityToTheRight_TurnLeft_Unknown
learn PriorityRoad_TurnLeft_Unknown
learn GiveWay_TurnRight_Unknown
generate Stop,GiveWay,PriorityToTheRight,PriorityRoad,TurnLeft,TurnRight,Unknown

learn PriorityToTheRight_TurnLeft_TurnRight_Unknown
learn GiveWay_PriorityRoad_PriorityToTheRight_Unknown
learn PriorityRoad_Stop_TurnRight_Unknown
generate Unknown,TurnLeft,GiveWay,PriorityToTheRight,Stop,TurnRight,PriorityRoad

learn GiveWay_Stop_Unknown
learn PriorityToTheRight_TurnLeft_Unknown
learn GiveWay_TurnLeft_TurnRight_Unknown
generate PriorityRoad,Stop,PriorityToTheRight,Unknown,TurnRight,GiveWay,TurnLeft

learn GiveWay_PriorityToTheRight_TurnLeft_Unknown
learn PriorityRoad_TurnLeft_Unknown
learn GiveWay_TurnRight_Unknown
generate Stop,PriorityToTheRight,PriorityRoad,TurnLeft,TurnRight,GiveWay,Unknown

