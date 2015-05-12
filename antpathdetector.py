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
    max_video_size = (320, 240)
    
    outputDirectory = None
    debug = False
    
    videoCap = None
    
    #GUI callback
    updateProgress = None
    showImageCallback = None
    showImageWidth = 640


    def __init__(self):
        pass
        
    def loadVideoFile(self, filename):
        print "loading video %s" % filename
        try:
            filename = int(filename)
        except:
            filename = os.path.abspath(filename)
        self.videoCap = cv2.VideoCapture()
        self.frameNr = 0
        
        if self.videoCap.open(filename):
            return True
        
        self.videoCap = None
        return False
    
    def _saveImages(self, frame, blend, path):
        #cv2.imwrite(os.path.join(self.outputDirectory, "%05d.png" % self.frameNr), outFrame)
        width, height, depth = frame.shape
        cv2.imwrite(os.path.join(self.outputDirectory, "frame_%05d.png" % self.frameNr), frame)
        cv2.imwrite(os.path.join(self.outputDirectory, "blend_%05d.png" % self.frameNr), cv2.resize(blend, (height, width), interpolation=cv2.INTER_NEAREST))
        
    
    def detect(self):
        
        if not self.videoCap:
            raise Exception
        
        frameCount = self.videoCap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        
        ### setup resized
        val, frame = self.videoCap.read()
        width, height, depth = frame.shape
        resize_factor = min(self.max_video_size[0] / float(width), self.max_video_size[1] / float(height))
        resized = cv2.resize(frame, (int(height*resize_factor), int(width*resize_factor)))
        resized_width, resized_height, resized_depth = resized.shape
        ### output
        #outFrame = np.zeros((width*2,height*2, 3), np.uint8)        
        outFrame = np.zeros((resized_width*2,resized_height*2, 3), np.uint8)
        ### running average
        average = np.float32(resized)
        path = np.zeros(resized.shape, resized.dtype)
        averagePath = np.float32(path)
        
        ### start capture loop
        while val:
            t0 = time.time()
            self.frameNr += 1
            fraction = (100.0/frameCount)*self.frameNr
            #print "frame %d/%d [%d%%]" % (self.frameNr, frameCount, fraction)
            
            ### update GUI progress
            if self.updateProgress:
                self.updateProgress(fraction)
            
            resized = cv2.resize(frame, (resized_height, resized_width))
            
            cv2.accumulateWeighted(resized,average,self.alpha)
            diff = cv2.absdiff(resized, cv2.convertScaleAbs(average))
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            ret, diff = cv2.threshold(diff_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            if ret <= 5:
                diff = np.zeros(diff.shape, dtype=diff.dtype)
            diff = cv2.cvtColor(diff, cv2.COLOR_GRAY2BGR)
            
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
                if self.debug or self.outputDirectory:
                    outFrame[0:resized_width, 0:resized_height] = resized
                    outFrame[0:resized_width, resized_height:resized_height*2] = diff
                    outFrame[resized_width:resized_width*2, 0:resized_height] = blend
                    outFrame[resized_width:resized_width*2, resized_height:resized_height*2] = averagePathGray
                    cv2.imshow("out", outFrame)
                if self.outputDirectory is not None:
                    self._saveImages(frame, blend, averagePathGray)
                if self.showImageCallback is not None:
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
            print "%0.2ffps" % (1.0 / (time.time()-t0))
        
        cv2.imwrite(os.path.join(self.outputDirectory, "%d_path.png" % time.time()), path)
            
            
            
            