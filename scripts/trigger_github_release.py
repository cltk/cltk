"""To be run on Travis CI after successful push to PyPI."""

import argparse
import json
import sys
from datetime import datetime

import pkg_resources
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="GitHub Auth token", type=str)
    args = parser.parse_args()
    token = args.token
    cltk_version = pkg_resources.get_distribution("cltk").version  # str
    # https://docs.github.com/en/rest/reference/repos#create-a-release
    data = {
        "tag_name": f"{cltk_version}",
        "target_commitish": "master",
        "name": cltk_version,
        "body": f"CLTK release version {cltk_version} triggered on {datetime.utcnow().strftime('%d/%m/%Y at %H:%M:%S')}.",
        "draft": False,
        "prerelease": False,
    }
    res = requests.post(
        url="https://api.github.com/repos/cltk/cltk/releases",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        },
        data=json.dumps(data),
    )
    print("Status code:", res.status_code)
    print("Message", res.text)
    if not res.status_code == 201:
        sys.exit(1)


if __name__ == "__main__":
    main()
