#!/usr/bin/env python
#http://stackoverflow.com/questions/296499/how-do-i-zip-the-contents-of-a-folder-using-python-version-2-5
from __future__ import with_statement
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import os

def zipdir(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)

if __name__ == '__main__':
    basedir=input("what folder do you want to zip?\n")
	import os
	while !os.path.isdir(basedir):
	    basedir=input("no such dir,enter again\n")
	archivename=basedir+'.zip'
    zipdir(basedir, archivename)
