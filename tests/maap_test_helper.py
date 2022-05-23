from difflib import SequenceMatcher
import json
from typing import Union, Any, Tuple, Iterable


def populate_maap_api_host(stage):
    stage = stage if stage != "main" else "dit"
    if stage == "production":
        # env_prefix = "ops." after services are migrated, this should be ops
        env_prefix = "ops."
    else:
        env_prefix = f"{stage}."
    return f"api.{env_prefix}maap-project.org"

def populate_maap_host(stage, prefix):
    stage = stage if stage != "main" else "dit"
    if stage == "production":
        env_prefix = ""
    else:
        env_prefix = f"{stage}."
    return f"{prefix}.{env_prefix}maap-project.org"


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


def assert_results(test: str, actual: Iterable[Any], expected: Union[str, int, Tuple[Any, Any]]) -> None:
    try:
        if isinstance(expected, str) or isinstance(expected, int):
            assert len(actual) == expected
        elif isinstance(expected, Tuple):
            if expected[0]:
                assert len(actual) >= expected[0]
            if expected[1]:
                assert len(actual) <= expected[1]
    except Exception as e:
        print(
            f"{test}: {len(actual)} does not match bounds {expected}")
        raise e


def similar(a, b) -> float:
    return SequenceMatcher(None, a, b).ratio()
