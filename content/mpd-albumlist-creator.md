Title: Create html list of all your albums
Date: 2014-04-05 14:20
Tags: MPD, linux, scripting, python
Category: computer
Slug: albumlist_creator
Author: Rasi
Summary: Python script that creates a html table of all your albums, using python-mpd2

## Python to the rescue

I love my CD collection. I needed months to rip all my CDs into flac format and tagging it all correctly will probably never be finished.
But what use is the biggest collection if you cannot show off? So I wanted a script that makes a nice html table of my music.
And ideally it uses MPD since that has an index of my music anyway.

So I started fiddling with bash and mpc only to find out that mpc is too limited to reach my goal. At least not in a performant way.
So the aproach I originally took was to use metaflac to scan my collection and create a html table from that.
This is how it looks:

~~~~~~
#!/bin/bash
echo '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<meta name="robots" content="noindex" />
<title>My Music</title>
<style type="text/css"><!--body {font-family:arial;font-size: medium;color: #3D3D3D;}table.tablesorter {background-color: 
#CDCDCD; align="center"; margin: 0px auto;text-align: left;width: 50%;}table.tablesorter thead tr th, table.tablesorter tfoot tr th 
{background-color: #e6EEEE;border: 1px solid #FFF;font-size: medium;padding: 4px;}table.tablesorter thead tr .header 
{background-image:url(data:image/gif;base64,R0lGODlhFQAJAIAAACMtMP///yH5BAEAAAEALAAAAAAVAAkAAAIXjI+AywnaYnhUMoqt3gZXPmVg94yJVQAAOw%3D%3D);background-repeat: 
no-repeat;background-position: center right;cursor: pointer;}table.tablesorter tbody td {color: #3D3D3D;padding: 
4px;background-color: #FFF;vertical-align: top;}table.tablesorter tbody tr.odd td { background-color:#F0F0F6; }table.tablesorter 
thead tr .headerSortUp { 
background-image:url(data:image/gif;base64,R0lGODlhFQAEAIAAACMtMP///yH5BAEAAAEALAAAAAAVAAQAAAINjB+gC+jP2ptn0WskLQA7); 
}table.tablesorter thead tr .headerSortDown { 
background-image:url(data:image/gif;base64,R0lGODlhFQAEAIAAACMtMP///yH5BAEAAAEALAAAAAAVAAQAAAINjI8Bya2wnINUMopZAQA7); 
}table.tablesorter thead tr .headerSortDown, table.tablesorter thead tr .headerSortUp {background-color: #8dbdd8; }--></style>
</head>
<body>
<script type="text/javascript" src="jquery.min.js"></script>
<script type="text/javascript" src="jquery.tablesorter.js"></script>
<script type="text/javascript"><!--
--></script>
<table id="music" class="tablesorter" margin-{left,right}: auto;>
<thead>
  <tr>
	  <th>Artist</th>
		  <th>Album</th>
			  <th>Ratings</th>
	   </tr>
		</thead>
		 <tbody>'
me="${0##*/}"
if [ $# -eq 0 -o "$1" = '-h' -o "$1" = '--help' -o ! -d "$1" ]; then
	echo "Usage: $me /path/to/flacs" 1>&2
	exit 1
fi
fdir="$1"
if [ -z "$TMPDIR" ]; then TMPDIR='/tmp'; fi
tdir="$( mktemp -d "${TMPDIR}/${me}.XXXXXXXX" )"
if [ -z "$tdir" ]; then
	echo "$me: error: mktemp failed." 1>&2
	exit 1
fi
lastDir=''
while read f; do
	if [ ! -f "$f" ]; then continue; fi
	currentDir="${f%/*}"
	if [ "$currentDir" = "$lastDir" ]; then continue; fi
	lastDir="$currentDir"
	shopt -qs nocasematch
	artist='' albumArtist='' album='' year='0000'
	while read line; do
		case "$line" in
			artist=*) artist="${line#*=}" ;;
			albumartist=*|album*artist=*) albumArtist="${line#*=}" ;;
			album=*) album="${line#*=}" ;;
			date=*) year="${line#*=}" ;;
		esac
	done < <( metaflac --export-tags-to=- "$f" 2>/dev/null )
	shopt -qu nocasematch
	if [ -z "$albumArtist" -a -z "$artist" ]; then continue; fi
	if [ -z "$albumArtist" ]; then albumArtist="$artist"; fi
	if [ -z "$album" ]; then continue; fi
	artistHash="$( echo -n "$albumArtist" | md5sum - | cut -d ' ' -f 1 )"
	if [ ! -d "${tdir}/${artistHash}" ]; then
		echo "${artistHash} ${albumArtist}" >> "${tdir}/artists"
		mkdir "${tdir}/${artistHash}"
	fi
	rating='-'
	if [ -f "${currentDir}/../../rating.txt" ]; then
		read rating < "${currentDir}/../../rating.txt"
	elif [ -f "${currentDir}/../rating.txt" ]; then
		read rating < "${currentDir}/../rating.txt"
	elif [ -f "${currentDir}/rating.txt" ]; then
		read rating < "${currentDir}/rating.txt"
	fi
	echo "$year $rating $album" >> "${tdir}/${artistHash}/albums"
done < <( find "$fdir" -type f -iname '*.flac' 2>/dev/null | sort -u )
while read artistHash artist; do
		rowspan="$( sort -u "${tdir}/${artistHash}/albums" 2>/dev/null | wc -l 2>/dev/null )"
	echo "<tr>"
	echo "  <td rowspan="$rowspan">${artist//&/&amp;}</td>"
	while read year rating album; do
				echo "  <td>$year ${album//&/&amp;}</td>"
				echo "  <td><font color=red>${rating}</font></td>"
				echo "</tr>"
	done < <( sort -u "${tdir}/${artistHash}/albums" 2>/dev/null )
done < <( sort -u -k 2 "${tdir}/artists" 2>/dev/null )
echo "</tbody></table>
<p>
	<a href="http://validator.w3.org/check?uri=referer"><img
	  src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>
  </p>
</body></html>"
rm -rf "$tdir"
~~~~~~

This worked perfectly but it had a drawback. Original music that I purchased from amazon and other sources could not be read by metaflac.
Using mutagen could have been another option, but I *really* prefer to do my stuff with MPD :)

## rob``, python and performance

rob`` from the german arch linux IRC channel was so kind to create this really neat python script which does exactly what I wanted:
Get all artists and their albums and create a nice html table. In addition it also scans my album ratings (created with my [mpdmenu]({filename}/mpdmenu.md)
) and puts them in another column.
After some css tweaking the script was done in a few minutes.
The above bash script which uses metaflac takes about 1 minute to finish the table. My tries with bash+mpc needed at least 20 minutes (!). 
This very script now needs around 30 seconds. Not too bad :)

Anyway here is the script:

~~~~~~
#!/usr/bin/env python2
from __future__ import print_function
import os
import operator
import re
import mpd  # pacman -S python2-mpd
MUSIC_ROOT = '/mnt/wasteland/Audio/Rips'
RATING_FILE = 'rating.txt'
def query(c, *items, **conditions):
	if conditions:
		# turn dict into flattened list, e.g.
		# {k1: v1, k2: v2} -> [k1, v1, k2, v2]
		cond = reduce(operator.add, conditions.items())
		results = c.find(*cond)
	else:
		results = c.listallinfo()
	yielded = set()
	for r in results:
		d = []
		for i in items:
			it = r.get(i)
			if isinstance(it, list):
				it = it[0]
			d.append(it)
		d = tuple(d)
		if all(d) and d not in yielded:
			yield d
		yielded.add(d)
def get_artists(c):
	a = [r[0] for r in query(c, 'albumartist')]
	return a
def get_rating(c, artist, date, album):
	r = query(c, 'file', albumartist=artist, date=date, album=album)
	path = next(r)[0]
	path = os.path.join(MUSIC_ROOT, path)
	path = os.path.dirname(path)
	if re.search("CD ?\d", path, flags=re.IGNORECASE):
		path = os.path.dirname(path)
	path = os.path.join(path, RATING_FILE)
	try:
		with(open(path)) as f:
			rating = f.readline().strip()
			return rating
	except IOError:
		return "-"
def main():
	c = mpd.MPDClient()
	host = os.environ.get('MPD_HOST', 'localhost')
	port = os.environ.get('MPD_PORT', '6600')
	pw = None
	if "@" in host:
		pw, host = host.split("@")
	c.connect(host, port)
	if pw is not None:
		c.password(pw)
	print("<html>")
	print("<head><meta charset=\"utf-8\"/><link rel=\"stylesheet\" href=\"//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css\"><style>body{background:#eee}table{margin:5em auto; max-width:56em; background: white;}</style></head>")
	print("<body>")
	print("<div class=\"table-responsive\">")
	print("<table id=\"music\" class=\"table table-bordered\">")
	print("<thead>")
	print("<tr><th>Artist</th><th>Year</th><th>Album</th><th>Rating</th></tr></thead><tbody>")
	for artist in sorted(get_artists(c), key=lambda v: (v.upper(), v[0].islower())):
		albums = sorted(query(c, 'date', 'album', albumartist=artist))
		print('<tr class=\"newartist\"><td rowspan="{0}">{1}</td>'.format(len(albums), artist))
		for i, (date, album) in enumerate(albums):
			rating = get_rating(c, artist, date, album)
			# templating libraries ftw
			print("<td>{}</td>".format(date))
			print("<td>{}</td>".format(album))
			print("<td><font color=\"red\">{}</td>".format(rating))
			print("</tr>")
	print("</table></div>")
if __name__ == '__main__':
	main()
~~~~~~

## The Result

And [here](https://53280.de/music.html) is how the generated html will look like
