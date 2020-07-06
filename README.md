# PyURL [![CircleCI](https://circleci.com/gh/ydcjeff/pyurl.svg?style=svg)](https://app.circleci.com/pipelines/github/ydcjeff/pyurl)

PyURL is the CS50x 2020 Final Project. What it does is to let you check if your favourite websites have released/updated new blogs, articles, posts, announcements or releases.

Here's all what you can do:

- You can add the url or urls of the websites with `-a [URL(s)]`
- You can check updates about all the added websites with `-s all` or specific website with `-s [URL(s)]`
- You can open them at once with `-o`
- You can list out the updates you haven't opened yet with `-nv` and open them at once with `-o` if you want
- You can also remove the url(s) you wish to remove with `-rm [URL(s)]`
- You can print out the added urls with `-l`

## Sample

Adding:

```
pyurl -a https://pytorch.org/blog,https://blog.tensorflow.org
```

Syncing:

```
pyurl -s all -o # or
pyurl -s all # or
pyurl -s https://pytorch.org/blog,https://blog.tensorflow.org
```

Viewing the updates that haven't opened:

```
pyurl -nv # or
pyurl -nv -o # to open at once
```

Removing:

```
pyurl -rm https://pytorch.org/blog,https://blog.tensorflow.org
```

## Requirements

- Python 3.6 or greater
- pip 3
- requests
- Beautiful Soup 4
- SQLite 3
- lxml

## Installation

```
pip install pyurl
```

## Usage

You can now use `pyurl`.

```
usage: pyurl <commands> [URL(s)]

Get notified about new blogs, updates of your favourite webistes and visit
them at once

Commands:
  -a ADD, --add ADD     Add the website url
  -s SYNC, --sync SYNC  Check the added websites update status
  -rm REMOVE, --remove REMOVE
                        Remove the added URL(s)
  -l, --log             Output the urls of the added websites
  -o, --open            Open the new found website links
  -nv, --no-view        Output the un-opened links

Options:
  -V, --version         Output version number
  -h, --help            Output usage information
```

## LICENSE

MIT
