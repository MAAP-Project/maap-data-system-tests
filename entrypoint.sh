#!/bin/bash

set -Eeuo pipefail
set -x # print each command before executing

cd tests
time python harness.py --stage $1
