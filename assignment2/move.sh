#!/bin/bash

src=$1
dst=$2

if [ ! "$#" -eq 2 ]; then
  echo "usage: move <src> <dst>";
  exit 0
fi

if [ ! -d "${src}" ]; then
  echo "'${src}' is not a directory."
  exit 0
fi

if [ ! -d "${dst}" ]; then
  echo "'${dst}' is not a directory."
  exit 0
fi

mv $src/* $dst/.
