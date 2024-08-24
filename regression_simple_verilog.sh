#!/bin/bash

# Choose the target clock period
clock_period=4

# Choose the target hdl to test (vhdl|verilog)
hdl="verilog"

dynamatic_dir=./dynamatic

cat filelist.lst | while read benchmark
do
  [ -f "$benchmark" ] || continue
  echo "[INFO] Launching Dynamatic on benchmark ${benchmark}..."
  rm -r "$(dirname ${benchmark})/out" 2> /dev/null
  echo "set-dynamatic-path $dynamatic_dir; \
    set-src ${benchmark}; \
    set-clock-period ${clock_period}; \
    compile --simple-buffers; \
    write-hdl --hdl ${hdl}; \
    simulate; \
    # synthesize; \
    exit" 2>&1 | $dynamatic_dir/bin/dynamatic --exit-on-failure --debug
done | tee regression_test_${clock_period}_${hdl}_simple.log
