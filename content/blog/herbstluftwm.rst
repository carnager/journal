Herbstluftwm
############
:date: 2013-06-05 10:00
:author: Rasi
:slug: herbstluftwm
:category: computer
:tags: windowmanager, linux, tiling, herbstluftwm

In my neverending journey to find the optimal windowmanager, I finally
ended up trying herbstluftwm, which i wanted to give a shot for ages.

Turned out to be a good choice. But wait. What makes herbstluftwm
different from the gazillion other windowmanagers out there? Let's dive
into it.

--------------

The config file...
^^^^^^^^^^^^^^^^^^

...which really is no config file at all. You see, in herbstluftwm
everything is done through a helper binary called herbstclient. You want
to resize a window? You call something like

.. code-block:: bash

    herbstclient resize right +0.05

The same thing applies to every other possible action. So the config
file is really just a set of herbstclient commands that sets the initial
state of the windowmanager. This includes things like number of
workspaces (and names for them too), layout for individual workspaces,
placement rules for applications, as well as theming and keybindings.

Here is my example config file (which is appropriately called
"autostart"):

.. code-block:: bash

    #!/bin/bash

    # this is a simple config for herbstluftwm

    function hc() {
    herbstclient "$@"
    }

    hc emit_hook reload

    #xsetroot -solid '#5A8E3A'


    # remove all existing keybindings
    hc keyunbind --all

    # keybindings
    Mod=Mod4
    hc keybind $Mod-z floating toggle
    hc keybind $Mod-Shift-q quit
    hc keybind $Mod-Shift-r reload
    hc keybind $Mod-k close
    hc keybind $Mod-Return spawn termite --role=term /bin/zsh
    hc keybind $Mod-Shift-Return spawn termite /bin/zsh
    hc keybind Print spawn teiler
    hc keybind $Mod-Shift-s spawn termite --role=ssh -e karif
    hc keybind $Mod-Shift-F12 spawn lastfm.sh switch
    hc keybind $Mod-F12 spawn lastfm.sh check
    hc keybind $Mod-Shift-F11 spawn love
    hc keybind $Mod-Tab spawn simpleswitcher -now

    hc keybind $Mod-p spawn dmenu_run

    # tags
    TAG_NAMES=( {terms,www,stuff,media,dl,gfx} )
    TAG_KEYS=( {1..9} 0 )

    hc rename default "${TAG_NAMES[0]}" || true
    for i in ${!TAG_NAMES[@]} ; do
        hc add "${TAG_NAMES[$i]}"
        key="${TAG_KEYS[$i]}"
        if ! [ -z "$key" ] ; then
            hc keybind "$Mod-$key"       use  "${TAG_NAMES[$i]}"
            hc keybind "$Mod-Shift-$key" move "${TAG_NAMES[$i]}"
        fi
    done

    # cycle through tags
    hc keybind $Mod-period use_index +1 --skip-visible
    hc keybind $Mod-comma  use_index -1 --skip-visible
    hc keybind $Mod-Right focus right
    hc keybind $Mod-Left focus left
    hc keybind $Mod-Up focus up
    hc keybind $Mod-Down focus down
    hc keybind $Mod-Shift-Right shift right
    hc keybind $Mod-Shift-Left shift left
    hc keybind $Mod-Shift-Up shift up
    hc keybind $Mod-Shift-Down shift down

    # layouting
    hc keybind $Mod-r remove
    hc keybind $Mod-space cycle_layout 1
    hc keybind $Mod-v split vertical 0.5
    hc keybind $Mod-h split horizontal 0.5
    hc keybind $Mod-Shift-v split vertical 0.3
    hc keybind $Mod+Shift+h split horizontal 0.3
    hc keybind $Mod-s floating toggle
    hc keybind $Mod-f fullscreen toggle
    hc keybind $Mod-Shift-p pseudotile toggle

    # resizing
    RESIZESTEP=0.05
    hc keybind $Mod-Control-Left resize left +$RESIZESTEP
    hc keybind $Mod-Control-Down resize down +$RESIZESTEP
    hc keybind $Mod-Control-Up resize up +$RESIZESTEP
    hc keybind $Mod-Control-Right resize right +$RESIZESTEP

    # mouse
    hc mouseunbind --all
    hc mousebind $Mod-Button1 move
    hc mousebind $Mod-Button2 resize
    hc mousebind $Mod-Button3 zoom

    # focus
    hc keybind $Mod-BackSpace   cycle_monitor
    #hc keybind $Mod-Tab         cycle_all +1
    #hc keybind $Mod-Shift-Tab   cycle_all -1
    hc keybind $Mod-c cycle
    hc keybind $Mod-i jumpto urgent
    hc keybind $Mod-KP_Left shift left
    hc keybind $Mod-KP_Down shift down
    hc keybind $Mod-KP_Right shift right
    hc keybind $Mod-KP_Up shift up

    # colors
    hc set frame_border_active_color '#82B414'
    hc set frame_border_normal_color '#0c0d0e'
    hc set frame_bg_normal_color '#121212'
    hc set frame_active_opacity 90
    hc set frame_normal_opacity 70
    hc set frame_bg_active_color '#121212'
    hc set frame_bg_transparent 0
    hc set frame_border_width 1
    hc set window_border_width 1
    hc set window_border_inner_width 3
    hc set window_border_normal_color '#454545'
    hc set window_border_active_color '#0c73c2'
    hc set always_show_frame 1
    hc set frame_gap 2
    # add overlapping window borders
    hc set window_gap 2
    hc set frame_padding 0
    hc set smart_window_surroundings 1

    hc set smart_frame_surroundings 1
    hc set mouse_recenter_gap 0
    hc set focus_follows_mouse 1
    hc set raise_on_focus 1
    hc pad 5 5 5 5 5

    # rules
    hc unrule -F
    #hc rule class=XTerm tag=3 # move all xterms to tag 3
    hc rule focus=on # normally do not focus new clients
    # give focus to most common terminals
    hc rule class~'(.*[Rr]xvt.*|.*[Tt]erm|Konsole)' focus=on
    hc rule windowtype~'_NET_WM_WINDOW_TYPE_(DIALOG|UTILITY|SPLASH)' pseudotile=on
    hc rule windowtype='_NET_WM_WINDOW_TYPE_DIALOG' focus=on
    hc rule windowtype~'_NET_WM_WINDOW_TYPE_(NOTIFICATION|DOCK)' manage=off
    hc rule class=Firefox tag=www
    hc rule windowrole=term tag=terms
    hc rule windowrole=ssh tag=terms

    # unlock, just to be sure
    hc unlock

    herbstclient set tree_style '╾│ ├└╼─┐'

    # do multi monitor setup here, e.g.:
    # hc set_monitors 1280x1024+0+0 1280x1024+1280+0
    # or simply:
    # hc detect_monitors

    # find the panel
    panel=~/.config/herbstluftwm/panel.sh
    [ -x "$panel" ] || panel=/etc/xdg/herbstluftwm/panel.sh
    for monitor in $(herbstclient list_monitors | cut -d: -f1) ; do
    # start it on each monitor
    $panel $monitor &
    done

    # GIMP
    # ensure there is a gimp tag
    hc load gfx '
    (split horizontal:0.850000:0
      (split horizontal:0.200000:1
        (clients vertical:0)
        (clients grid:0))
       (clients vertical:0))
     '               # load predefined layout
    # center all other gimp windows on gimp tag
    hc rule class=Gimp tag=gfx index=01 pseudotile=on
    hc rule class=Gimp windowrole~'gimp-(image-window|toolbox|dock)' \
        pseudotile=off
    hc rule class=Gimp windowrole=gimp-toolbox focus=off index=00
    hc rule class=Gimp windowrole=gimp-dock focus=off index=1

    All the available commands are explained in the manpage of herbstluftwm.
    But the last bit needs some special attention.

