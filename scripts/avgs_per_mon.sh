#!/bin/bash

input=$1
months=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12")

for m in "${months[@]}"
do
    total=$(grep ",$m," "$input" | wc -l)
    avgs=($(grep ",$m," "$input" | grep -E -o "[0-9]+\.[0-9]+"))

    sum=0

    for a in "${avgs[@]}"
    do
    sum=$(echo "$sum + $a" | bc -l) 
    done
    
    overall_avg=$(echo "scale=4; $sum / $total" | bc)
    echo "$m,$overall_avg"
done
