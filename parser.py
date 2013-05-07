#!/usr/bin/env python
#-*-coding:utf-8-*-
from optparse import OptionParser

def start():
    
    parser = OptionParser()
    
    parser.add_option("-u", "--start", dest="url",
                      help="starting from here")
    parser.add_option("-d", "--deep",dest="level",default=2,
                      help="setting level")
    parser.add_option("--thread", dest="pool_size",default=10,
                      help="thread pool num")
    parser.add_option("--dbfile", dest="dbfile",
                      help="write data to FILE", metavar="FILE")
    parser.add_option("--key", dest="keywords",
                      help="keywords")
    parser.add_option("-l", dest="loglevel",
                      help="log record")
    parser.add_option("--testself", dest="dotest",
                      help="db test")
    (options, args) = parser.parse_args()

    return options