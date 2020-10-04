# submission-downloader
submission-downloader downloads your submissions in bulk from the [DMOJ](https://dmoj.ca/) website and compatible forks. There are a variety of options you can use to select what programs you want to download. This complements [dmoj-submission-downloader](https://github.com/Ninjaclasher/dmoj-submission-downloader), which downloads all the submissions for a problem. [Here](https://github.com/ComputerGenius152/programming-solutions) is an example of submissions that have been downloaded.

## Getting Started

### Installing
This program can be installed in two different ways. You can clone the repository and run the code yourself with Python 3 (recommended) or download prebuilt binaries that will run without Python (convenient) from our releases page:

1. Install the prerequisites with ```$ pip3 install -r requirements.txt```. Next, download [submission-downloader.py](submission-downloader.py). Run the program with ```python3 submission-downloader.py```.

2. Go to the [releases page](https://github.com/ComputerGenius152/submission-downloader/releases) and download the prebuilt binary file for your operating system. You can run the program with ```./submission-downloader``` or ```submission-downloader.exe```.

### Usage

If you have downloaded the binaries, use ```./submission-downloader``` or ```submission-downloader.exe``` instead of ```python3 submission-downloader.py```.

```
$ python3 submission-downloader.py --help
usage: submission-downloader.py [-h] [--aconly] [--best] [--fast]
                                [--overwrite]
                                apitoken username

Downloads online judge submissions from DMOJ.

positional arguments:
  apitoken         Your API token, can be retrived from your DMOJ profile
  username         Your username, can be retrived from your DMOJ profile

optional arguments:
  -h, --help       show this help message and exit
  --aconly, -a     Only download submissions if they earn points, recommended
  --best, -b       Only download the best submission for each problem,
                   recommended
  --fast, -f       Ignore the DMOJ API ratelimit, not recommended
  --overwrite, -o  Overwrite existing downloaded submissions, recommended
  ```

## Contributing
PRs and forks are welcome. Please open an issue if you notice any bugs.

## Licence
This project is licensed under the GNU General Public License v3.0. For more information, refer to [LICENSE.md](LICENSE.md).
