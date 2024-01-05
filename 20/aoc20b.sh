#!/bin/bash

echo "Starting"
basename="input"
# basename="test"


echo "digraph test {" > ${basename}.dot
# Label node types
cat ${basename}.txt | sed -E -n 's/%([a-z]+).*/\t\1 [label=\1_FF];/p' >> ${basename}.dot
cat ${basename}.txt | sed -E -n 's/&([a-z]+).*/\t\1 [label=\1_inv];/p' >> ${basename}.dot
# Strip symbols from ids and indent
cat ${basename}.txt | sed -e 's/^/\t/; s/%//; s/&//' >> ${basename}.dot
# cat ${basename}.txt | sed 's/:\ /\ -- {/g' | sed 's/$/}/g' >> ${basename}.dot
echo "}" >> ${basename}.dot
dot ${basename}.dot -Tpng -o ${basename}.png
open ${basename}.png
echo "Done"