# Useful Scripts for Working with Dynamatic on the EDA2 Machine

## Prerequisite: get your Gurobi license

You need to download [gurobi optimizer for x64
Linux](https://www.gurobi.com/downloads/gurobi-software/).

Gurobi offers free [academic
license](https://www.gurobi.com/academia/academic-program-and-licenses/).

After getting the license, go to the EDA2 machine:

```sh
/opt/gurobi1000/linux64/bin/grbgetkey xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx # format of your key
```

Which stores the license file at `~/gurobi.lic` (this is one of the default
location for Gurobi to check if you have a valid license).

Remember to put the following lines in your `~/.bashrc` or `~/.zshrc`.
Dynamatic's cmake settings will use these environment variables to determine
how to include the headers of Gurobi.

```sh
export GUROBI_HOME="/opt/gurobi1003/linux64"
export PATH="${PATH}:${GUROBI_HOME}/bin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$GUROBI_HOME/lib"
```

## Build dynamatic on the EDA2 machine

```sh
bash fetch.sh
```

## Build dynamatic

```sh
cd dynamatic/
bash ../mybuild.sh
``` 

## Run your first example 

```sh
dynamatic/bin/dynamatic --run=run.sh
```

## Change/add the benchmark

In the file `run.sh`, change the `fir/fir.c` to what you need

```sh 
set-src ./dynamatic/integration-test/fir/fir.c
```

In the `./dynamatic/integration-test/`, add your new benchmark
