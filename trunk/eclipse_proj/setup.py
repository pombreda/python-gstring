import sys
import commands
from distutils.core import setup
from distutils.extension import Extension

__author__ = "Christian S. Perone"
__authormail__ = "christian.perone@gmail.com"



def pkgconfig(*packages, **kw):
   flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
   for token in commands.getoutput("pkg-config --libs --cflags %s" % ' '.join(packages)).split():
      kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
   return kw

if sys.platform.startswith("win"):
	mod_gstringc = Extension("gstringc",
                  sources=["gstringc.c"],
                  include_dirs=['C:\Arquivos de programas\Gtk+\include\glib-2.0',
                                'C:\Arquivos de programas\Gtk+\lib\glib-2.0\include'],
                  library_dirs=['C:\Arquivos de programas\Gtk+\lib'],
                  libraries=['glib-2.0'])

	setup(name='python-gstringc',
			version='1.0',
			description='A fast Python extension for GLib::GString.',
			author=__author__,
			author_email=__authormail__,
			url='http://pyevolve.sourceforge.net/wordpress',
			ext_modules=[mod_gstringc])


elif sys.platform.startswith("linux"):
	mod_gstringc = Extension("gstringc",
                  sources=["gstringc.c"],
						**pkgconfig('glib-2.0'))

	setup(name='python-gstringc',
			version='1.0',
			description='A fast Python extension for GLib::GString.',
			author=__author__,
			author_email=__authormail__,
			url='http://pyevolve.sourceforge.net/wordpress',
			ext_modules=[mod_gstringc])

else:
   raise Exception, "Unknow platform ! Contact %s" % __author__
