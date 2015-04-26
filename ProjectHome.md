A pythonic wrapper of the GLib GString.

**If you want more performance, check the C extension I've done for GLib::GString [here](http://code.google.com/p/python-gstringc).**

The python-gstring uses Python ctypes to create a wrapper of [GLib](http://library.gnome.org/devel/glib/2.20/) GString; the GLib Srings are text buffers which grow automatically as text is added, they have many handling methods described in the documentation on the GLib site.

python-gstring is simple, open-source and runs under Linux and Windows (you must have gtk or just [glib](http://ftp.gnome.org/pub/gnome/binaries/win32/glib/2.20/glib_2.20.4-1_win32.zip) installed).

You can find more information about GLib GString [here](http://library.gnome.org/devel/glib/2.20/glib-Strings.html#g-string-insert).

See the wiki here on Google hosting of python-gstring for more information about python-gstring.

**I'm working on a C version of this wrapper with new features and better performance.**

- _Christian S. Perone_

http://pyevolve.sourceforge.net/wordpress