Title: Grouping VA albums in mpd
Date: 2014-12-25 12:40
Tags: MPD, linux, tagging
Category: computer
Slug: mpd
Author: Rasi
Summary: the key is proper tagging...

## The issue

Every once in a while some user joins #mpd and asks how albums with
several artists can be grouped together instead of displaying each artist
individually in library.
And while I agree that this is annoying, their assumptions are wrong.
They assume this is a player issue, while in reality it's caused by missing
tags in the music files.

![Messed up Compilation album](/images/missing_tags1.jpg)

## Say hello to the albumartist tag

The solution is in fact relatively simple. The artist tag that everyone knows
just represents the artist for the current title.
There is another artist tag, called "albumartist", which represents the artist
of the album.

## Wrong usage of albumartist - a common problem

Many users know the albumartist tag, but only tag their Multi-artist albums
accordingly. This is wrong, because for this to work, the music player has to
make exceptions what to do with files that don't have an albumartist tag.

You see: EVERY album has a global artist. It just happens to be the same artist
for all tracks on regular albums. It's still a album-related artist.

Long story short: Every album needs an albumartist tag. For regular albums
the albumartist tag is the same as the artist tag.
For multi-artist releases it can be something like "Various Artists" or "Soundtrack"

## I have thousands of albums, how to sort this mess?

Don't worry, the process of fixing your files is a short one. It's a 2 step
process.

### 1. Fixing of your multi-artist releases.

First step is to get a tagger, for this example I use the excellent picard tagger.
Install it from your repository.
Now load all your multi-artist albums into it, by simply dragging the folders
on picards window.

When all files were properly added, select them all and watch the lower part
of picards window.
As you can see my files already have the albumartist tag. If you have such a line
too, simply click in the right column and give it a name (e.g. Various Artists)

![Adding albumartist tag in picard](/images/picard.jpg)

If no "Album Artist" line is visible right click and chose "Add New Tag"
type "albumartist" and fill the value as above.

Now make sure that "Move Files" and "Rename Files" is disabled in the Options
menu on top.

Finally hit save. You have successfully fixed your Multi-Artist albums.

### 2. Fix your regular albums

But remember, all albums need an albumartist tag. Luckily ncmpcpp has a little
tool to fix this automatically for you, but we need to build it.

Open a terminal.
Create an empty directory and cd into it.
run these commands:

    wget http://repo.or.cz/w/ncmpcpp.git/blob_plain/HEAD:/extras/Makefile
    wget http://repo.or.cz/w/ncmpcpp.git/blob_plain/HEAD:/extras/artist_to_albumartist.cpp
    make

This will build a little programm, called artist_to_albumartist, that you can find
in the same directory now. To use it simply run this command:

    find /PATH/TO/YOUR/MUSIC \( -name "*.flac" -o -name "*.mp3" -o -name "*.ogg" \) -exec ./artist_to_albumartist {} \;

Replace /PATH/TO/YOUR/MUSIC with your actual music root.
This will copy the artist tag of all files to the albumartist tag, skipping those files
that already have one (aka the multi-artist releases we fixed earlier)

Finally to make ncmpcpp use this new tag add this to your ~/.ncmpcpp/config file:

    media_library_primary_tag = "album_artist"

## Result

See the same track from first image properly grouped under its album:

![Fixed Compilation album](/images/fixed_tags.jpg)
