@echo off

\python25\python setup.py clean
\python26\python setup.py clean

\python26\python setup.py build
\python26\python setup.py sdist --formats=gztar,zip
\python26\python setup.py bdist --format=wininst

\python26\python setup.py clean
\python25\python setup.py clean

\python25\python setup.py bdist --format=wininst

\python25\python setup.py clean
\python26\python setup.py clean

