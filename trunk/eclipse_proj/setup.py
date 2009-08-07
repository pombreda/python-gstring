import sys
from distutils.core import setup
from distutils.extension import Extension

__author__ = "Christian S. Perone"
__authormail__ = "christian.perone@gmail.com"

mod_gstringc = Extension("gstringc",
                  sources=["gstringc.c"],
                  include_dirs=['C:\Arquivos de programas\Gtk+\include\glib-2.0',
                                'C:\Arquivos de programas\Gtk+\lib\glib-2.0\include'],
                  library_dirs=['C:\Arquivos de programas\Gtk+\lib'],
                  libraries=['glib-2.0'])

if sys.platform.startswith("win"):
   setup(name='python-gstringc',
         version='1.0',
         description='A fast Python extension for GLib::GString.',
         author=__author__,
         author_email=__authormail__,
         url='http://pyevolve.sourceforge.net/wordpress',
         ext_modules=[mod_gstringc],
         )
elif sys.platform.startswith("linux"):
   print "LINUX"
else:
   raise Exception, "Unknow platform ! Contact %s" % __author__