# submission-downloader
Submission Downloader downloads your submissions in bulk from [DMOJ](https://dmoj.ca/). You can tell it to download all your submissions, all the correct ones, or the best submission from each question. This complements [dmoj-submission-downloader](https://github.com/Ninjaclasher/dmoj-submission-downloader), which downloads all the submissions for a problem. Although the code shares some similiarities with it, it was not originally forked from that repository.

## Getting Started

### Installing
This program can be installed in two different ways. You can clone the repository and run the code yourself with Python 3 or download prebuilt binaries that will run without Python from our releases page:

1. Install the prerequisites with ```$ pip3 install -r requirements.txt```. Next, download [submission-downloader.py](submission-downloader.py). Run the program with ```python3 submission-downloader.py```.

2. Go to the [releases page](https://github.com/ComputerGenius152/submission-downloader/releases) and download the prebuilt binary file for your operating system. You can run the program with ```./submission-downloader``` or ```submission-downloader.exe```.

### Usage

If you have downloaded the binaries, use ```./submission-downloader``` or ```submission-downloader.exe``` instead of ```python3 submission-downloader.py```.

```
$ python3 submission-downloader.py --help
usage: submission-downloader.py [-h] [--aconly] [--best] [--fast]
                                [--overwrite]
                                username session_id

Downloads online judge submissions from DMOJ.

positional arguments:
  username         Your username, can be retrived from your DMOJ profile
  session_id       Your session ID, can be retrived from your browser's
                   Developer tools

optional arguments:
  -h, --help       show this help message and exit
  --aconly, -a     Only download submissions if they are correct, recommended.
  --best, -b       Only download the best submission for each problem,
                   recommended.
  --fast, -f       Ignore the DMOJ API ratelimit, not recommended.
  --overwrite, -o  Overwrite existing downloaded submissions, recommended.
  ```

## Todo
- Support for more online judges such as MCPT

## Contributing
PRs and forks are welcome. Open an issue if you notice any bugs.

## Licence
This project is licensed under the MIT license. For more information, refer to [LICENSE.md](LICENSE.md).
