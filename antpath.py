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
                  default="out_%d" % time.time(),
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
    
        
    #exit(0)
    
    #videofile = "ants_01.h264"
    #videofile = "output.mp4"
    #scale = 0.4
#     alpha = 0.05
#     pathAlpha = 0.01
#     minFrames = 2.0 / alpha
#     frameNr = 0
    ### output
    #outDirName = "out_%d" % time.time()
    #os.mkdir(outDirName)
    
    
#     ### open videofile
#     cap = cv2.VideoCapture()
#     if not cap.open(options.filename):
#         parser.error("Can't open videofile!")
#     frameCount = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
#     
#     ### start capture loop
#     val, frame = cap.read()
#     width, height, depth = frame.shape
#     resized = cv2.resize(frame, (int(height*options.scale), int(width*options.scale)))
#     resized_width, resized_height, resized_depth = resized.shape
#     ### running average
#     average = np.float32(resized)
#     path = np.minimum(resized, 0)
#     averagePath = np.float32(path)
#     while val:
#         frameNr += 1
#         print "frame %d/%d [%d%%]" % (frameNr, frameCount, (100.0/frameCount)*frameNr)
#         
#         resized = cv2.resize(frame, (int(height*options.scale), int(width*options.scale)))
#         
#         cv2.accumulateWeighted(resized,average,alpha)
#         diff = cv2.absdiff(resized, cv2.convertScaleAbs(average))
#         ret,diff = cv2.threshold(diff,10,255,cv2.THRESH_TOZERO)
#         
#         if frameNr > minFrames:
#             path = np.maximum(diff, path)
#             
#             ### average path
#             cv2.accumulateWeighted(diff, averagePath, pathAlpha)
#             averagePathGray = cv2.convertScaleAbs(cv2.cvtColor(cv2.cvtColor(averagePath, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)*255)
#             #if options.debug:
#             #    cv2.imshow("avergaePathGray", averagePathGray)
#             #averagePathGrayCol = cv2.convertScaleAbs(cv2.cvtColor(averagePathGray, cv2.COLOR_GRAY2BGR)*255)
#             
#             ### hsv test (heatmap)
#             hsv = cv2.cvtColor(averagePathGray, cv2.COLOR_BGR2HSV)
#             h, s, v = cv2.split(hsv)
#             h = (np.minimum(v, 120)-120)
#             merged = cv2.merge( (h, np.maximum(s, 255), v) )
#             heatmap = cv2.cvtColor(merged, cv2.COLOR_HSV2BGR)
#             if options.debug:
#                 cv2.imshow("hsv", heatmap)
#             
#             ###blending test
#             blend = cv2.addWeighted(resized, 1.0, heatmap, 0.5, 0)
#             if options.debug:
#                 cv2.imshow("blend", blend)
#             
#             ### save to output
#             outFrame = np.zeros((resized_width*2,resized_height*2,3), np.uint8)
#             outFrame[0:resized_width, 0:resized_height] = resized
#             outFrame[0:resized_width, resized_height:resized_height*2] = diff
#             outFrame[resized_width:resized_width*2, 0:resized_height] = blend
#             outFrame[resized_width:resized_width*2, resized_height:resized_height*2] = averagePathGray
#             cv2.imwrite(os.path.join(options.output, "%05d.png" % frameNr), outFrame)
#             cv2.imshow("join", outFrame)
#             
#         if options.debug:
#             #cv2.imshow('average', res2)
#             cv2.imshow('diff', diff)
#             cv2.imshow('path', path)
#             #cv2.imshow('averagePath', averagePath)
#             #cv2.imshow("prev", resized)
#         cv2.waitKey(1)
#         val, frame = cap.read()
#     
#     cv2.imwrite(os.path.join(options.output, "%d_path.png" % time.time()), path)
