import sys
from distutils.core import setup
from distutils.extension import Extension

__author__ = "Christian S. Perone <christian.perone@gmail.com>"

if sys.platform.startswith("win"):
   setup(name='python-gstringc',
         version='1.0',
         ext_modules=[Extension('gstringc', ['gstringc.c'])],
         )

elif sys.platform.startswith("linux"):
   print "LINUX"
else:
   raise Exception, "Unknow platform ! Contact %s" % __author__