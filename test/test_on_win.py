#!/usr/local/bin/python2.7

__project__ = "RSS-feed-downloader"
__author__  = "Khaled Monsoor <k@kmonsoor.com>"
__license__ = "MIT"

"""
This is a sample test module
"""

remote = "http://archive.apache.org/dist/apr/binaries/win32/apr-1.2.12-winnt-x86-ipv6-msvcrt60.zip"
local = "c:\\new"
print remote
print local

download(remote,local)
