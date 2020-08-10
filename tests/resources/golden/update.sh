#! /usr/bin/bash

scriptpath=$(readlink -f "$0")
scriptroot=$(dirname "$scriptpath")

echo "update golden master"

pushd $scriptroot

todo="--images! --figures!"

vimguide=$(python -c 'import power; print(power.DOCU13_PDF)')
rawmaker -i ${vimguide} -j8 --pages=1:4 ${todo} -o vim

# TODO COMPARE $0 with SUCCESS
echo "done"

popd
