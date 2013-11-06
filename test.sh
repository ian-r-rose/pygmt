#!/bin/bash

cd tests
for test in `ls *.py`
do
    echo "Running test $test"
    python $test &> $test.tmp || { echo "Test $test failed"; exit 1; }
    rm $test.tmp
done
cd ..


