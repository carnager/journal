Fluxbox with manual tiling
##########################
:date: 2013-01-26 11:00
:author: Rasi
:tags: linux, windowmanager, tiling, fluxbox
:category: computer
:slug: fluxbox-with-manual-tiling

--------------

So partly because I was bored, partly because subtle doesn’t work very
well with both qt and gtk3, i decided to fiddle around with fluxbox a
bit. My goal was to make it behave as closely to my subtle setup as
possible. Of all the \*box WMs I only ever used openbox properly before.
And while theoretically possible, I soon gave up porting my subtle
config to it. XML is just such a mess. Really, whoever thought XML is
suitable for config files is nuts.

So back to fluxbox. It turned out that setting it up is very straight
forward. There are a handful of files you want to look at more closely:

--------------

~/.fluxbox/init
^^^^^^^^^^^^^^^

this file stores the general options, like focus model, enable/disable
tabs, settings for the internal panel. Most of it is pretty obvious
stuff.

--------------

~/.fluxbox/keys
^^^^^^^^^^^^^^^

This is where the fun starts. In this file you set up all your key
bindings. Nothing special, every WM does this. But there is a but.
Fluxbox has some unique ways that make it the optimal choice for my
plan. So what did I actually want? In my subtle setup I had a few
hotkeys, that move windows to one of the 4 corners on screen or fill up
half the screen either horizontally or vertically. MacroCmd to the
rescue!

Of course fluxbox supports positioning windows and resizing windows, but
what if you want to have both things without strictly tagging windows?
(to retain flexibility) The solution is actually pretty easy:

::

    Mod4 KP_1 :MacroCmd {ResizeTo 945 500} {MoveTo 4 4 LowerLeft} {Raise} {Focus}

This will move the current window to the upper left corner and resize it
to fill 25% of my screen. Percentage values are also possible, tho less
exact. Another thing I had in my subtle setup was the ability to start
terminal windows instantly at specified areas (matching my grid to move
windows around) To do this you have to give your terminal a proper name.
For urxvt you can use the -name argument, for xfce4-terminal –role=foo
will work. With these unique names we can now tag all windows matching
those. Which leads us to:

--------------

~/.fluxbox/apps
^^^^^^^^^^^^^^^

the apps file is very simple to use. Lets see an example:

::

    [app] (role=term_top_left) [Dimensions] {945 500} [Position] (UPPERLEFT) {4 4}[Workspace] {0} [Deco] {BORDER} [Alpha] {245 230} [end]

Pretty obvious, once you have seen it. The last line is particulary
interesting tho: It sets transparency values based based on active state
of the window. I don’t know any other WM that has such an option. Pretty
neat if you want some eyecandy! Apart from this the apps file normally
is used to simply set a workspace for an application. Unlike subtle,
fluxbox never forces the workspace tho, you are free to move your
windows everytime. Anyway, basic setup was complete, now all that was
left was to clone subtle’s panel, which seemed like an impossible task.
Fluxbox internal panel is far too limited, so I gave xfce4-panel another
try - and was surprised how good you can make it look - using more or
less nothing but generic command widgets :) Fluxbox doesn’t work too
well with xfce4-panel, maximized windows will cover it. Luckily I found
a patch that works around this. For your convinience, here it is:

`patch`_

--------------

Mandatory Screenshot
^^^^^^^^^^^^^^^^^^^^

|Screenshot|

.. _patch: https://dl.53280.de/fluxbox-wm-strut-partial.patch

.. |Screenshot| image:: https://blog.53280.de/content/images/2014/Jan/fluxbox_shot.png
