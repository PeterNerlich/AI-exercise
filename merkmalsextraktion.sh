#!/bin/sh

./merkmalsextraktion.py ../../../../studymat/I/Ringwelski/Verkehrszeichen/206\ -\ Stop/*/*/*.bmp Stop Stop.vectors 
./merkmalsextraktion.py ../../../../studymat/I/Ringwelski/Verkehrszeichen/205\ -\ Vorfahrt\ gewähren/*/*/*.bmp GiveWay GiveWay.vectors
./merkmalsextraktion.py ../../../../studymat/I/Ringwelski/Verkehrszeichen/102\ -\ Vorfahrt\ von\ rechts/*/*/*.bmp PriorityToTheRight PriorityToTheRight.vectors
./merkmalsextraktion.py ../../../../studymat/I/Ringwelski/Verkehrszeichen/306\ -\ Vorfahrtsstraße/*/*/*.bmp PriorityRoad PriorityRoad.vectors 
./merkmalsextraktion.py ../../../../studymat/I/Ringwelski/Verkehrszeichen/209\ -\ Fahrtrichtung\ links/*/*/*.bmp TurnLeft TurnLeft.vectors 
./merkmalsextraktion.py ../../../../studymat/I/Ringwelski/Verkehrszeichen/210\ -\ Fahrtrichtung\ rechts/*/*/*.bmp TurnRight TurnRight.vectors 
