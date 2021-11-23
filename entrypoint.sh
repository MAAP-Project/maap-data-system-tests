#!/bin/sh -l

set -Eeuo pipefail
set -x # print each command before executing

papermill system-tests.ipynb system-tests-out.ipynb -p my_param 2