#!/bin/bash


benchmark=gsum
echo "set-dynamatic-path ./dynamatic; \
  set-src ./dynamatic/integration-test/$benchmark/$benchmark.c; \
  compile --simple-buffers; \
  write-hdl; \
  exit" \
  | dynamatic/bin/dynamatic --exit-on-failure

benchmark=fir
echo "set-dynamatic-path ./dynamatic; \
  set-src ./dynamatic/integration-test/$benchmark/$benchmark.c; \
  compile --simple-buffers; \
  write-hdl; \
  exit" \
  | dynamatic/bin/dynamatic --exit-on-failure


