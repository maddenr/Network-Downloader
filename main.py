import urllib
import NDS
from threading import Thread
import os
import os.path as path
from time import sleep
import libtorrent as lt
import sys


ftpQueuePath = './ftpDownloadQueue/'
torQueuePath = './torDownloadQueue/'
ftpCurrentDownload = 'currentFTP.txt'
torCurrentDownload = 'currentTOR.txt'

def ftpThread():
	try:
		while True:
			ftpQueue = os.listdir(ftpQueuePath)
			if ftpQueue != []:
				for fileName in ftpQueue:
					print ("opening %s" % fileName)
					with open(ftpQueuePath+fileName) as ftpURLFile:
						ftpUrl = ftpURLFile.read()
					os.remove(ftpQueuePath+fileName)
					
					with open(ftpCurrentDownload, "w+") as file:
						file.write(fileName[:-4])
					print ("Retrieving: %s\tAs: %s" % (ftpUrl, fileName[:-4]))
					urllib.urlretrieve(ftpUrl, fileName[:-4])#trims .txt ending to file name. save as blah.zip.txt
					os.remove(ftpCurrentDownload)
					print "Finished"
			else:
				print "sleeping..."
				sleep(10)
				
	except Exception as e:
		print ("FTP Error:	%s" % e)

		
def torThread():
	ses = lt.session()
	ses.listen_on(6881, 6891)
	while True:
		torQueue = os.listdir(torQueuePath)
		try:
			if torQueue != []:
				for fileName in torQueue:
					ti = lt.torrent_info(path.abspath(torQueuePath+fileName))
					print ("Retrieving: %s" % ti)
					torrent = ses.add_torrent({'ti' : ti, 'save_path' : './'})
					os.remove(torQueuePath+fileName)
					with open(torCurrentDownload, "w+") as file:
						#file.write(fileName[:-4])
					while (not torrent.is_seed()):
						sleep(1)
					os.remove(torCurrentDownload)
					print "Finished"
			else:
				print "sleeping..."
				sleep(10)
		except Exception as e:
			print ("Error in torrent: %s" % e)
					
		
def serverThread():
	NDS.start()

		
def main():
	#ftpProcess = Thread(target=ftpThread)
	#torProcess = Thread(target=torThread)
	#serverProcess = Thread(target=serverThread)
	torThread()
	#ftpProcess.start()
	
	
	
	
	
	
	
	
	
	
	
	
	