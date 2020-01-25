#!/bin/bash

for i in {0..23..1}
do
	cd ./run$i
	mkdir output
	mkdir microutput
	cd ../
done
