from flask import Flask, render_template, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './torQueue/'

@app.route("/")
def index():
	return render_template("base.html")
	
@app.route("/downloadQueue")
def downloadQueue():
	#poll for downloads
	ftpDownloads = []
	torDownloads = []
	curTor = None
	curFtp = None
	return render_template("Download Queue.html", num_tor = len(torDownloads), num_ftp = len(ftpDownloads),
					cur_ftp = curFtp, cur_tor = curTor, ftpDownloads = ftpDownloads, torDownloads = torDownloads)

@app.route("/addToQueue/ftp/", , methods=['POST'])
def addToFtpQueue():
	return None

@app.route("/addToQueue/tor/", , methods=['POST'])
def addToTorQueue():
	file = request.files['file']
        if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		else
			render_template("base.json", status=False)
        return render_template("base.json", status=True)
	
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



if __name__ == '__main__':
	app.run(debug=True)