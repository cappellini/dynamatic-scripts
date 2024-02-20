# Useful scripts

## Build dynamatic and legacy-dynamatic on the EDA2 machine

```sh
bash fetch.sh
```

## Rebuilt dynamatic

```sh
cd dynamatic/
bash ../mybuild.sh
``` 

## Run your first example 

```sh
dynamatic/bin/dynamatic --run=run.sh
```

## change the benchmark

In the file `run.sh`, change the `share_test_1/share_test_1.c` that you need

```sh 
set-src             ./dynamatic/integration-test/share_test_1/share_test_1.c
```

In the `./dynamatic/integration-test/`, add your new benchmark
