#!/bin/bash

for i in {0..23..1}
do
	cd ./example_spheroid_TNF_conc0.1_pulse25-600/run$i
	mkdir output
	mkdir microutput
	cd ../
done
