#!/bin/bash

querynum=10000
rangeEnd=$(($querynum/1000))

for num in 1 2 3 4 5 6 7 8 9 10
do
 # echo $num
 # echo $rangeEnd
  python3 mlas_auto.py $num &
done
wait

python3 excelconcat.py

echo All done
