import os

__dirlist = os.listdir("WebRoot")

__all__ = []

for __dirent in __dirlist:
        #print "__dirent = %s" % ( __dirent )
        if __dirent[-3:] != ".py":
                continue
        if __dirent == "__init__.py":
                continue
        __all__.append(__dirent[0:-3])


