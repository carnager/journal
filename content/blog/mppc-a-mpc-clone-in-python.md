Title: clerk - mpd client that needs typing
Date: 2014-08-09 10:36
Category: computer
Tags: mpd, programming, rofi
Authors: Rasi
Summary: clerk - mpd client on steroids

## History

Back in march I wrote about [mpdMenu](|filename|/blog/mpdmenu.md).
It basically used mpc and dmenu to create lists of albums/files that were displayed
in dmenu. It had some nice features like rating albums/tracks but to be honest it
seemed a little rough around the edges.

Those times are over now. mpdMenu is history. Long live clerk.
clerk is basically the same thing as mpdMenu was, but it's presented in a much
nicer way.
I cleaned up the whole menu structure and i think it looks rather nice now.
But let's see what clerk can actually do.

## Features

Let's first have a look at the main menu.

### The Main Menu

![Pelican](/images/clerk-main.jpg)

Nothing too exciting here. Play a random album, play random tracks.
The number of tracks can be configured in the options menu, which we will
look at later.

### Browsing

#### Current Artist

The next section covers actual browsing functionality. The current artist menu
allows you to browse all albums or tracks by the artist currently playing in mpd.

![Current Artist](/images/clerk-current-artist.jpg)

Do you see the section that says "Adding Mode: Add"?
Clicking this will change the Mode to either "Insert" or "Replace" so you can
decide how the actual album will be handled in the queue.

#### Current Queue

The Current Queue menu will show what it says: mpd's current queue.
It has 2 modes: Play and Delete. Play will simply change playback to the
chosen song, whereas Delete will remove items from the queue.

![Queue](/images/clerk-queue.jpg)

#### Manage Playlists

The Manage Playlists menu allows you to save, crop and clear the current
playlist - or load an already saved one. It will ask for a filename and
even warn you if the playlist already exists.

 ![Save Playlist](/images/clerk-playlist-save.jpg)

In addition to this, you will find options to load an RSS Feed
(those should be manually put in a file called podcasts in clerk's config directory)

There are also entries to suspend or resume the current queue.
This is very handy if you are listening to a podcast and want to continue later.
Just suspend the playlist, listen to whatever you want and later resume it.
It will load the state of the playlist and the position of the active track.

### Browsing the Database

Clerk offers several ways to browse the database.
First there is the hierarchical browser, which let's you first chose an artist
and displays all albums related to it. If you chose to browse even deeper
it will show all tracks of the given album.
At any point in the library it's possible to add/insert/replace every shown artist/album/track.

If you use rofi it is even possible to add several songs at once, by hitting Shift+Enter.

![Hierachical Browser](/images/clerk-browser1.jpg)

It's also possible to browse the Database by date, list all albums.
Last but not least clerk can show you all songs in database.
Each browser can add, insert or replace the results into the queue.

Speaking of insert mode. This is one thing that most mpd clients get wrong, imho.
You see, insert in mpd means, that the track will be placed right after the one
that is currently playing. Which works fine, as long as you are not in random mode.
For this scenario mpd offers a feature called "Priorities", which can set a weight
to songs in the playlist. Sounds like a good solution, but the developer of mpd only
made it available for random mode. In normal playback mode weights are ignored.

So there are some clients that support priorities. But they seperate it from the "Insert" command.
Which seems wrong to me, because all in all you always want the same thing, be it in random mode or not:
Play that goddamn song NEXT.

Well, this is exactly what clerk does. Insert will always play the selected songs next. No matter what
mode mpd is in. Nice.

### A word about mpc

For the tracks and album listings I really wanted to have a way to show a nice tag based view.
Which turned out to be not-easy at all.
Why is that?
Well there are actually 2 issues here, which both needed solving.
First of all mpd does not allow to list albums or tracks in a formatted way.
This basically means that you have to fetch the whole database with all tags just to display one part
of the information (in this case either title or album). This is slow. very.
I worked around this by creating a cache for clerk.
Clerk will automatically detect if the mpd database has changed since the last time. If it has it will update
its local cache. No user interaction needed.
But there was another issue. mpc only knows the listall command (which only sends URIs) - not the listallinfo (which sends tags).

But I wanted those nice formatted views!

![Sad Kitten](/images/sad-kitten.jpg)

So I took the hard road and started developing a python clone of mpc. I simply called mppc (music player python client).
It's an explicit dependency for clerk and is used in quite some places.
Not only does it allow for the formatted album/track view, but it also adds readcomments support to clerk, a feature mpd offers
for nearly a year now, but I havent seen a single client using it. With readcomments it's possible to show ALL tags of a file.

But let's see what's left to show.

### The options dialog

![Options Dialog](/images/clerk-options.jpg)

The options dialog gives you all options you would expect in a mpd client.
You can change all modes, enable/disable outputs, set crossfade or toggle replaygain.
In addition it's possible to start/stop mpdscribble. This works for either local
or remote mpdscribbles (set in config file). Right now it kills or start mpdscribble.
Hopefully mpdscribble will receive an option to suspend scrobbling itself via the
client protocol. We will see :)

### Ratings

*** UPDATE ***

The ratings system is using mpds sticker database now, so ratings work for
every filetype. Everything else remains the same, flat files for portability.

One feature in clerk not found elsewhere is the ability to rate albums or tracks.
Personally I don't do track ratings, but in my tests it worked fine for flac
and mp3 files. Vorbis files are not yet implemented. It's just a pain to update
vorbis tags.

So I will only speak about the albumratings now.
First of all, ratings need local access to the music directory.
I wanted a way that is 100% portable and absolutely NOT tied to a musicplayer.
This rules out mpd's sticker database, which seems hardly maintained anyway.
Tags would be another obvious choice, but it's still not accessible enough for my taste.
So the way I created ratings is by saving a ratings file to the album folder.
That's all. A tiny text file containing the actual rating in the first line
and some basic information (artist, date, album) afterwards.

Clerk can even load albums by ratings. To make this happen I use bash's globbing mode
which can very fast wander through the filesystem. Then I only need to grep for ratings in all text files
and voila: It works.

![Ratings](/images/clerk-rating.jpg)

### Mildly related

I already wrote about [musiclist.py](|filename|/blog/mpd-albumlist-creator.md)
This little script uses the ratings file and mpd itself to create a nice table of all albums, including
ratings. Thanks to thor77 this now shows some very nice Stars instead of plain numbers.
You can see the result here: [musiclist](https://list.53280.de)

### The rest

Apart from those features clerk offers basic controls (Play, Stop, Next, Prev, Clear) and lookup of
lyrics, artists, albums (using surfraw).

Last but not least every single dialog is available via cli arguments to quickly bind your favorite features to
hotkeys. See all available arguments with `clerk -h`

If you want to try it out, you can find it on github, together with mppc:<br />
[github](https://github.com/carnager)

To get the most out of it, you really should get the excellent rofi tool by DaveDavenport:<br />
[rofi](https://github.com/DaveDavenport/rofi)