--------------

layouts
^^^^^^^

The nice thing about herbstluftwm, compared to e.g. i3 is that you can
predefine layouts per workspace. Watch the code again:

.. code-block:: bash

    # GIMP
    # ensure there is a gimp tag
    hc load gfx '
    (split horizontal:0.850000:0
      (split horizontal:0.200000:1
        (clients vertical:0)
        (clients grid:0))
       (clients vertical:0))
     '               # load predefined layout
    center all other gimp windows on gimp tag
    hc rule class=Gimp tag=gfx index=01 pseudotile=on
    hc rule class=Gimp windowrole~'gimp-(image-window|toolbox|dock)' \
    pseudotile=off
    hc rule class=Gimp windowrole=gimp-toolbox focus=off index=00
    hc rule class=Gimp windowrole=gimp-dock focus=off index=1

This makes sure that we create 3 "tiles" on a workspace called "gfx".
Then it creates rules based on the gimp windows, so that each gimp
window will be put into the desired tile. This will result in this:

|layouts|

That's really nice, isn't it? The best part is you don't have to fiddle
with this by try and error. simply resize your windows the way you want
them to be and run

.. code-block:: bash

    herbstclient dump gfx

where gfx is the workspace name (or tag). This will output the desired
string which you can either use manually like i did in my gimp example,
or you use the command:

