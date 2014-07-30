import urllib
import NDS
from threading import Thread
import os
from time import sleep

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
			else:
				print "sleeping..."
				sleep(10)
				
	except Exception as e:
		print ("FTP Error:	%s" % e)

		
def torThread():
	try:
		while True:
			for file in os.listdir(torQueuePath):
				print ""
	except Exception as e:
		print ("Torrent Error:	%s" % e)
		
def serverThread():
	NDS.start()

		
def main():
	#ftpProcess = Thread(target=ftpThread)
	#torProcess = Thread(target=torThread)
	#serverProcess = Thread(target=serverThread)
	ftpThread()
	#ftpProcess.start()