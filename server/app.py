from flask import Flask, flash, request, redirect, url_for, render_template
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'mp4'}
import os
# from flask_socketio import SocketIO
# from flask_socketio import send, emit
import cv2 
import random
import vector_search as vsearch

app = Flask(__name__)
app.config['SECRET_fKEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

UPLOAD_FOLDER = "data"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == '__main__':
    socketio.run(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def start():
    return redirect(url_for('upload_file'))  
    # return render_template('index.html', name="bob the bear")

@app.route('/gpt_query', methods=['GET', 'POST'])
def gpt_query():
    if request.method == 'POST':
        # check if the post request has the file part
        gptquery = request.form['gptquery']
        #function to pass query to database    
        results = vsearch.vector_search(gptquery) 
        video_path = results[2]
        print(video_path)
        detail_path = results[3]
        print(detail_path)
        return redirect(url_for('index'))
  
    return render_template('gpt.html', name="bob")



@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        if 'details' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        #here it is 
        details = request.files['details']
        
        desc = request.form['desc']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename) and file.filename.endswith('.mp4'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # test
            vsearch.insert_data(filename, desc, "hackMIT_detail.txt")
            return redirect(url_for('gpt_query'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('gpt_query'))

    return render_template('upload.html')

# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})


@app.route('/index')       
# def localize(filename):
    # socketio.emit('localized', list(pos))
    
def index():
    #call name from database memory or desc

    return render_template('index.html', name='HOHDOQUWHDOU')