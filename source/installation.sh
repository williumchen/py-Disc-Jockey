#!/bin/bash

echo "Installing necessary packages"
# Install homebrew to install 
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install portaudio
pip install pyparsing
pip install pydub
pip install pyaudio
exit
