# submission-downloader
submission-downloader downloads your submissions in bulk from the [DMOJ](https://dmoj.ca/) website and compatible forks. There are a variety of options you can use to select what programs you want to download. This complements [dmoj-submission-downloader](https://github.com/Ninjaclasher/dmoj-submission-downloader), which downloads all the submissions for a problem. [Here](https://github.com/ComputerGenius152/programming-solutions) is an example of submissions that have been downloaded.

## Getting Started

### Installing and Running
This program can be installed in two different ways. You can install it directly with pip (recommended), or clone the repository and run the code yourself. Either way, you will need Python 3.8 or higher to run the code.

#### With Pip
```
$ pip3 install submission_downloader
$ python3 -m submission_downloader
```

#### Manually
```
$ git clone https://github.com/ComputerGenius152/submission-downloader.git
$ cd submission-downloader
$ pip3 install -r requirements.txt
$ python3 submission_downloader.py
```

### Usage
```
usage: submission_downloader.py [-h] [--aconly] [--best] [--fast] [--overwrite] apitoken username judge

Downloads online judge submissions from DMOJ.

positional arguments:
  apitoken         Your API token, can be retrived from your DMOJ profile
  username         Your username, can be retrived from your DMOJ profile
  judge            URL for the judge you are trying to download from, must support the DMOJ v2 API (https://dmoj.ca/api/#v2)

optional arguments:
  -h, --help       show this help message and exit
  --aconly, -a     Only download submissions if they earn points, recommended
  --best, -b       Only download the best submission for each problem and programming language, recommended
  --fast, -f       Ignore the DMOJ API ratelimit, not recommended
  --overwrite, -o  Overwrite existing downloaded submissions, recommended
```

## Contributing
PRs and forks are welcome. Please open an issue if you notice any bugs.

## Licence
This project is licensed under the GNU General Public License v3.0. For more information, refer to [LICENSE.md](LICENSE.md).
