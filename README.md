# Functional Flow

## About

This project uses [Python3](https://www.python.org/)

## Getting Started In Simple 4 Steps (Mac OS)

1. Install [Python3](https://www.python.org/downloads/)
2. Clone your project

   ```
   git clone https://github.com/leogoesger/func-flow.git
   cd func-flow/
   ```

3. Installing virtualenv

   ```
   python3 -m pip install --user virtualenv
   ```

4. Create and activate virtualenv

   ```
   python3 -m virtualenv env;
   source env/bin/activate
   ```

5. Install dependencies

   ```
   pip install -r requirements.txt
   ```

## Run Script

1. In project directory, make two folders

   ```
   mkdir rawFiles processedFiles
   ```

2. Load raw files to rawFiles folder, and run script

   ```
   python main.py
   ```

## Error and Bug

Use [Trello](https://trello.com/funcflow) to keep upload error message, a screen shot, and raw data file used

## CI

It uses [Travis-CI](https://travis-ci.org/) and [Coveralls](https://coveralls.io/).

## Options

[iTerm](https://www.iterm2.com/): iTerm2 is a replacement for Terminal

## License

Copyright (c) 2018

Licensed under the [MIT license](LICENSE).
