#!/bin/bash

set -Eeuo pipefail
set -x # print each command before executing

python harness.py --stage $1