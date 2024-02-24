#!/usr/bin/env bash

#--------------------------------------------------------------------
#- this script clones and builds dynamatic in the official repo
#--------------------------------------------------------------------

SCRIPT_CWD=$PWD
cd $SCRIPT_CWD

set -e

DYNAMATIC_ROOT=$SCRIPT_CWD/dynamatic

mkdir -p $DYNAMATIC_ROOT

git clone git@github.com:epfl-lap/dynamatic.git $DYNAMATIC_ROOT

cd $DYNAMATIC_ROOT

bash $SCRIPT_CWD/mybuild.sh && echo "successfully built dynamatic"
