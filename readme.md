# Scripts for Working with Dynamatic on the ee-tik-dynamo-eda1 Machine

## Prerequisite: get your Gurobi license

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

## Clone and build dynamatic on the EDA2 machine

```sh
git clone git@github.com:EPFL-LAP/dynamatic.git
cd dynamatic/
bash ../mybuild.sh
``` 

## (Optional) Building the handshake visualizer

```sh
cd dynamatic/
git submodule init "visual-dataflow/godot-cpp"
bash "../build_visualizer.sh"
``` 

## Run your first example 

```sh
dynamatic/bin/dynamatic --run run.sh
```

## Change/add the benchmark

In the file `run.sh`, change the `fir/fir.c` to what you need

```sh 
set-src ./dynamatic/integration-test/fir/fir.c
```

In the `./dynamatic/integration-test/`, add your new benchmark

## Trouble-shooting

### Error when running simulation: 

```
dynamatic/include/dynamatic/Integration.h:214:34: error: no member named 'setfill' in namespace 'std'
  214 |   os << "0x" << std::hex << std::setfill('0') << std::setw(8)
```

Change `simulate.sh` as the following: 
```diff
+++ b/tools/dynamatic/scripts/simulate.sh
@@ -24,7 +24,7 @@ IO_GEN_BIN="$SIM_DIR/C_SRC/$KERNEL_NAME-io-gen"

 # Shortcuts
 HDL_DIR="$OUTPUT_DIR/hdl"
-CLANGXX_BIN="$DYNAMATIC_DIR/bin/clang++"
+CLANGXX_BIN="clang++"
 HLS_VERIFIER_BIN="$DYNAMATIC_DIR/bin/hls-verifier"
 RESOURCE_DIR="$DYNAMATIC_DIR/tools/hls-verifier/resources" 
```

### Error during visualization:

A pop-up window saying "Your video card drivers seems not to support the
required Vulkan version...".

Change one line in `$DYNAMATIC_DIR/tools/dynamatic/scripts/visualize.sh`:

```diff
# Launch the dataflow visualizer
echo_info "Launching visualizer..."
---"$VISUAL_DATAFLOW_BIN" "--dot=$F_DOT_POS" "--csv=$F_CSV" >/dev/null
+++"$VISUAL_DATAFLOW_BIN" "--dot=$F_DOT_POS" "--csv=$F_CSV" --rendering-driver opengl3 >/dev/null
exit_on_fail "Failed to run visualizer" "Visualizer closed" 
```
