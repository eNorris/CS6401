#!/usr/bin/env bash
MCTHREADS=8

usage () {
  echo "Usage: mcnprun.sh <filename> [threads]"
  exit
}

if [[ "$#" -eq 0 ]]; then
  usage
fi

if [[ "$#" -gt 1 ]]; then
  MCTHREADS=$2
fi

{ time mcnp5 inp="$1" out=oua.out run=runtpa.rtpe mesh=mesa.msh mctal=mctaa.mctal tasks "$MCTHREADS" ; }  2>&1 | tee ngen_mcnp.log

