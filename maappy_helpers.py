import json

def fetch_results(maap, collection={}, query={}, timeout=180):
    """
    Function which utilizes the `executeQuery` function to return the results of queries.
    """
    # use the executeQuery() function to get a response object
    response = maap.executeQuery(
      # dictionary-like object specifying the dataset to query 
      src = collection,
      # dictionary-like object specifying the parameters for query
      query = query,
      # must be True to use the timeout parameter
      poll_results = True,
      # max waiting period for a response in seconds
      timeout = timeout
    )
    return json.loads(response.text)
