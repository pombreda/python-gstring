#!/bin/sh
PY_CFLAGS=`python2.6-config --cflags`
GLIB_CFLAGS=`pkg-config --cflags glib-2.0`

PY_LIBS=`python2.6-config --libs`
GLIB_LIBS=`pkg-config --libs glib-2.0`

EXTRA_FLAGS="-Wall -fPIC -DNDEBUG -g -Wstrict-prototypes"

gcc $PY_CFLAGS $GLIB_CFLAGS $EXTRA_FLAGS -c gstringc.c -o gstringc.o
gcc $PY_LIBS $GLIB_LIBS -shared -o gstringc.so gstringc.o

