#!/bin/bash

querynum=10000
rangeEnd=$(($querynum/1000))

for num in $(seq 1 $rangeEnd)
do
 # echo $num
 # echo $rangeEnd
  sudo python3 mlas_auto.py $num & disown;
done

wait

sudo python3 mlas_auto.py 11

echo All done
