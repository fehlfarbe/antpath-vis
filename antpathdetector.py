'''
Created on 02.06.2014

@author: kolbe
'''
import os, time
import cv2
import numpy as np

class AntPathDetector(object):
    '''
    classdocs
    '''
    alpha = 0.05
    pathAlpha = 0.01
    minFrames = 2.0 / alpha
    frameNr = 0
    scale = 0.4
    
    outputDirectory = "out_%d" % time.time()
    debug = False
    
    videoCap = None
    
    #GUI callback
    updateProgress = None
    showImageCallback = None
    showImageWidth = 640


    def __init__(self):
        pass
        
    def loadVideoFile(self, filename):
        filename = os.path.abspath(filename)
        print "loading video %s" % filename
        self.videoCap = cv2.VideoCapture()
        self.frameNr = 0
        
        if self.videoCap.open(filename):
            return True
        
        self.videoCap = None
        return False
    
    def detect(self):
        
        if not self.videoCap:
            raise Exception
        
        frameCount = self.videoCap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        
        ### setup resized
        val, frame = self.videoCap.read()
        width, height, depth = frame.shape
        resized = cv2.resize(frame, (int(height*self.scale), int(width*self.scale)))
        resized_width, resized_height, resized_depth = resized.shape
        ### running average
        average = np.float32(resized)
        path = np.minimum(resized, 0)
        averagePath = np.float32(path)
        ### start capture loop
        while val:
            self.frameNr += 1
            fraction = (100.0/frameCount)*self.frameNr
            print "frame %d/%d [%d%%]" % (self.frameNr, frameCount, fraction)
            
            ### update GUI progress
            if self.updateProgress:
                self.updateProgress(fraction)
            
            resized = cv2.resize(frame, (int(height*self.scale), int(width*self.scale)))
            
            cv2.accumulateWeighted(resized,average,self.alpha)
            diff = cv2.absdiff(resized, cv2.convertScaleAbs(average))
            ret,diff = cv2.threshold(diff,10,255,cv2.THRESH_TOZERO)
            
            if self.frameNr > self.minFrames:
                path = np.maximum(diff, path)
                
                ### average path
                cv2.accumulateWeighted(diff, averagePath, self.pathAlpha)
                averagePathGray = cv2.convertScaleAbs(cv2.cvtColor(cv2.cvtColor(averagePath, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)*255)
                #if options.debug:
                #    cv2.imshow("avergaePathGray", averagePathGray)
                #averagePathGrayCol = cv2.convertScaleAbs(cv2.cvtColor(averagePathGray, cv2.COLOR_GRAY2BGR)*255)
                
                ### hsv test (heatmap)
                hsv = cv2.cvtColor(averagePathGray, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                h = (np.minimum(v, 120)-120)
                merged = cv2.merge( (h, np.maximum(s, 255), v) )
                heatmap = cv2.cvtColor(merged, cv2.COLOR_HSV2BGR)
                if self.debug:
                    cv2.imshow("hsv", heatmap)
                
                ###blending test
                blend = cv2.addWeighted(resized, 1.0, heatmap, 0.5, 0)
                if self.debug:
                    cv2.imshow("blend", blend)
                
                ### save to output
                outFrame = np.zeros((resized_width*2,resized_height*2,3), np.uint8)
                outFrame[0:resized_width, 0:resized_height] = resized
                outFrame[0:resized_width, resized_height:resized_height*2] = diff
                outFrame[resized_width:resized_width*2, 0:resized_height] = blend
                outFrame[resized_width:resized_width*2, resized_height:resized_height*2] = averagePathGray
                cv2.imwrite(os.path.join(self.outputDirectory, "%05d.png" % self.frameNr), outFrame)

                if self.showImageCallback:
                    #cv2.imshow("123", outFrame)
                    image = cv2.cvtColor(outFrame, cv2.COLOR_BGR2RGB)
                    factor = float(self.showImageWidth) / image.shape[1]
                    newWidth = int(image.shape[1] * factor)
                    newHeight = int(image.shape[0] * factor)
                    self.showImageCallback(cv2.resize(image, (newWidth,newHeight)))
                
            if self.debug:
                #cv2.imshow('average', res2)
                cv2.imshow('diff', diff)
                cv2.imshow('path', path)
                #cv2.imshow('averagePath', averagePath)
                #cv2.imshow("prev", resized)
            cv2.waitKey(1)
            val, frame = self.videoCap.read()
        
        cv2.imwrite(os.path.join(self.outputDirectory, "%d_path.png" % time.time()), path)
            
            
            
            