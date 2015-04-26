# Introduction #

A pythonic wrapper of the rock-stable GLib GString.

The python-gstring uses Python ctypes to create a wrapper of [GLib](http://library.gnome.org/devel/glib/2.20/) GString; the GLib Srings are text buffers which grow automatically as text is added, they have many handling methods described in the documentation on the GLib site.

python-gstring is simple, open-source and runs under Linux and Windows (you must have gtk or just [glib](http://ftp.gnome.org/pub/gnome/binaries/win32/glib/2.20/glib_2.20.4-1_win32.zip) installed).

You can find more information about GLib GString [here](http://library.gnome.org/devel/glib/2.20/glib-Strings.html#g-string-insert).

See the wiki here on Google hosting of python-gstring for more information about python-gstring.

**I'm working on a C version of this wrapper with new features and better performance.**

## Performance comparsion ##

You can run performance comparison by doing:

```
   python GString.py
```

You'll probably get different performance issues on Windows and Linux, GLib can be nearly 5 times faster than Python native str under Windows. Here is a result of tests on Windows:

```
Timing the Python native str...
Time using Python (str): 29.42s
Timing the GString of GLib...
Time using GLib (GString): 7.53s
Timing the StringIO of Python...
Time using Python (StringIO): 1.11s
Timing the cStringIO of Python...
Time using Python (cStringIO): 0.27s
```

# API Reference #

## Class GString ##

**Constructor**
**GString(text="", size=0)**

Creates a new GString object with blank text, if size is greater than zero, it will allocate the size bytes in the GString buffer.

**GString.assign(text)**

Copies the bytes from a string into a GString, destroying
any previous contents. It is rather like the standard strcpy()
function, except that you do not have to worry about having
enough space to copy the string.

**GString.append(text)**

Adds a string onto the end of a GString, expanding it if necessary.

**GString.prepend(text)**

Adds a string on to the start of a GString, expanding it if necessary.

**GString.insert(pos, text)**

Inserts a copy of a string into a GString, expanding it if necessary.

**GString.overwrite(pos, text)**

Overwrites part of a string, lengthening it if necessary.

**GString.erase(pos, length)**

Removes len bytes from a GString, starting at position pos.
The rest of the GString is shifted down to fill the gap.

**GString.truncate(length)**

Cuts off the end of the GString, leaving the first len bytes.

**GString.get\_glib\_version**

Returns the GLib version tuble (major, minor, micro).

**GString.glib\_check\_version(major, minor, micro)**

Checks that the GLib library in use is compatible with the given version.

### Native string emulation ###

```
__str__ method
Example:
   print gstring_object
   text in the buffer

__repr__ method
Example:
   repr(gstring_object)
   <GString [text in the buffer]>

__getitem__ method
Example:
   for i in xrange(len(gstring_object)):
      print gstring_object[i]

__len__ method
Example:
   print len(gstring_object)

__cmp__ method
Example:
   print gstring_object1 == gstring_object2

__hash__ method
Example:
   print hash(gstring_object)

__iadd__ method
Example:
   gstring_object += "text"

__add__ method
Example:
   new_gstring_obj = gstring_object1 + gstring_object2
```


