import argparse
import os
import requests
import shutil
import sys
import time
import urllib


class SubmissionDownloader:
    RATE_LIMIT = 0.67
    DOWNLOAD_ORDER = {"AC": 0, "_AC": 1, "TLE": 2, "MLE": 3, "OLE": 4, "IR": 5, "RTE": 6, "CE": 7, "IE": 8, "AB": 9, "WA": 10}  # from https://github.com/DMOJ/online-judge/blob/master/judge/models/submission.py#L34
    FILE_EXTENSIONS = {"ADA": "ada", "AWK": "awk", "BF": "bf", "C": "c", "C11": "c", "CBL": "cbl", "CCL": "ccl", "CLANG": "c", "CLANGX": "c", "COFFEE": "coffee", "CPP03": "cpp", "CPP11": "cpp", "CPP14": "cpp", "CPP17": "cpp", "D": "d", "DART": "dart", "F95": "f95", "FORTH": "forth", "GAS32": "s", "GAS64": "s", "GASARM": "s", "GO": "go", "GROOVY": "groovy", "HASK": "hs", "ICK": "ick", "JAVA15": "java", "JAVA11": "java", "JAVA8": "java", "KOTLIN": "kt", "LUA": "lua", "MONOCS": "mono", "MONOFS": "mono", "MONOVB": "mono", "NASM": "asm", "NASM64": "asm", "NIM": "nim", "OBJC": "m", "OCAML": "ml", "OCTAVE": "m", "PAS": "pas", "PCPP11": "cpp", "PCPP13": "cpp", "PERL": "pl", "PHP": "php", "PIKE": "pike", "PRO": "pro", "PY2": "py", "PY3": "py", "PYPY": "py", "PYPY2": "py", "PYPY3": "py", "RKT": "rkt", "RUBY18": "rb", "RUBY2": "rb", "RUST": "rs", "SBCL": "lisp", "SCALA": "sc", "SCM": "scm", "SED": "sed", "SWIFT": "swift", "TCL": "tcl", "TEXT": "txt", "TUR": "t", "V8JS": "js", "VC": "c", "ZIG": "zig"}  # languages allowed for helloworld

    def __init__(self, apitoken=None, username=None, judge=None, aconly=None, best=None, fast=None, overwrite=None):
        self.apitoken = apitoken
        self.username = username
        self.judge = judge
        self.aconly = aconly
        self.best = best
        self.fast = fast
        self.overwrite = overwrite

    def request(self, url, params):
        """
        Sends a request using the v2 API.
        """
        if self.fast:
            pass
        else:
            time.sleep(self.RATE_LIMIT)
        return requests.get(url, headers={"User-Agent": "submission-downloader.py", "Authorization": "Bearer {apitoken}".format(apitoken=self.apitoken)}, params=params)

    def get_submission_ids(self):
        """
        Gets information about submissions.
        """
        submission_ids = []
        total_pages = self.request(
            self.SUBMISSION_LIST, {"user": self.username}
        ).json()["data"]["total_pages"]
        for i in range(1, total_pages + 1):
            data = self.request(self.SUBMISSION_LIST, {"user": self.username, "page": i}).json()["data"]["objects"]
            for thing in data:
                submission_ids.append(
                    [thing["problem"], thing["id"], thing["language"], thing["time"], thing["result"]]
                )
        return submission_ids

    def get_submission_sources(self, submissions):
        """
        Downloads submissions and filters out the best.
        """
        # overwrite?
        if self.overwrite:
            try:
                shutil.rmtree(self.judge+"-"+"downloaded-submissions")
            except:
                pass
            os.mkdir(self.judge+"-"+"downloaded-submissions")
            os.chdir(self.judge+"-"+"downloaded-submissions")
        else:
            try:
                os.mkdir(self.judge+"-"+"downloaded-submissions")
            except:
                pass
            os.chdir(self.judge+"-"+"downloaded-submissions")
        if self.aconly:
            submissions = [thing for thing in submissions if thing[4] == "AC" or thing[4] == "_AC"]
        else:
            pass
        if self.best:
            submissions = sorted(submissions, key=lambda x: [self.DOWNLOAD_ORDER[x[4]], x[3]])  # sort by download order, then least time
            for thing in submissions:
                code = self.request(self.SUBMISSION_SOURCE.format(submission_id=thing[1]), {}).text
                try:
                    filename = thing[0] + "." + self.FILE_EXTENSIONS[thing[2]]
                except:
                    filename = thing[0] + "." + "txt"
                    print(f"Unknown file extension for problem {thing[0]}")
                if os.path.exists(filename):
                    pass
                else:
                    print("Downloading {filename}...".format(filename=filename))
                    open(filename, "wb").write(code.encode('utf8'))
        else:
            counter = 1
            for thing in submissions:
                code = self.request(self.SUBMISSION_SOURCE.format(submission_id=thing[1]), {}).text
                filename = thing[0] + "." + self.FILE_EXTENSIONS[thing[2]]
                if os.path.exists(filename):
                    filename = thing[0] + "-" + str(counter) + "." + self.FILE_EXTENSIONS[thing[2]]
                    counter += 1
                else:
                    counter = 1
                print("Downloading {filename}...".format(filename=filename))
                open(filename, "wb").write(code.encode('utf8'))

    def download_submissions(self):
        """
        Downloads all user submissions from the judge.
        """
        self.SUBMISSION_LIST = "https://" + self.judge + "/api/v2/submissions"
        self.SUBMISSION_SOURCE = "https://" + self.judge + "/src/{submission_id}/raw"
        print('Started fetching submissions from url {url}'.format(url=self.SUBMISSION_LIST))
        print("Getting submission IDs...")
        self.get_submission_sources(self.get_submission_ids())
        print("{submissions} submissions downloaded.".format(submissions=len(os.listdir())))

def main():
    parser = argparse.ArgumentParser(description="Downloads online judge submissions from DMOJ.")
    parser.add_argument("apitoken", help="Your API token, can be retrived from your DMOJ profile", type=str)
    parser.add_argument("username", help="Your username, can be retrived from your DMOJ profile", type=str)
    parser.add_argument("judge", help="URL for the judge you are trying to download from, must support the DMOJ v2 API (https://dmoj.ca/api/#v2)", type=str)
    parser.add_argument("--aconly", "-a", default=False, action="store_true", help="Only download submissions if they earn points, recommended")
    parser.add_argument("--best", "-b", default=False, action="store_true", help="Only download the best submission for each problem and programming language, recommended")
    parser.add_argument("--fast", "-f", default=False, action="store_true", help="Ignore the DMOJ API ratelimit, not recommended")
    parser.add_argument("--overwrite", "-o", default=False, action="store_true", help="Overwrite existing downloaded submissions, recommended")
    arguments = parser.parse_args()
    # custom url parsing for judge, always prefer netloc over path
    judge_url = urllib.parse.urlparse(arguments.judge)
    judge = judge_url.path
    if judge_url.netloc:
        judge = judge_url.netloc
    SubmissionDownloader(
        arguments.apitoken,
        arguments.username,
        judge,
        arguments.aconly,
        arguments.best,
        arguments.fast,
        arguments.overwrite
    ).download_submissions()

if __name__ == "__main__":
    sys.exit(main())
