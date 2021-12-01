import papermill as pm
import glob
import sys
import re


success_results = []
failure_results = {}

for filename in [f for f in glob.glob('./*.ipynb') if not f.endswith("-output.ipynb")]:
  try:
    pm.execute_notebook(
      filename,
      re.sub("^(.*)\.ipynb$", r"\1-output.ipynb", filename),
      parameters=dict(stage=sys.argv[1]),
      progress_bar=False
    )
    success_results.append(filename)
  except pm.exceptions.PapermillExecutionError as e:
    failure_results[filename] = e


if failure_results:
  print("Failures:")
  for (k, v) in failure_results.items():
    print(f"File {k} => {v}")
  exit(1)
else:
  exit(0)