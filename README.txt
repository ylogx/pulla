Pulla [![Build Status](https://travis-ci.org/shubhamchaudhary/pulla.svg)](https://travis-ci.org/shubhamchaudhary/pulla)
=========

Are you tired of doing `git pull` into all your git folders to keep them updated.  

With Pulla we present a solution to you:  

Pulla lets you pull code into all subfolder containing git projects.  

#### Usage

```sh
code $  ls
vdm                   wordpowermadeeasy

code $  pulla
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
 app/src/main/assets/parser.js                                               | 898 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++--------------
 app/src/main/java/com/example/downloadhandlers/DownloadReciever.java        |   4 +-
 app/src/main/java/com/example/downloadhandlers/JsObject.java                |  18 +-
 app/src/main/java/com/example/downloadhandlers/MyWebViewClient.java         |  14 +-
 app/src/main/java/com/example/searchhandlers/AsyncGetSearchResults.java     |  34 +++-
 app/src/main/java/com/example/searchhandlers/CustomGridAdapter.java         |   4 +-
 app/src/main/java/com/example/videodownloadmanager/Constants.java           |  14 ++
 app/src/main/java/com/example/videodownloadmanager/MainActivity.java        |  38 ++--
 app/src/main/java/com/example/videodownloadmanager/PlaceholderFragment.java |  15 +-
 app/src/main/java/com/example/videodownloadmanager/SearchableActivity.java  |   6 +-
 app/src/main/res/anim/infinite_slide_in_left.xml                            |   1 -
 app/src/main/res/drawable/action_bar_icon.png                               | Bin
 app/src/main/res/layout/fragment_home.xml                                   |   8 +-
 app/src/main/res/menu/main.xml                                              |  14 +-
 app/src/main/res/menu/search_menu.xml                                       |   7 +-
 app/src/main/res/values-v11/styles.xml                                      |   3 +-
 app/src/main/res/values/styles.xml                                          |   5 +-
 18 files changed, 870 insertions(+), 221 deletions(-)
 mode change 100644 => 100755 app/src/main/assets/parser.js
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
# sudo pip3 install pulla
```
