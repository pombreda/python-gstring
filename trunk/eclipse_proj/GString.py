#    GString wrapper for GLib 2.20.x
#    Written by Christian S. Perone (christian.perone@gmail.com)
#    http://pyevolve.blogspot.com/wordpress
#
#    GString wrapper 1.0
#    Copyright (C) 2009 Christian S. Perone
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = (1, 0)
__author__  = "Christian S. Perone"

import sys
import ctypes as ct
from ctypes.util import find_library

class GStringData(ct.Structure):
   _fields_ = [("str", ct.c_char_p),
               ("len", ct.c_ulong),
               ("allocated_len", ct.c_ulong)]

GStringDataPointer = ct.POINTER(GStringData)

def find_and_set_glib():
   if find_and_set_glib.dll_cache is not None:
      return find_and_set_glib.dll_cache

   if sys.platform.startswith("win"):
      lib_path = find_library("libglib-2.0-0")
   elif sys.platform.startswith("linux"):
      lib_path = find_library("glib-2.0")
   else:
      raise NotImplementedError, "GString not implemented for your platform [%s] !"  % sys.platform

   if lib_path is None:
      raise Exception, "GLib 2.20 not found ! Visit http://library.gnome.org/devel/glib/2.20/"

   dll = ct.CDLL(lib_path)

   dll.glib_check_version.argtypes = [ct.c_uint, ct.c_uint, ct.c_uint]
   dll.glib_check_version.restype = ct.c_char_p
   dll.g_string_new.argtypes = [ct.c_char_p]
   dll.g_string_new.restype  = GStringDataPointer
   dll.g_string_free.argtypes = [GStringDataPointer, ct.c_int]
   dll.g_string_free.restype  = ct.c_char_p
   dll.g_string_sized_new.argtypes = [ct.c_ulong]
   dll.g_string_sized_new.restype = GStringDataPointer
   dll.g_string_assign.argtypes = [GStringDataPointer, ct.c_char_p]
   dll.g_string_assign.restype  = GStringDataPointer
   dll.g_string_append.argtypes = [GStringDataPointer, ct.c_char_p]
   dll.g_string_append.restype  = GStringDataPointer
   dll.g_string_prepend.argtypes = [GStringDataPointer, ct.c_char_p]
   dll.g_string_prepend.restype  = GStringDataPointer
   dll.g_string_insert.argtypes = [GStringDataPointer, ct.c_long, ct.c_char_p]
   dll.g_string_insert.restype  = GStringDataPointer
   dll.g_string_overwrite.argtypes = [GStringDataPointer, ct.c_ulong, ct.c_char_p]
   dll.g_string_overwrite.restype     = GStringDataPointer
   dll.g_string_erase.argtypes = [GStringDataPointer, ct.c_long, ct.c_long]
   dll.g_string_erase.restype  = GStringDataPointer
   dll.g_string_truncate.argtypes = [GStringDataPointer, ct.c_ulong]
   dll.g_string_truncate.restype  = GStringDataPointer
   dll.g_string_hash.argtypes = [GStringDataPointer]
   dll.g_string_hash.restype  = ct.c_uint
   dll.g_string_equal.argtypes = [GStringDataPointer, GStringDataPointer]
   dll.g_string_equal.restype = ct.c_int

   find_and_set_glib.dll_cache = dll
   return dll

find_and_set_glib.dll_cache = None

class GString:
   def __init__(self, text="", size=0):
      self.dll = find_and_set_glib()

      if size > 0:
         self._gstring = self.dll.g_string_sized_new(size)
         self._gstring = self.dll.g_string_assign(self._gstring, str(text))
      else:
         self._gstring = self.dll.g_string_new(text)

   def __del__(self):
      self.dll.g_string_free(self._gstring, 1)

   def __str__(self):
      return self._gstring.contents.str

   def __repr__(self):
      return "<GString [%s]>" % self.__str__()

   def __getitem__(self, key):
      return self._gstring.contents.str[key]
   
   def __len__(self):
      return int(self._gstring.contents.len)

   def __cmp__(self, other):
      return not self.dll.g_string_equal(self._gstring, other._gstring)

   def __hash__(self):
      return self.dll.g_string_hash(self._gstring)

   def __iadd__(self, other):
      self._gstring = self.dll.g_string_append(self._gstring, str(other))
      return self
      
   def __add__(self, other):
      new_gstring = GString(self._gstring.contents.str)
      new_gstring._gstring = self.dll.g_string_append(new_gstring._gstring, str(other))
      return new_gstring

   def assign(self, text):
      """ Copies the bytes from a string into a GString, destroying
      any previous contents. It is rather like the standard strcpy()
      function, except that you do not have to worry about having
      enough space to copy the string. """
      self._gstring = self.dll.g_string_assign(self._gstring, str(text))
      return self

   def append(self, text):
      """ Adds a string onto the end of a GString, expanding it if necessary. """
      return self.__iadd__(text)

   def prepend(self, text):
      """ Adds a string on to the start of a GString, expanding it if necessary. """
      self._gstring = self.dll.g_string_prepend(self._gstring, str(text))
      return self

   def insert(self, pos, text):
      """ Inserts a copy of a string into a GString, expanding it if necessary. """
      self._gstring = self.dll.g_string_insert(self._gstring, pos, str(text))
      return self

   def overwrite(self, pos, text):
      """ Overwrites part of a string, lengthening it if necessary. """
      self._gstring = self.dll.g_string_overwrite(self._gstring, pos, str(text))
      return self

   def erase(self, pos, length):
      """ Removes len bytes from a GString, starting at position pos.
      The rest of the GString is shifted down to fill the gap. """
      self._gstring = self.dll.g_string_erase(self._gstring, pos, length)
      return self

   def truncate(self, length):
      """ Cuts off the end of the GString, leaving the first len bytes. """
      self._gstring = self.dll.g_string_truncate(self._gstring, length)
      return self

   def get_glib_version(self):
      """ Returns the GLib version tuble (major, minor, micro). """
      major = int(ct.c_uint.in_dll(self.dll, "glib_major_version").value)
      minor = int(ct.c_uint.in_dll(self.dll, "glib_minor_version").value)
      micro = int(ct.c_uint.in_dll(self.dll, "glib_micro_version").value)
      return (major, minor, micro)

   def glib_check_version(self, major, minor, micro):
      """ Checks that the GLib library in use is compatible with the given version. """
      return self.dll.glib_check_version(major, minor, micro)

