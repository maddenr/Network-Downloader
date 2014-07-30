from flask import Flask, render_template, url_for, send_from_directory, redirect, request
import os
from werkzeug.utils import secure_filename
from os.path import isfile

ALLOWED_EXTENSIONS = set(['tor'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './torQueue/'
ftpQueuePath = './ftpDownloadQueue/'
torQueuePath = './torDownloadQueue/'
ftpCurrentDownload = 'currentFTP.txt'
torCurrentDownload = 'currentTOR.txt'

@app.route("/")
def index():
	return render_template("base.html")
	
@app.route("/downloadQueue")
def downloadQueue():
	#poll for downloads
	ftpDownloads = os.listdir(ftpQueuePath)
	torDownloads = os.listdir(torQueuePath)
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
					cur_ftp = curFtp, cur_tor = curTor, ftpDownloads = ftpDownloads, torDownloads = torDownloads)

@app.route("/addToQueue/ftp/", methods=['POST'])
def addToFtpQueue():
	if request is None:
		return redirect("/?404")
	print request.form['url']
	#with open(ftpQueuePath+ NAME+".txt", "w+") as file:
		#file.write(FTPURL)
	return redirect("/")

@app.route("/addToQueue/tor/", methods=['POST'])
def addToTorQueue():
	if request is not None:
		file = request.files['file']
		if allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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