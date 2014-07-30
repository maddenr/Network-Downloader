from flask import Flask, render_template, url_for, send_from_directory, redirect, request
import os
from werkzeug.utils import secure_filename
from os.path import isfile, join

ALLOWED_EXTENSIONS = set(['torrent'])

app = Flask(__name__)
ftpQueuePath = './ftpDownloadQueue/'
torQueuePath = './torDownloadQueue/'
ftpCurrentDownload = 'currentFTP.txt'
torCurrentDownload = 'currentTOR.txt'
downloadsFolder = './Downloads/'

@app.route("/")
def index():
	return render_template("base.html")
	
@app.route("/downloadQueue")
def downloadQueue():
	#poll for downloads
	ftpDownloads = os.listdir(ftpQueuePath)
	torDownloads = os.listdir(torQueuePath)
	downloads = os.listdir(downloadsFolder)
	if isfile(ftpCurrentDownload):
		with open(ftpCurrentDownload, "r") as currentFtpFile:
			curFtp = currentFtpFile.read()
	else:
		curFtp = None
	
	if isfile(torCurrentDownload):
		with open(torCurrentDownload, "r") as currentTorFile:
			curTor = currentTorFile.read()
	else:
		curTor = None
	
	return render_template("Download Queue.html", num_tor = len(torDownloads), num_ftp = len(ftpDownloads),
					cur_ftp = curFtp, cur_tor = curTor, ftpDownloads = ftpDownloads, torDownloads = torDownloads, num_dl=len(downloads), downloads=downloads)

@app.route("/addToQueue/ftp/", methods=['POST'])
def addToFtpQueue():
	if request is None:
		return redirect("/?404")
	print ftpQueuePath+request.form['fileName']+".txt"
	with open(ftpQueuePath+request.form['fileName']+".txt", "w+") as file:
		file.write(request.form['url'])
	return redirect("/")

@app.route("/addToQueue/tor/", methods=['POST'])
def addToTorQueue():
	if request is not None:
		file = request.files['file']
		if allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(join(torQueuePath, filename))
		else:
			return redirect("/?error=406")
	else:
		return redirect("/?error=404")
		
	return redirect("/")
	
@app.route("/removeFromQueue/<string:type>/<string:name>/")
def removeFromQueue():
	return None
	
@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def start():
	app.run(debug=True)

if __name__ == '__main__':
	start()