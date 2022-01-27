import papermill as pm
import glob
import re
import argparse
import os
from multiprocessing import Pool
from functools import partial


def run_single_test(stage, input_path):
    output_path_prefix = os.environ.get("GITHUB_WORKSPACE", ".")

    try:
        output_path_filename = re.sub(
            "^(.*)\.ipynb$", r"\1-output.ipynb", input_path)
        output_path = f"{output_path_prefix}/{output_path_filename}"
        pm.execute_notebook(
            input_path=input_path,
            output_path=output_path,
            parameters={"stage": stage},
            progress_bar=False,
        )
        return (input_path, None)
    except pm.exceptions.PapermillExecutionError as e:
        return (input_path, e)


def main():

    parser = argparse.ArgumentParser(
        description="Execute the test Jupyter Notebooks.")
    parser.add_argument("--stage", required=True,
                        help="stage to execute against")
    args = parser.parse_args()

    stage = args.stage

    # Pull Requests should be tested against the dit env
    if re.fullmatch(r"refs/pull/\d+/merge", stage):
        stage = "dit"

    run_single_test_with_stage = partial(run_single_test, stage)
    with Pool(10) as p:
        results = p.map(run_single_test_with_stage, [nbf for nbf in glob.glob("*.ipynb")
                            if not nbf.endswith("-output.ipynb")])

    failure_results = [r for r in results if r[1] != None]

    if not results:
        print("No test notebooks were run")
        exit(1)
    if failure_results:
        print("Failure!")
        for r in failure_results:
            print(f"Failed: {r[0]} => {r[1]}")
        exit(1)
    else:
        print(
            f"Success! Ran {len(results)} test notebooks: {[r[0] for r in results]}")
        exit(0)


if __name__ == "__main__":
    main()
