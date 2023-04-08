#!/bin/bash
#change the upper limit of the sequence with the actual number of frames of the video
#change the --input flag to the name of the video
for i in $(seq 0 47)
do
  echo "python3 optiflow.py --frame1 $i --frame2 $(($i+1)) --input video"
  python3 optiflow.py --frame1 $i --frame2 $(($i+1)) --input video
done
