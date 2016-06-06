# Stasipy

A static site generator written in python.

## Purpose

This was mostly just done as a fun side project. I've always wanted to write a static site generator (text parsing is fun!), so here it is! It's not as full featured as I'd like it to be, and I suspect I'll hack on it for a long time as I need more and more features.


## Should I use this?

Probably not.

There are plenty to choose from that will be more actively maintained and more feature rich. This is mostly for my own use. However, if you want to, go for it!


## Usage

To use from source:

1. Clone from github.
2. Create Virtual Environment.
3. Activate that Environment.
4. Install Requirements.

```
$ git clone https://github.com/blakfeld/stasipy
$ cd stasipy
$ virtualenv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

To install via setup.py:

1. Clone from github
2. Run `setup.py install`

```
$ git clone https://github.com/blakfeld/stasipy
$ python setup.py install
```

To initialize a new site:

```
$ stasipy init ~/path/to/site --name "My Totes Rad Site"
```

To generate your new content:

```
$ stasipy generate ~/path/to/site
```

## To Do

[] Pagination.
[] Generate post summaries.
[] In general the way post content is templated/rendered needs some tweaking.
[] Add github styled code highlighting.
