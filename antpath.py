'''
Created on 30.05.2014

@author: kolbe
'''
import os, sys, datetime, time
from antpathdetector import AntPathDetector
from optparse import OptionParser

if __name__ == '__main__':
    
    print "antpath"
    parser = OptionParser()
    parser.add_option("-f", "--file",
                  action="store", type="string", dest="filename",
                  help="Input videofile")
    parser.add_option("-s", "--scale",
                  action="store", type="float", dest="scale",
                  default=0.4,
                  help="Scale video to scale * size")
    parser.add_option("-o", "--output",
                  action="store", type="string", dest="output",
                  default=None,
                  help="Output directory")
    parser.add_option("-d", "--debug",
                  action="store_true", dest="debug",
                  default=False,
                  help="Show additional windows")
    (options, args) = parser.parse_args()
    print options
    print args
    
    if not options.filename:
        parser.error("No input filename!")
    if options.output is not None:
        if not os.path.exists(options.output):
            os.mkdir(options.output)
        
    detector = AntPathDetector()
    ### setup detector
    detector.scale = options.scale
    detector.debug = options.debug
    detector.outputDirectory = options.output
    
    if detector.loadVideoFile(options.filename):
        try:
            detector.detect()
        except Exception:
            exit()