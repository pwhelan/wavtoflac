#!/usr/bin/env python
#
# Simple Script to Encode all WAV files as FLAC and tag them in the process.
#

import sys
import os
import threading
import dircache
import time


try:
	import pygtk
	pygtk.require("2.0")
except:
	pass
try:
	import gtk
	import gtk.glade
except:
	sys.exit(1)

gtk.gdk.threads_init()


class pyWavToFlac:
	def __init__(self):
		self.gladefile = "wavtoflac.glade"
		self.wTree = gtk.glade.XML(self.gladefile, "mainWindow")
		
		dic = {"on_mainWindow_destroy" : gtk.main_quit}
		self.wTree.signal_autoconnect(dic)
	
	def setDirectory(self, dir):
		lblDirectory = self.wTree.get_widget("lblDirectory")
		lblDirectory.set_label(dir)
	
	def addTrack(self, file):
		trackDlg = pyWavToFlacTrackDlg()
		track = trackDlg.run(file)

class pyWavToFlacTrackDlg:
	
	def __init__(self):
		self.gladefile = "wavtoflac.glade"
		self.track = {
			'artist' : '',
			'title' : '',
			'album' : '',
			'tracknumber' : '',
			'year' : ''
		}
	
	def run(self, file):
		
		self.wTree = gtk.glade.XML(self.gladefile, "trackDlg")
		self.dlg = self.wTree.get_widget("trackDlg")
		
		self.result = self.dlg.run()
		self.dlg.destroy()
		
		print "RESULT:", self.result
		return self.result, self.track

class WavScanner(threading.Thread):
	def __init__(self, dir):
		threading.Thread.__init__(self)
		self._dir = dir
	
	def scan(self, cwd = None):
		
		if cwd == None:
			cwd = self._dir
		
		#print "Scanning:", cwd
		
		gtk.gdk.threads_enter()
		window.setDirectory(cwd)
		gtk.gdk.threads_leave()
		
		
		files = dircache.listdir(cwd)
		for file in files:
			fname = cwd + '/' + file
			
			if fname.endswith('.wav'):
				
				print "Wave File:", fname
				
				gtk.gdk.threads_enter()
				window.addTrack(fname)
				gtk.gdk.threads_leave()
			
			elif os.path.isdir(fname):
				
				self.scan(fname)	
	
	def run(self):
		self.scan()
		
		gtk.gdk.threads_enter()
		gtk.main_quit()
		gtk.gdk.threads_leave()

if __name__ == "__main__":
	window = pyWavToFlac()
	
	scanner = WavScanner('/media/disk/psytrance')
	scanner.start()
	
	gtk.main()
