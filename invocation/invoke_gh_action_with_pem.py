import jwt
import time
import requests
import argparse


def main():

    parser = argparse.ArgumentParser(
        description="Invoke a workflow_dispatch GitHub Action.")

    parser.add_argument("--issuer", dest="issuer", type=str, required=True,
                        help="The GitHub App's identifier, used for the JWT issuer field"
                        )  # 153910

    parser.add_argument("--installation_id", dest="installation_id", type=str, required=True,
                        help="The GitHub App's installation id for the target repo"
                        )  # 20905774

    parser.add_argument("--branch", dest="branch", type=str, required=True,
                        help="The branch/stage on which the tests are being invoked"
                        )  # main

    parser.add_argument("--pem", dest="private_key", type=str, required=True,
                        help="The contents of the private key in PEM format"
                        )  # copied from the PEM file

    parser.add_argument("--repo", dest="gh_repo", type=str, required=True,
                        help="The GitHub repo to invoke the workflow dispatch on"
                        )  # MAAP-Project/maap-data-system-tests

    parser.add_argument("--workflow", dest="workflow", type=str, required=True,
                        help="The workflow to dispatch"
                        )  # test.yml

    args = parser.parse_args()

    # Generate a JWT from the PEM
    now = time.time()
    jwt_token = jwt.encode(
        {
            "iat": int(now - 60),
            "exp": int(now + (10 * 60)),
            "iss": args.issuer
        },
        args.private_key,
        algorithm="RS256"
    )

    s = requests.Session()
    s.headers.update({"Accept": "application/vnd.github.v3+json"})
    res = s.post(
        f"https://api.github.com/app/installations/{args.installation_id}/access_tokens",
        headers={"Authorization": f"Bearer {jwt_token}"}
    )

    if res.status_code != 201:
        print(
            f"Error: access token retrieval status code was {res.status_code}")
        exit(1)

    gh_api_token = res.json()["token"]

    res = s.post(
        f"https://api.github.com/repos/{args.gh_repo}/actions/workflows/{args.workflow}/dispatches",
        headers={"Authorization": f"Bearer {gh_api_token}"},
        json={"ref": args.branch}
    )

    if res.status_code != 204:
        print(
            f"Error: workflow dispatch request got status code {res.status_code}")
        exit(1)


if __name__ == '__main__':
    main()
