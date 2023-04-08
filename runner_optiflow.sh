#!/bin/bash

for i in $(seq 0 47)
do
  echo "python3 optiflow.py --frame1 $i --frame2 $(($i+1))"
  python3 optiflow.py --frame1 $i --frame2 $(($i+1))
done
