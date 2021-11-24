#!/bin/bash

set -Eeuo pipefail
set -x # print each command before executing

papermill system-tests.ipynb system-tests-out.ipynb -p my_param 1 || true
papermill data-system-tests.ipynb data-system-tests-out.ipynb