#!/bin/bash

set -Eeuo pipefail
set -x # print each command before executing

papermill data-system-tests.ipynb data-system-tests-out.ipynb -p stage $1