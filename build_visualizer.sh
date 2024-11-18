#!/usr/bin/env bash

#----------------------------------------------------------------------------
#- This script compiles the dynamatic visualizer
#----------------------------------------------------------------------------

# this script should be called from dynamatic's source directory
SCRIPT_CWD="$PWD"

[ -d "./polygeist" ] || { echo "this directory doesn\'t look like dynamatic!" && exit 1; }

# These paths are hardcoded! Sorry!
CMAKE=cmake
POLYGEIST_DIR_PREFIX="/opt/polygeist"
GODOT_PATH="/usr/local/bin/Godot_v4.2.1-stable_linux.x86_64"
GODOT_EXPORT_TEMPLATE_PATH="/opt/godot/export_templates"

LLVM_PREFIX="$POLYGEIST_DIR_PREFIX/llvm-project"

C_COMPILER="clang"
CXX_COMPILER="clang++"

CMAKE_FLAGS_SUPER="\
  -DCMAKE_C_COMPILER=$C_COMPILER \
  -DCMAKE_CXX_COMPILER=$CXX_COMPILER \
  -DLLVM_ENABLE_LLD=ON \
  "

cd "$SCRIPT_CWD/visual-dataflow"

[ -d "./godot-cpp" ] || { echo "this directory doesn\'t look like visual-dataflow!" && exit 1; }

cd "$SCRIPT_CWD/visual-dataflow" && mkdir -p build && cd build

$CMAKE -G Ninja .. \
  -DMLIR_DIR=$LLVM_PREFIX/build/lib/cmake/mlir \
  -DLLVM_DIR=$LLVM_PREFIX/build/lib/cmake/llvm \
  -DCLANG_DIR=$LLVM_PREFIX/build/lib/cmake/clang \
  -DLLVM_TARGETS_TO_BUILD="host" \
  -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  $CMAKE_FLAGS_SUPER

ninja

cd "$SCRIPT_CWD/visual-dataflow"

mkdir -p "$HOME/.local/share/godot"
ln -sf $GODOT_EXPORT_TEMPLATE_PATH "$HOME/.local/share/godot"

"$GODOT_PATH" --headless --export-debug "Linux/X11" visual-dataflow

cd "$SCRIPT_CWD"
ln -f --symbolic $SCRIPT_CWD/visual-dataflow/visual-dataflow ./bin/visual-dataflow
