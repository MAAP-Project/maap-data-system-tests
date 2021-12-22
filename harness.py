import papermill as pm
import glob
import re
import argparse
import os


def main():

    parser = argparse.ArgumentParser(
        description="Execute the test Jupyter Notebooks.")
    parser.add_argument("--stage", required=True,
                        help="stage to execute against")
    args = parser.parse_args()

    success_results = []
    failure_results = {}

    stage = args.stage

    # Pull Requests should be tested against the dit env
    if re.fullmatch(r"refs/pull/\d+/merge", stage):
        stage = "dit"

    output_path_prefix = os.environ.get("GITHUB_WORKSPACE", "")

    for filename in [f for f in glob.glob("./*.ipynb") if not f.endswith("-output.ipynb")]:
        try:
            output_filename = re.sub(
                " ^ (.*)\.ipynb$", r"\1-output.ipynb", filename)
            pm.execute_notebook(
                input_path=filename,
                output_path=f"{output_path_prefix}/{output_filename}",
                parameters={"stage": stage},
                progress_bar=False,

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


if __name__ == "__main__":
    main()
