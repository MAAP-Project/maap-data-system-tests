from difflib import SequenceMatcher
import json
from typing import Union, Any, Tuple


def populate_maap_api_host(stage):
    if stage == "production":
        env_prefix = "ops."
    elif stage in ["main", "dit"]:
        env_prefix = ""
    else:
        env_prefix = f"{stage}."
    return f"api.{env_prefix}maap-project.org"


def fetch_results(maap, collection={}, query={}, timeout=180):
    """
    Function which utilizes the `executeQuery` function to return the results of queries.
    """
    return json.loads(maap.executeQuery(
        src=collection,
        query=query,
        poll_results=True,
        timeout=timeout
    ).text)


def try_test_actual(test, actual, expected: Union[str, int, Tuple[Any, Any]]):
    try:
        if isinstance(expected, str) or isinstance(expected, int):
            assert actual == expected
        elif isinstance(expected, Tuple):
            if expected[0]:
                assert actual >= expected[0]
            if expected[1]:
                assert actual <= expected[1]
    except Exception as e:
        print(
            f"{test}: {actual} does not match bounds {expected}")
        raise e


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
