#!/usr/bin/env bash

#--------------------------------------------------------------------
#- this script sets up and build everything of legacy-dynamatic
#--------------------------------------------------------------------

# this script should be called from dynamatic's source directory
SCRIPT_CWD=$PWD

cd $SCRIPT_CWD

set -e

DYNAMATIC_ROOT=$SCRIPT_CWD/dynamatic

mkdir -p $DYNAMATIC_ROOT

git clone git@github.com:epfl-lap/dynamatic.git $DYNAMATIC_ROOT
#git clone git@github.com:Jiahui17/dynamatic-mlir.git $DYNAMATIC_ROOT
cd $DYNAMATIC_ROOT

bash $SCRIPT_CWD/mybuild.sh && echo "successfully built dynamatic"
