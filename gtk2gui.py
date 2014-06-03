'''
Created on 03.06.2014

@author: kolbe
'''
import pygtk
pygtk.require('2.0')
import gtk
from antpathdetector import AntPathDetector

class MainWindow(object):
    
    def __init__(self):
        ### setup window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.show()
        self.window.connect("delete_event", self.delete_event)
        
        ### setup layout
        self.vbox1 = gtk.VBox(False, 0)
        
        ### setup buttons
        self.btnSrcVideo = gtk.Button("Open video")
        self.btnSrcVideo.connect("clicked", self.srcDialog, None)
        self.btnSrcVideo.show()
        
        self.btnDstDir = gtk.Button("Destination Directory")
        self.btnDstDir.connect("clicked", self.dstDialog, None)
        self.btnDstDir.show()

        self.btnDetect = gtk.Button("Start detection")
        self.btnDetect.connect("clicked", self.startDetection, None)
        self.btnDetect.show()
        
        self.progressbar = gtk.ProgressBar(adjustment=None)
        self.progressbar.set_fraction(0.0)
        self.progressbar.show()
                
        ### add all
        self.vbox1.pack_start(self.btnSrcVideo, False, False, 0)
        self.vbox1.pack_start(self.btnDstDir, False, False, 0)
        self.vbox1.pack_start(self.btnDetect, False, False, 0)
        self.vbox1.pack_start(self.progressbar, False, False, 0)
        self.vbox1.show()
        self.window.add(self.vbox1)
        
        ### setup detector
        self.detector = AntPathDetector()
        self.detector.showImageCallback = self.showImage
        self.detector.updateProgress = self.updateProgress
        self.img_gtk = None
        
        
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False
    
    def main(self):
        gtk.main()
        
    def srcDialog(self, widget, data=None):
        dia = gtk.FileChooserDialog(title="Choose videofile",
                                    parent=self.window,
                                    action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                    buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        dia.set_default_response(gtk.RESPONSE_OK)
        response = dia.run()
        if response == gtk.RESPONSE_OK:
            print dia.get_filename(), 'selected'
            self.detector.loadVideoFile(dia.get_filename())
        elif response == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
        dia.destroy()
         
    def dstDialog(self, widget, data=None):
        dia = gtk.FileChooserDialog(title="Choose output directory",
                                    action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                    buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        
        response = dia.run()
        if response == gtk.RESPONSE_OK:
            self.detector.outputDirectory = dia.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            print "Closed..."
        dia.destroy()

    def startDetection(self, widget, data=None):
        print "start!"
        self.btnDetect.set_sensitive(False)
        self.btnDstDir.set_sensitive(False)
        self.btnSrcVideo.set_sensitive(False)
        try:
            self.detector.detect()
            self.delete_event(None, None, None)
        except Exception:
            self.btnDetect.set_sensitive(True)
            self.btnDstDir.set_sensitive(True)
            self.btnSrcVideo.set_sensitive(True)
            message = gtk.MessageDialog(parent=self.window,
                                    flags=0,
                                    type=gtk.MESSAGE_ERROR,
                                    buttons=gtk.BUTTONS_NONE)
            message.set_markup("Error! Wrong video format?")
            message.run()        
        
    def showImage(self, image):   
        self.img = image
        if self.img_gtk is None:
            self.img_gtk = gtk.Image()# Create gtk.Image() only once
            self.vbox1.add(self.img_gtk)# Add Image in the box, only once
        self.img_pixbuf = gtk.gdk.pixbuf_new_from_data(self.img.reshape(-1),
                                                gtk.gdk.COLORSPACE_RGB,
                                                False,
                                                8,
                                                self.img.shape[1],
                                                self.img.shape[0],
                                                self.img.shape[1]*self.img.shape[2])
        self.img_gtk.set_from_pixbuf(self.img_pixbuf)
        self.img_gtk.show()
        
    def updateProgress(self, progress):
        self.progressbar.set_fraction(progress/100.0)
        self.progressbar.set_text("%.2f%%"%progress)


if __name__ == '__main__':
    w = MainWindow()
    w.main()