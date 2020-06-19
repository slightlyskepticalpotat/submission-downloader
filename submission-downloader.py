import argparse
import os
import requests
import shutil
import sys
import time


class SubmissionDownloader:
    SUBMISSION_LIST = "https://dmoj.ca/api/v2/submissions"
    SUBMISSION_SOURCE = "https://dmoj.ca/src/{submission_id}/raw"
    RATE_LIMIT = 0.6
    DOWNLOAD_ORDER = {"AC": 0, "WA": 1, "IR": 2, "RTE": 3, "OLE": 4, "MLE": 5, "TLE": 6, "CE": 7, "AB": 8, "IE": 9} # taken from https://dmoj.ca/about/codes/
    FILE_EXTENSIONS = {"ADA": "ada", "AWK": "awk", "BF": "bf", "C": "c", "C11": "c", "CBL": "cbl", "CCL": "ccl", "CLANG": "c", "CLANGX": "c", "COFFEE": "coffee", "CPP03": "cpp", "CPP11": "cpp", "CPP14": "cpp", "CPP17": "cpp", "D": "d", "DART": "dart", "F95": "f95", "FORTH": "forth", "GAS32": "s", "GAS64": "s", "GASARM": "s", "GO": "go", "GROOVY": "groovy", "HASK": "hs", "ICK": "ick", "JAVA11": "java", "JAVA8": "java", "KOTLIN": "kt", "LUA": "lua", "MONOCS": "mono", "MONOFS": "mono", "MONOVB": "mono", "NASM": "asm", "NASM64": "asm", "NIM": "nim", "OBJC": "m", "OCAML": "ml", "OCTAVE": "m", "PAS": "pas", "PERL": "pl", "PHP": "php", "PIKE": "pike", "PRO": "pro", "PY2": "py", "PY3": "py", "PYPY": "py", "PYPY2": "py", "PYPY3": "py", "RKT": "rkt", "RUBY18": "rb", "RUBY2": "rb", "RUST": "rs", "SBCL": "lisp", "SCALA": "sc", "SCM": "scm", "SED": "sed", "SWIFT": "swift", "TCL": "tcl", "TEXT": "txt", "TUR": "t", "V8JS": "js", "VC": "c", "ZIG": "zig"} # languages allowed for helloworld

    def __init__(self, username, aconly, best, fast, overwrite, cookies):
        self.username = username
        self.aconly = aconly
        self.best = best
        self.fast = fast
        self.overwrite = overwrite
        self.cookies = cookies

    def request(self, url, params): # send a request to the dmojv2 api
        if self.fast == True:
            pass
        else:
            time.sleep(self.RATE_LIMIT)
        return requests.get(url, headers={"User-Agent": "submission-downloader.py"}, params=params, cookies=self.cookies)

    def get_submission_ids(self): # gets information about all submissions
        submission_ids = []
        total_pages = self.request(self.SUBMISSION_LIST, {"user": self.username}).json()["data"]["total_pages"]
        for i in range(1, total_pages + 1):
            data = self.request(self.SUBMISSION_LIST, {"user": self.username, "page": i}).json()["data"]["objects"]
            for thing in data:
                submission_ids.append([thing["problem"], thing["id"], thing["language"], thing["time"], thing["result"]])
        return submission_ids

    def get_submission_sources(self, submissions): # downloads submissions, filters out the best
        if self.overwrite == True:
            shutil.rmtree("downloaded-submissions")
            os.mkdir("downloaded-submissions")
            os.chdir("downloaded-submissions")
        else:
            try:
                os.mkdir("downloaded-submissions")
                os.chdir("downloaded-submissions")
            except:
                os.chdir("downloaded-submissions")
        if self.aconly == True:
            submissions = [thing for thing in submissions if thing[4] == "AC"]
        else:
            pass
        if self.best == True:
            submissions = sorted(submissions, key=lambda x: [self.DOWNLOAD_ORDER[x[4]], x[3]]) # sort by download order, then least time
            for thing in submissions:
                code = self.request(self.SUBMISSION_SOURCE.format(submission_id=thing[1]), {}).text
                filename = thing[0] + "." + self.FILE_EXTENSIONS[thing[2]]
                if os.path.exists(filename):
                    pass
                else:
                    open(filename, "w").write(code)
                    print("Downloading {filename}...".format(filename=filename))
        else:
            counter = 1
            for thing in submissions:
                code = self.request(self.SUBMISSION_SOURCE.format(submission_id=thing[1]), {}).text
                filename = thing[0] + "." + self.FILE_EXTENSIONS[thing[2]]
                if os.path.exists(filename):
                    filename = thing[0] + "-" + str(counter) + "." + self.FILE_EXTENSIONS[thing[2]]
                    counter+=1
                else:
                    counter = 1
                open(filename, "w").write(code)
                print("Downloading {filename}...".format(filename=filename))

    def download_submissions(self):
        print("Getting submission IDs...")
        submission_ids = self.get_submission_ids()
        self.get_submission_sources(submission_ids)
        print("All submissions downloaded.")


def main():
    parser = argparse.ArgumentParser(description="Downloads online judge submissions from DMOJ.")
    parser.add_argument("username", help="Your username, can be retrived from your DMOJ profile", type=str)
    parser.add_argument("session_id", help="Your session ID, can be retrived from your browser's Developer tools", type=str)
    parser.add_argument("--aconly", "-a", default=False, action="store_true", help="Only download submissions if they are correct, recommended.")
    parser.add_argument("--best", "-b", default=False, action="store_true", help="Only download the best submission for each problem, recommended.")
    parser.add_argument("--fast", "-f", default=False, action="store_true", help="Ignore the DMOJ API ratelimit, not recommended.")
    parser.add_argument("--overwrite", "-o", default=False, action="store_true", help="Overwrite existing downloaded submissions, recommended.")
    arguments = parser.parse_args()
    cookies = {"sessionid": arguments.session_id} # have to have this to access user submissions
    SubmissionDownloader(arguments.username, arguments.aconly, arguments.best, arguments.fast, arguments.overwrite, cookies).download_submissions()


if __name__ == "__main__":
    sys.exit(main())
