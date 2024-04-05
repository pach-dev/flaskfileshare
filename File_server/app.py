from flask import Flask, render_template, request, send_file, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx", "pdf","docx","jpeg","jpg"}

#DEFAULT PATH TO INDEX HTML
@app.route('/')
def index():
    return render_template('index.html')


#def image():
    #background_image_url = "/static/images/background_image.jpg"
    #return render_template(background_image_url)


#ROUTE AND FUNCTION TO UPLOAD FILES FUNCTION ALLOWS SPECIFIC FILE EXTENSIONS
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if "." not in filename:
                raise ValueError("file has no extension")
        
        file_extension = filename.split(".",1)[1].lower()


        if file_extension not in ALLOWED_EXTENSIONS:
                raise ValueError("File type not allowed")
        
        else:
             
            return 'File uploaded successfully'

            

    

#DOWNLOAD FILES, FUNCTION TAKES THE FILENAME AS TH ARGUMENT AND USED GET METHOD TO RETRIEVE
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

#LISTS A GROUP OF FILES UPLOADED
@app.route('/list_files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('list_files.html', files=files)

#VIEW FILES AS A USER 
@app.route('/view_files')
def view_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('view_files.html', files=files)

#THIS IS FOR THE USER TO VIEW A SPECIFIC FILE AND DOWNLOAD
@app.route('/view/<filename>', methods=['GET'])
def view_file_in_browser(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content
    else:
        return 'File not found'



#FILES CAN BE DELETED
@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('list_files'))
    else:
        return 'File not found'


if __name__ == '__main__':
    app.run(debug=True)
