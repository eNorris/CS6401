#!/usr/bin/env bash

usage () {
  echo "Usage: advrun.sh <filename>"
  exit
}

if [[ "$#" -eq 0 ]]; then
  usage
fi

if [[ "$#" -gt 1 ]]; then
  usage
fi

{ time advantg "$1" ; } 2>&1 | tee ngen_adv.log
