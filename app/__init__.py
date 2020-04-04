# this file tells python that this is a package and initializes the things we need

from flask import Flask, render_template, url_for, redirect, request, flash
from flask_bcrypt import Bcrypt
import os
import secrets
import zipfile
from werkzeug.utils import secure_filename
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b49a2921e19d1ceda4ea97c54ccb51a2'		# this protects the information entered in the forms from modifying cookies, cross-site request forgery attacks, etc.

if __name__ == '__main__':
	app.run(host = '127.0.0.1', port = '5000')


# From here...

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['zip'])


basepath = os.path.join(app.root_path, 'static/ZipFiles')		# app.root_path gives the root path of application all the way up the package directory

def save_file(uploaded_file):
	for entry in os.listdir(basepath):							# deleting all the previously saved files from this folder
		file_name = os.path.join(basepath, entry)
		if os.path.isfile(file_name):
			os.remove(file_name)

	random_hex = secrets.token_hex(8)
	filename = random_hex + '.zip'
	zip_fn = secure_filename(filename)
	zip_fp = os.path.join(basepath, zip_fn)

	uploaded_file.save(zip_fp)

	return zip_fn

def extract_files(zip_fn):
	zip_ref = zipfile.ZipFile(os.path.join(basepath, zip_fn), 'r')
	zip_ref.extractall(basepath)
	zip_ref.close()

@app.route("/", methods=['POST', 'GET'])
@app.route("/home", methods=['POST', 'GET'])
def home():
	print(basepath)
	if request.method == 'POST':

		# in case the post request has no 'file' part. 'file' is the name we gave to the file input in home.html.
		if 'file' not in request.files:
			flash("The file was not found!", 'danger')
			return redirect(url_for('home'))

		file = request.files['file']

		# if user does not select file, browser submits an empty part without filename
		if file.filename == '':
			flash("Please upload a zip file", 'info')
			return redirect(url_for('home'))

		if file:
			if allowed_file(file.filename):
				folder_name = file.filename.rsplit('.', 1)[0]		# name of the folder that will be created after extracting files from zip
				zip_fn = save_file(file)							# name of zip file along with .zip and passed through secure_filename() function
				extract_files(zip_fn)
				try:
					return redirect(url_for('static', filename = 'ZipFiles/' + folder_name + '/index.html'))
				except: # catch *all* exceptions
					e = sys.exc_info()[0]
					# write_to_page( "<p>Error: %s</p>" % e )
					flash(str(e), 'info')
			else:	
				flash("Make sure the extension of uploaded file is .zip", 'danger')		# if file extension wasn't zip
				return redirect(url_for('home'))
	return render_template("home.html")