def run_test1():
   import time
   import gc
   import sys
   import StringIO
   import cStringIO
   import gstringc

   string      = ""
   text_to_add = "x" * 40
   iterations  = 100000*8
   
   #print "Timing the Python native str..."
   #gc.collect()
   #time.sleep(1)
   #begin = time.time()
   #for i in xrange(iterations):
   #   string += text_to_add
   #end = time.time()
   #print "Time using Python (str): %.2fs" % (end-begin)

   print "Timing the GString of GLib..."
   gc.collect()
   time.sleep(1)
   begin = time.time()
   string = GString(size=iterations*len(text_to_add))
   for i in xrange(iterations):
      string += text_to_add
   end = time.time()
   print "Time using GLib (GString): %.2fs" %(end-begin)

   print "Timing the StringIO of Python..."
   gc.collect()
   time.sleep(1)
   begin = time.time()
   string = StringIO.StringIO()
   for i in xrange(iterations):
      string.write(text_to_add)
   val = string.getvalue()
   string.close()
   string = StringIO.StringIO()
   for i in xrange(iterations):
      string.write(text_to_add)
   val = string.getvalue()
   string.close()
   end = time.time()
   print "Time using Python (StringIO): %.2fs" %(end-begin)

   print "Timing the cStringIO of Python..."
   gc.collect()
   time.sleep(1)

   begin = time.time()

   string = cStringIO.StringIO()
   for i in xrange(iterations):
      string.write(text_to_add)
   val = string.getvalue()
   string.close()

   string = cStringIO.StringIO()
   for i in xrange(iterations):
      string.write(text_to_add)
   val = string.getvalue()
   string.close()

   end = time.time()

   print "Time using Python (cStringIO): %.2fs" %(end-begin)

   print "Timing the gstringc.GString of GLib..."
   gc.collect()
   time.sleep(1)
   begin = time.time()
   string = gstringc.GString("",iterations*len(text_to_add))
   for i in xrange(iterations):
      string += text_to_add
   string = gstringc.GString("",iterations*len(text_to_add))
   for i in xrange(iterations):
      string += text_to_add
   end = time.time()
   print "Time using GLib (gstringc.GString): %.2fs" %(end-begin)

   print "Timing the gstringc.GString+gstringc.GString of GLib..."
   gc.collect()
   time.sleep(1)
   text_to_add_gstring = gstringc.GString("x" * 40)
   begin = time.time()
   string = gstringc.GString("",iterations*len(text_to_add_gstring))
   for i in xrange(iterations):
      string += text_to_add_gstring
   string = gstringc.GString("",iterations*len(text_to_add_gstring))
   for i in xrange(iterations):
      string += text_to_add_gstring
   end = time.time()
   print "Time using GLib (gstringc.GString+gstringc.GString): %.2fs" %(end-begin)

   print "Timing the gstringc.GString+gstringc.GString of GLib (no initial size)..."
   gc.collect()
   time.sleep(1)
   text_to_add_gstring = gstringc.GString("x" * 40)
   begin = time.time()
   string = gstringc.GString("")
   for i in xrange(iterations):
      string += text_to_add_gstring
   string = gstringc.GString("")
   for i in xrange(iterations):
      string += text_to_add_gstring
   end = time.time()
   print "Time using GLib (gstringc.GString+gstringc.GString): %.2fs" %(end-begin)


   print "Timing the gstringc.GString (append) of GLib..."
   gc.collect()
   time.sleep(1)
   begin = time.time()
   string = gstringc.GString("",iterations*len(text_to_add))
   for i in xrange(iterations):
      string.append(text_to_add)
   string = gstringc.GString("",iterations*len(text_to_add))
   for i in xrange(iterations):
      string.append(text_to_add)
   end = time.time()
   print "Time using GLib (gstringc.GString/append): %.2fs" %(end-begin)


if __name__ == "__main__":
   run_test1()