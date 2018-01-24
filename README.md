# Functional Flow

[![Build Status](https://travis-ci.org/leogoesger/func-flow.svg?branch=master)](https://travis-ci.org/leogoesger/func-flow)

## About

This project uses [Python3](https://www.python.org/)

## Getting Started in 4 simple steps (Mac OS)

1. Install [Python3](https://www.python.org/downloads/), [Git](https://git-scm.com/download/) and a [text editor](https://www.sublimetext.com/3) of your choice.
2. Clone your project in [Terminal](http://www.informit.com/blogs/blog.aspx?uk=The-10-Most-Important-Linux-Commands)

   ```
   git clone https://github.com/leogoesger/func-flow.git
   cd func-flow/
   ```

3. Create and activate virtualenv

   ```
   python3 -m venv my-virtualenv
   source my-virtualenv/bin/activate
   ```

4. Install dependencies

   ```
   pip install -r requirements.txt
   ```

## Getting Started in 5 steps (Windows)

1. Install [Python3](https://www.python.org/downloads/), [Git](https://git-scm.com/download/win) and a [text editor](https://www.sublimetext.com/3) of your choice.
2. Add Python to [System Path](https://www.pythoncentral.io/add-python-to-path-python-is-not-recognized-as-an-internal-or-external-command/)

   * Locate `Python3` from your local computer. Usually located in the following folder:

     ```
     C:\python3
     ```

     or

     ```
     C:\Users\your-name\AppData\Local\Programs\Python\Python36-32
     ```

   * Follow this [link](https://www.pythoncentral.io/add-python-to-path-python-is-not-recognized-as-an-internal-or-external-command/) from step 2 to the end.
   * Go into Command Prompt by typing `cmd` in search bar, and type `python`. You should see the following:

     ```
     Python 3.6.4 (v3.6.4:d48ecebad5, Dec 18 2017, 21:07:28)
     [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
     Type "help", "copyright", "credits" or "license" for more information.
     >>>
     ```

   * Type `exit()` to exit the python shell.

3. Clone your project in [Command Prompt](http://www.informit.com/blogs/blog.aspx?uk=The-10-Most-Important-Linux-Commands)

   ```
   git clone https://github.com/leogoesger/func-flow.git
   cd func-flow
   ```

4. Create and activate virtualenv

   ```
   python -m venv my-virtualenv
   my-virtualenv\Scripts\activate
   ```

5. Install dependencies

   ```
   pip install -r requirements.txt
   ```

## Run Script

1. In project directory

   ```
   python main.py
   ```

## Test

## Error and Bug

Use [Trello](https://trello.com/funcflow) to keep upload error message, a screen shot, and raw data file used

## Options

[iTerm](https://www.iterm2.com/): iTerm2 is a replacement for Terminal

```
find . -name '*.rdb' -exec sh -c 'mv "$0" "${0%.rdb}.csv"' {} \;

  pip freeze > requirements.txt
```

## License

Copyright (c) 2018

Licensed under the [MIT license](LICENSE).
