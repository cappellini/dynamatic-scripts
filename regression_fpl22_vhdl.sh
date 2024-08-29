#!/bin/bash

# Choose the target clock period
clock_period=4

# Choose the target hdl to test (vhdl|verilog)
hdl="vhdl"

dynamatic_dir=./dynamatic

cat filelist.lst | while read benchmark
do
  [ -f "$benchmark" ] || continue
  echo "[INFO] Launching Dynamatic on benchmark ${benchmark}..."
  rm -r "$(dirname ${benchmark})/out" 2> /dev/null
  echo "set-dynamatic-path $dynamatic_dir; \
    set-src ${benchmark}; \
    set-clock-period ${clock_period}; \
    compile; \
    write-hdl --hdl ${hdl}; \
    simulate; \
    # synthesize; \
    exit" | $dynamatic_dir/bin/dynamatic --exit-on-failure --debug
done 2>&1 | tee regression_test_${clock_period}_${hdl}_fpl22.log
