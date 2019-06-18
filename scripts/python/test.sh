#!/bin/bash

KEY=data/julio-gpu.pem
FILE_CFG=$1

echo "Testing single core"
python3 run_test.py --key $KEY --max 0 $FILE_CFG > output

echo "Testing 2 cores with 1 thread"
python3 run_test.py --key $KEY --max 2 $FILE_CFG >> output
echo "Testing 2 cores with 2 threads"
python3 run_test.py --key $KEY --max 2 --slots 2 $FILE_CFG >> output

echo "Testing 4 cores with 1 thread"
python3 run_test.py --key $KEY --max 4 $FILE_CFG >> output
echo "Testing 4 cores with 2 threads"
python3 run_test.py --key $KEY --max 4 --slots 2 $FILE_CFG >> output
echo "Testing 4 cores with 4 threads"
python3 run_test.py --key $KEY --max 4 --slots 4 $FILE_CFG >> output

echo "Testing 8 cores with 1 thread"
python3 run_test.py --key $KEY --max 8 $FILE_CFG >> output
echo "Testing 8 cores with 2 threads"
python3 run_test.py --key $KEY --max 8 --slots 2 $FILE_CFG >> output
echo "Testing 8 cores with 4 threads"
python3 run_test.py --key $KEY --max 8 --slots 4 $FILE_CFG >> output
echo "Testing 8 cores with 8 threads"
python3 run_test.py --key $KEY --max 8 --slots 8 $FILE_CFG >> output
