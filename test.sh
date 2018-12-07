#!/bin/bash

sudo mkdir downloads

querynum=10000
rangeEnd=$(($querynum/1000))

for num in 1 2 3 4 5 6 7 8 9 10
do
 # echo $num
 # echo $rangeEnd
  sudo python3 mlas_auto.py $num &
done
wait

sudo rm -r downloads/*.csv

sudo python3 excelconcat.py

echo All done
