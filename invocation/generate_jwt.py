import argparse
import time
import jwt


def main():

    parser = argparse.ArgumentParser(
        description="Invoke a workflow_dispatch GitHub Action.")

    parser.add_argument(
        "--pem", required=True, help="path to the PEM file")

    parser.add_argument(
        "--issuer", default="153910",
        help="The GitHub App's identifier, used for the JWT issuer field"
    )

    args = parser.parse_args()

    with open(args.pem) as f:
        private_key = f.read()

    now = time.time()
    jwt_token = jwt.encode(
        {
            "iat": int(now - 60),
            "exp": int(now + (10 * 60)),
            "iss": args.issuer
        },
        private_key,
        algorithm="RS256"
    )

    print(jwt_token)


if __name__ == '__main__':
    main()
