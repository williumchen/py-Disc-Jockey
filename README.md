# py-Disc-Jockey
*Abbreviated as py-DJ.*

py-DJ is a free domain-specific language for quickly editting audio files in a way that is intuitive and easy to learn, with the eventual goal of making audio-mixing more user friendly. py-DJ is a command-line interface that is entirely text-based. py-DJ offers support for basic features (volume adjustment, pitch adjustment, and concatenation of files), and will be later expanded to be more feature-rich. 

## Dependencies
* Python 2.7.x
* pip

### Python
Use of py-DJ relies on [Python 2.7.x](https://www.python.org/downloads/). 

### pip
py-DJ uses several external libraries. In order to use these libraries, [pip](https://pypi.python.org/pypi/pip) must be installed. pip is a Python package manager that is used by `installation.sh`, a shell script to ensure all proper dependencies are installed.

## Installing py-DJ
1. Clone the repository using ``` git ```:

  ``` git clone https://github.com/williumchen/py-disc-jockey.git ```
2. In the source directory, run `installation.sh` (may require sudo):

  ``` bash installation.sh ```
3. In the source directory, run the REPL file ``` repl.py ```:

  ``` python repl.py ```
  
## Usage
All currently implemented features can be summarized by using ``` help ``` or ``` ? ``` in the REPL interface. Further details of each features are found by typing ``` help [feature] ```.
