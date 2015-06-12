Pulla
=========

[![PyPI Version](https://img.shields.io/pypi/v/pulla.svg)](https://pypi.python.org/pypi/pulla) [![PyPI Downloads](https://img.shields.io/pypi/dm/pulla.svg)](https://pypi.python.org/pypi/pulla) [![PyPI License](https://img.shields.io/pypi/l/pulla.svg)](https://pypi.python.org/pypi/pulla) [![GitHub tag](https://img.shields.io/github/tag/shubhamchaudhary/pulla.svg)](https://github.com/shubhamchaudhary/pulla/releases) [![GitHub release](https://img.shields.io/github/release/shubhamchaudhary/pulla.svg)](https://github.com/shubhamchaudhary/pulla/releases/latest)

[![Build Status Travis-CI](https://travis-ci.org/shubhamchaudhary/pulla.svg)](https://travis-ci.org/shubhamchaudhary/pulla) [![Coverage Status](https://coveralls.io/repos/shubhamchaudhary/pulla/badge.svg)](https://coveralls.io/r/shubhamchaudhary/pulla) [![Build Status Snap-CI](https://snap-ci.com/shubhamchaudhary/pulla/branch/develop/build_image)](https://snap-ci.com/shubhamchaudhary/pulla/branch/develop) [![Requirements Status](https://requires.io/github/shubhamchaudhary/pulla/requirements.svg)](https://requires.io/github/shubhamchaudhary/pulla/requirements/)

[![GitHub issues](https://img.shields.io/github/issues/shubhamchaudhary/pulla.svg?style=plastic)](https://github.com/shubhamchaudhary/pulla/issues) [![Stories in Ready](https://badge.waffle.io/shubhamchaudhary/pulla.png?label=ready&title=Ready)](https://waffle.io/shubhamchaudhary/pulla) [![Stories in Progress](https://badge.waffle.io/shubhamchaudhary/pulla.png?label=in progress&title=In Progress)](https://waffle.io/shubhamchaudhary/pulla)


Are you tired of doing `git pull` into all your git folders to keep them updated.  

With Pulla we present a solution to you:  

Pulla lets you pull code into all subfolder containing git projects.  

#### Usage

```sh
code $  ls
vdm                   wordpowermadeeasy

code $  pulla
wordpowermadeeasy:  Success
vdm:                Success

code $  pulla --verbose
Directory is:  ~/code/
----------------------
vdm : git pull --verbose
----------------------
remote: Counting objects: 69, done.
remote: Compressing objects: 100% (58/58), done.
remote: Total 69 (delta 40), reused 0 (delta 0)
Unpacking objects: 100% (69/69), done.
From bitbucket.org:varunest/vdm
   88fc178..371f66f  master     -> origin/master
Updating 88fc178..371f66f
Fast-forward
 app/src/main/AndroidManifest.xml                                            |   8 +-
 app/src/main/java/com/example/videodownloadmanager/MainActivity.java        |  38 ++--
 app/src/main/java/com/example/videodownloadmanager/PlaceholderFragment.java |  15 +-
 app/src/main/res/drawable/action_bar_icon.png                               | Bin
 app/src/main/res/menu/main.xml                                              |  14 +-
 app/src/main/res/values/styles.xml                                          |   5 +-
 6 files changed, 87 insertions(+), 22 deletions(-)
 create mode 100644 app/src/main/java/com/example/videodownloadmanager/Constants.java
 mode change 100644 => 100755 app/src/main/res/drawable/action_bar_icon.png
----------------------
wordpowermadeeasy : git pull --verbose
----------------------
remote: Counting objects: 47, done.
remote: Compressing objects: 100% (31/31), done.
remote: Total 47 (delta 12), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (47/47), done.
From github.com:shubhamchaudhary/wordpowermadeeasy
 = [up to date]      master     -> origin/master
 = [up to date]      fullscreen -> origin/fullscreen
 * [new branch]      wordnik    -> origin/wordnik
Already up-to-date.
----------------------

code $ pulla -h
```

#### Installation
Pulla is available from PyPi

```
# pip install pulla
```


#### Contributors
Checkout CONTRIBUTION.md file


[![wercker status](https://app.wercker.com/status/d8901c704b2e7befa14998731113e38f/m "wercker status")](https://app.wercker.com/project/bykey/d8901c704b2e7befa14998731113e38f)
