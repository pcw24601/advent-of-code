#!/bin/bash

echo "graph test {" > input.dot
cat input.txt | sed 's/:\ /\ -- {/g' | sed 's/$/}/g' >> input.dot
echo "}" >> input.dot
neato input.dot -Tpng -o graph.png
open graph.png
