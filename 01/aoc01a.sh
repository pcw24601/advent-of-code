#!/bin/bash

tens=$(sed -nr 's/^[^0-9]*([0-9]).*/+\1/p' input.txt)
units=$(sed -nr 's/^.*([0-9])[^0-9]*$/+\1/p' input.txt)
echo $((10*$(($tens))+$(($units))))