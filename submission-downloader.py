import argparse
import os
import requests
import sys
import time


class SubmissionDownloader:
    SUBMISSION_LIST = "https://dmoj.ca/api/user/submissions/{username}"
    SUBMISSION_SOURCE = "https://dmoj.ca/src/{submission_id}/raw"
    RATE_LIMIT = 1 # can be safely changed to 0.6
    # taken from https://dmoj.ca/about/codes/
    DOWNLOAD_ORDER = ["AC", "WA", "IR", "RTE", "OLE", "MLE", "TLE", "IE"]

    def __init__(self, username, best, overwrite, fast, headers):
        self.username = username
        self.best = best
        self.overwrite = overwrite
        self.fast = fast
        self.headers = headers

    def request(): # requests
        pass

    def get_submission_ids(): # read submission ids from json
        pass

    def get_submission_sources(): # actually downloads submissions
        pass

    def download(): # ties everything together
        get_submission_ids()
        get_submission_sources()

def main():
    parser = argparse.ArgumentParser(description="Downloads online judge submissions from DMOJ.")
    parser.add_argument("username", help="Your username, can be retrived from your DMOJ profile", type=str)
    parser.add_argument("session_id", help="Your session ID, can be retrived from your browser's Developer tools", type=str)
    parser.add_argument("--best", "-b", default=False, action="store_true", help="Only download the best submission for each problem, recommended.")
    parser.add_argument("--overwrite", "-o", default=False, action="store_true", help="Overwrite existing downloaded submissions, recommended.")
    parser.add_argument("--fast", "-f", default=False, action="store_true", help="Ignore the DMOJ API ratelimit, not recommended.")
    arguments = parser.parse_args()
    username, best, overwrite, fast = arguments.username, arguments.best, arguments.overwrite, arguments.fast
    # have to have this to access user submissions
    headers = {
        "User-Agent": "submission-downloader.py",
        "session_id": arguments.session_id}
    SubmissionDownloader(username, best, overwrite, fast, headers).download()


if __name__ == "__main__":
    sys.exit(main())
