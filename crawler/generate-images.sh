#!/bin/bash

for i in dot neato twopi circo fdp sfdp; do 
       echo "generating with $i"; 
       $i -Tpng result.dot -o result.$i.png; 
done