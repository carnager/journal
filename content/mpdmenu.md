Title: mpdMenu - mpd on stereoids
Date: 2014-03-29 14:20
Tags: MPD, linux, scripting
Category: computer
Slug: mpdMenu
Author: Rasi
Summary: mpd script that uses dmenu/rofi

# This article is obsolete.... read on [HERE](|filename|mppc-a-mpc-clone-in-python.md)

...

## Introduction

I am a fan of [dmenu]. I think it's incredibly useful and fast for a lot
of tasks.
Recently DaveDavenport forked simpleswitcher and renamed it to [rofi]. Why do I mention it?
Well he added a dmenu mode to it, which makes it 100% compatible with the latter. Nice!

It's also no secret that I am a MPD advocate. What it does it does perfectly -
the server/client design makes it's nothing but ideal for a home stereo system.

So I thought why not combine these 2 worlds and control MPD in the fastest way imaginable?
So I wrote mpdMenu - a dmenu based MPD client. Yes there are others out there already, but none
of these do, what mpdMenu does - trust me on that one.

## Features

So what makes it special?
The dmenu-based MPD clients you can find on the web normally do one thing: browse your Playlist (or maybe the database)
and select some songs/albums to play. That's cool, but I wanted more than that.

So mpdMenu has 4 modes to add, insert or replace music.

1. Artist - Browse Artists and add/play all their music
2. Albums - Chose any album and add/play it.
3. Track - Search for any track and add/play it.
4. Database Browser - Browse Database by Artist > Album > Track and add/play whatever you chose.

Believe me, espacally the 3rd part is a blessing. It never was that easy and that fast to play a specific song.
Don't believe me? Have a look yourself:

{% video ./images/mpd_track.mp4 800 450 https://pic.53280.de/mpd.png %}

It works around the same for the other modes too.

### Handling what's on your queue

Sometimes you want to hear more from the currently playing artist. That's why I added a submenu which does just this.
Selecting the "Current Artist" Option will present you a menu which will let you add tracks or albums by the Artist that
is currently playing.

Last but not least mpdMenu allows you to browse the current Queue and switch songs.

### Just play something!

But sometimes you simply don't know what you want to listen to.
For these ocasions I added 2 modes.

1. Random Album
2. Random Tracks

They do exactly what they say. For random tracks the script will ask you how many items you want to get added to your playlist.

### Options

The Options Menu presents you with most MPD options that can be switched on the fly.
This includes changing the volume, enabling modes (random, single, consume, repeat), changing replaygain,
enabling/disabling audio outputs and setting crossfading.

It also includes a submenu called lastfm, which allows to start and stop mpdscribble. It also can add/remove currently playing artists to
a blacklist so they will never be scrobbled. At the moment the lastfm functionality calls an external script, because the code for the blacklist
is relatively ugly :)

### Rating

My personal Highlight is the Rating Menu.
Here you can rate albums and tracks and search your database by rated tracks.

This is done in 2 different ways.
For tracks I use an external tagger (python-eyed3) to add a comment field to the files which includes the rating.
In theory I could have used the same way for albums too, but MPD cannot handle several comment fields, so I had to be clever.

So if you rate an album, mpdMenu will create a tiny text file inside of the album directory which includes Artist, Album and Rating.
When searching for album ratings bash's globbing is used to magically find the relevant information.

It works really well:

{% video ./images/mpd_rating.mp4 800 450 https://pic.53280.de/mpd.png %}

### Where to get it

You can find the little script in my [git repository]

[rofi]: https://github.com/DaveDavenport/rofi "rofi"
[dmenu]: https://bitbucket.org/melek/dmenu2 "dmenu"
[git repository]: https://git.53280.de/carnager/scripts/tree/mpdMenu "git repository"