.. code-block:: bash

    herbstclient load "$(cat DUMP_FILE)"

--------------

frames vs. windows
^^^^^^^^^^^^^^^^^^

The thing about herbstluftwm that is most obviously different from other
windowmanagers is probably the added layer called "frames". Where you
simply tile windows in other windowmanagers, you create frames in
herbstluftwm. Inside of these frames you finally start your
applications. Each frame can be tiled individually. This is best
explained with a screenshot:

|hlwm|

Have a look at the upper right corner. There are 4 terminal windows. The
active one has a blue border. But look outside of those 4 windows. There
is another border - green in my case. This marks the frame. Inside of
this you can have as many open windows as you wish and tile them in
different ways (splith, splitv, grid, maximized). The terminal window on
the lower right is another frame. Since its a single window it would
only receive a green outline when focused. The 2 terminals on the left
are another frame. This adds a bit of complexibility but is quite
flexible too.

--------------

panels
^^^^^^

Another nice thing about hlwm is the way it handles panels. Hlwm has an
inbuilt margin feature to preserve space for panels. This way I could
easily make sure that my xfce4-panel works flawlessly. When you watch my
config file above you probably noticed that it calls a script named
"panel.sh". The default panel.sh script sets some variables which are
finally piped to dzen2. That's rather nice, but it's missing a
systemtray. In addition to this current dzen2 has a bug which makes
clickable workspaces non-functional. So i created a very minimal
panel.sh which only loads my xfce4-panel:

.. code-block:: bash

    #!/bin/bash
    monitor=${1:-0}
    panel_height=16
    herbstclient pad $monitor $panel_height

That's all. xfce4-panel works perfectly, thanks to the "panel\_height"
option.

--------------

floating
^^^^^^^^

Most tiling window managers have a special layer for floating windows.
Windows that float will simply be shown on top of your other windows.
Herbstluftwm does not know the concept of a special floating layer. It's
either all floating or all tiled, but you can switch between these modes
with one keystroke.

As a workaround herbstluftwm includes a mode called "pseudotile".
Applications that are tagged to be pseudotiled (in default config this
includes all dialogs), will simply be tiled too, but still they are
floating. kind of. Let's show:

|pseudotile|

As you can see the dialog is in a regular tile (50% vertical split) but
still its dimensions are kept. While this works ok for some apps, it
works bad for others. Luckily a proper floating layer will be added to
hlwm in the future, but the developers are not sure yet how it will
look/work in the end.

--------------

conclusion
^^^^^^^^^^

Herbstluftwm is a very nice window manager.

-  The configuration is dead easy, a simple bash (perl,python,etc) file
   which calls a bunch of herbstclient commands.
-  Little things are taken care of, like the margin feature for panels.
-  Did I mention that hlwm supports compositing out of the box? Well, it
   does.

But the best part: Its constantly being worked on and has several
contributors, which is a very good sign for a free software project.

.. |layouts| image:: https://blog.53280.de/content/images/2014/Jan/hlwm_layout.png
.. |hlwm| image:: https://blog.53280.de/content/images/2014/Jan/hlwm.png
.. |pseudotile| image:: https://blog.53280.de/content/images/2014/Jan/pseudotile.png
