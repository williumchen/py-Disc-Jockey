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
py-DJ uses a REPL such that users can write programs simply passing input in line by line.

All currently implemented features can be summarized by using ``` help ``` or ``` ? ``` in the REPL interface, or by referring to the documentation below. Further details of each features are found by typing ``` help [feature] ```.

## Documentation
Load an audio file into the work-space with ` load <file name> `

Display the current audio file being edited with `edit`

* Optionally pass in a filename to switch the audio file being edited with `edit <file name>`

Play the current audio file with `play`

Display all files in the work-space in a well-formatted list with `files`

Export all edits to the current audio file to a file-name of your choice with `save <file name>`

Undo the most recent edit with `undo`

* Optionally pass in an integer to undo a specified number of edits with `undo <integer>`

Display the edit history of a song from most recent to oldest in a well-formatted list with `history`

* Optionally pass in an integer to truncate the list of edits to the specified number of most recent edits with `history <integer>`

Revert back to a specific state in `history` with `revert <integer>`

Increase or decrease the volume by a certain number of decibels with `<+,-> volume <integer>`

Increase or decrease the volume by a factor with `<*,/> volume <integer>`

Increase or decrease the pitch by a factor with `<*,/> pitch <integer>`

Concatenate two songs end to end and store in a new file with `<new-file> = <file1> append <file2>`

Overlay two songs and store in a new file with `<new-file> = <file1> + <file2>`

Reverse the currently edited song with `reverse`

Cut the currently song being edited at certain time intervals with `cut <x:yy> to <x:yy>` where `x` represents minutes and `yy` represents seconds.
